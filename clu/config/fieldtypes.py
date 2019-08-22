# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime, timedelta
from functools import wraps

import abc
import collections.abc
import contextlib
import weakref

from clu.constants.consts import DEBUG, NoDefault
from clu.config.base import NAMESPACE_SEP
from clu.fs.misc import stringify, wrap_value
from clu.naming import nameof
from clu.predicates import (negate,
                            isclasstype, always, no_op,
                            haspyattr, getpyattr,
                            uncallable, isexpandable, iscontainer,
                            tuplize, slots_for)
from clu.typology import ismapping, isnumber, isstring
from clu.exporting import Slotted, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class ValidationError(Exception):
    pass

hoist = lambda thing: uncallable(thing) and wrap_value(thing) or thing

# functional_and = lambda thing, *functions: all(function(thing) \
#                                            for function in functions
#                                             if function is not None)
#
# def functional_set(thing, *functions):
#     for function in functions:
#         if function is not None:
#             thing = function(thing)
#     return thing

@export
class FlatOrderedSet(collections.abc.Set,
                     collections.abc.Sequence,
                     collections.abc.Hashable,
                     metaclass=Slotted):
    
    __slots__ = tuplize('things')
    
    def __init__(self, *things, predicate=always):
        if uncallable(predicate):
            raise ValueError("FlatOrderedSet requires a callable predicate")
        thinglist = []
        if len(things) == 1:
            if isexpandable(things[0]):
                things = things[0]
            if iscontainer(things[0]):
                things = tuple(things[0])
        for thing in things:
            if thing is not None:
                if isinstance(thing, type(self)):
                    for other in thing.things:
                        if other not in thinglist:
                            thinglist.append(other)
                elif predicate(thing):
                    if thing not in thinglist:
                        thinglist.append(thing)
        self.things = tuple(thinglist)
    
    def __iter__(self):
        return iter(self.things)
    
    def __len__(self):
        return len(self.things)
    
    def __contains__(self, thing):
        return thing in self.things
    
    def __getitem__(self, idx):
        return self.thing[idx]
    
    def __bool__(self):
        return len(self.things) > 0
    
    def __hash__(self):
        return hash(self.things) & hash(id(self.things))
    
    def __repr__(self):
        cnm = nameof(type(self))
        lst = repr(self.things)
        hxa = hex(id(self))
        return f"{cnm}({lst}) @ {hxa}"

@export
class functional_and(FlatOrderedSet,
                     collections.abc.Callable):
    
    def __init__(self, *functions):
        super(functional_and, self).__init__(predicate=callable, *functions)
    
    def __call__(self, thing):
        return all(function(thing) \
               for function in reversed(self.things) \
                if function is not None)

@export
class functional_set(FlatOrderedSet,
                     collections.abc.Callable):
    
    def __init__(self, *functions):
        super(functional_set, self).__init__(predicate=callable, *functions)
    
    def __call__(self, thing):
        for function in reversed(self.things):
            if function is not None:
                thing = function(thing)
        return thing

@export
class FieldBase(abc.ABC, metaclass=Slotted):
    
    __slots__ = ('name', 'namespace',
                         'default',
                         'validator',
                         'extractor',
                         'allow_none')
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True):
        """ FieldBase __init__(…): initialize common attributes """
        
        self.namespace = None
        self.default = default
        self.validator = validator or always
        self.extractor = extractor or no_op
        self.allow_none = bool(allow_none)
        
        if uncallable(self.validator):
            raise TypeError("validators must be callables")
        
        if uncallable(self.extractor):
            raise TypeError("extractors must be callables")
    
    def __set_name__(self, cls, name):
        self.name = name
    
    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return getpyattr(instance, 'fields').get(self.name,
                                       namespace=self.namespace,
                                         default=self.default or NoDefault)
    
    def __set__(self, instance, value):
        # Check for outlawed Nones:
        if value is None and not self.allow_none:
            raise ValidationError(f"Field “{self.name}” does not allow None values")
        
        # Do extraction and validation:
        try:
            value = self.extractor(value)
        except (TypeError, ValueError, ValidationError) as exc:
            raise ValidationError(f"Extraction failue in “{self.name}”: {exc}")
        
        if not self.validator(value):
            raise ValidationError(f"Validation failue in “{self.name}”")
        
        # Set and return:
        # getpyattr(instance, 'fields')[self.name] = value
        getpyattr(instance, 'fields').set(self.name, value,
                                namespace=self.namespace)
        return value
    
    def __delete__(self, instance):
        getpyattr(instance, 'fields').delete(self.name,
                                   namespace=self.namespace)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return stringify(self, slots_for(type(self)))

@export
class SchemaField(FieldBase):
    
    def __init__(self, cls, validator=None):
        self.cls = cls
        isthisclass = lambda thing: isinstance(thing, cls)
        super(SchemaField, self).__init__(default=cls,
                                          validator=functional_and(validator,
                                                                   isthisclass,
                                                                   isclasstype))
        
    def __set__(self, instance, value):
        try:
            if ismapping(value):
                value = self.cls(**value)
            return super(SchemaField, self).__set__(instance, value)
        except ValidationError as exc:
            raise ValidationError(f"Validation failure in {nameof(type(self))}: {exc}")

@export
class StringField(FieldBase):
    
    __slots__ = ('min_length', 'max_length')
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True,
                       min_length=None,
                       max_length=None):
        
        super(StringField, self).__init__(default=default,
                                          validator=functional_and(validator,
                                                                   isstring,
                                                                   negate(isclasstype)),
                                          extractor=extractor,
                                          allow_none=allow_none)
        minl = min_length and int(min_length) or None
        maxl = max_length and int(max_length) or None
        if minl is not None and maxl is not None:
            if minl > maxl:
                raise ValidationError("min_length must be smaller than max_length: {minl} > {maxl}")
        self.min_length = minl
        self.max_length = maxl
    
    def __set__(self, instance, value):
        out = super(StringField, self).__set__(instance, value)
        if self.min_length is not None:
            if len(out) < self.min_length:
                raise ValidationError(f"Validation failure in {nameof(type(self))}: len(string) < min_length")
        if self.max_length is not None:
            if len(out) <= self.max_length:
                raise ValidationError(f"Validation failure in {nameof(type(self))}: len(string) > max_length")
        return out

@export
class IntField(FieldBase):
    
    __slots__ = ('min_value', 'max_value')
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True,
                       min_value=None,
                       max_value=None):
        
        super(IntField, self).__init__(default=default or 0,
                                       validator=functional_and(validator,
                                                                isnumber,
                                                                negate(isclasstype)),
                                       extractor=functional_set(extractor, int),
                                       allow_none=allow_none)
        minv = min_value and int(min_value) or None
        maxv = max_value and int(max_value) or None
        if minv is not None and maxv is not None:
            if minv > maxv:
                raise ValidationError("min_value must be smaller than max_value: {minv} > {maxv}")
        self.min_value = minv
        self.max_value = maxv
    
    def __set__(self, instance, value):
        if not isnumber(value):
            raise ValidationError("Cannot convert a “{value}” to integer")
        out = super(IntField, self).__set__(instance, value)
        if self.min_value is not None:
            if out < self.min_value:
                raise ValidationError(f"Validation failure in {nameof(type(self))}: integer < min_length")
        if self.max_value is not None:
            if out <= self.max_value:
                raise ValidationError(f"Validation failure in {nameof(type(self))}: integer > max_length")
        return out

@export
class UIntField(IntField):
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True,
                       min_value=None,
                       max_value=None):
        
        if max_value is not None:
            if max_value < 0:
                raise ValidationError("max_value must be positive for {nameof(type(self))} fields")
        
        super(UIntField, self).__init__(default=default or 0,
                                        validator=functional_and(validator,
                                                                 lambda thing: thing > 0),
                                        extractor=extractor,
                                        allow_none=allow_none,
                                        min_value=min_value or 0,
                                        max_value=max_value)

@export
class FloatField(FieldBase):
    
    __slots__ = ('min_value', 'max_value')
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True,
                       min_value=None,
                       max_value=None):
        
        super(FloatField, self).__init__(default=default or 0.0,
                                         validator=functional_and(validator,
                                                                  isnumber,
                                                                  negate(isclasstype)),
                                         extractor=functional_set(extractor, float),
                                         allow_none=allow_none)
        minv = min_value and float(min_value) or None
        maxv = max_value and float(max_value) or None
        if minv is not None and maxv is not None:
            if minv > maxv:
                raise ValidationError("min_value must be smaller than max_value: {minv} > {maxv}")
        self.min_value = minv
        self.max_value = maxv
    
    def __set__(self, instance, value):
        if not isnumber(value):
            raise ValidationError("Cannot convert a “{value}” to floating-point")
        out = super(FloatField, self).__set__(instance, value)
        if self.min_value is not None:
            if out < self.min_value:
                raise ValidationError(f"Validation failure in {nameof(type(self))}: float < min_length")
        if self.max_value is not None:
            if out <= self.max_value:
                raise ValidationError(f"Validation failure in {nameof(type(self))}: float > max_length")
        return out

@export
class BooleanField(FieldBase):
    
    def __init__(self, default=True,
                       validator=None,
                       extractor=None):
        
        super(BooleanField, self).__init__(default=default,
                                           validator=validator,
                                           extractor=functional_set(extractor, bool),
                                           allow_none=False)

isdatetime = lambda thing: isinstance(thing, datetime)
istimedelta = lambda thing: isinstance(thing, timedelta)

@export
class DateTimeField(FieldBase):
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True):
        
        super(BooleanField, self).__init__(default=default,
                                           validator=functional_and(validator,
                                                                    isdatetime),
                                           extractor=extractor,
                                           allow_none=False)

@export
class TimeDeltaField(FieldBase):
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True):
        
        super(BooleanField, self).__init__(default=default,
                                           validator=functional_and(validator,
                                                                    istimedelta),
                                           extractor=extractor,
                                           allow_none=False)

class NamespaceContext(contextlib.AbstractContextManager,
                       metaclass=Slotted):
    
    __slots__ = ('fieldmgr', 'namespace')
    
    def __init__(self, fieldmgr, namespace):
        if not namespace:
            raise ValueError("A truthy namespace declaration is required")
        if not isstring(namespace):
            raise ValueError("A string-type namespace declaration is required")
        self.fieldmgr = weakref.ReferenceType(fieldmgr)
        self.namespace = namespace
    
    def __enter__(self):
        self.fieldmgr().push(namespace=self.namespace)
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.fieldmgr().pop()
        return exc_type is None

def field(method):
    @wraps(method)
    def namespacer(self, *args, **kwargs):
        # cls = globals()[f"{method.__name__}Field"]
        cls = method(self)
        instance = cls(*args, **kwargs)
        instance.namespace = self.namespace
        return instance
    return namespacer

class NamespacedFieldManager(object):
    
    def __init__(self):
        self.namespace_stack = []
    
    def push(self, namespace):
        self.namespace_stack.append(namespace)
    
    def pop(self):
        return self.namespace_stack.pop()
    
    def _clear(self):
        self.namespace_stack = []
    
    def ns(self, namespace):
        return NamespaceContext(self, namespace)
    
    @property
    def namespace(self):
        return NAMESPACE_SEP.join(self.namespace_stack)
    
    def __len__(self):
        return len(self.namespace_stack)
    
    @field
    def Schema(self,        cls,
                            validator=None): return SchemaField
    
    @field
    def String(self,        default=None,
                            validator=None,
                            extractor=None,
                            allow_none=True,
                            min_length=None,
                            max_length=None): return StringField
    
    @field
    def Int(self,           default=None,
                            validator=None,
                            extractor=None,
                            allow_none=True,
                            min_value=None,
                            max_value=None): return IntField
    
    @field
    def UInt(self,          default=None,
                            validator=None,
                            extractor=None,
                            allow_none=True,
                            min_value=None,
                            max_value=None): return UIntField
    
    @field
    def Float(self,         default=None,
                            validator=None,
                            extractor=None,
                            allow_none=True,
                            min_value=None,
                            max_value=None): return FloatField
    
    @field
    def Boolean(self,       default=True,
                            validator=None,
                            extractor=None): return BooleanField
    
    @field
    def DateTime(self,      default=None,
                            validator=None,
                            extractor=None,
                            allow_none=True): return DateTimeField
    
    @field
    def TimeDelta(self,     default=None,
                            validator=None,
                            extractor=None,
                            allow_none=True): return TimeDeltaField

def __getattr__(key):
    """ Module __getattr__(…) instances the NamespacedFieldManager on-demand """
    if key == 'fields':
        if DEBUG:
            print("» Instancing NamespacedFieldManager…")
        return NamespacedFieldManager()
    raise AttributeError(f"module {__name__} has no attribute {key}")

# MODULE EXPORTS:
export(hoist,           name='hoist',       doc="hoist(thing) → if “thing” isn’t already callable, turn it into a lambda that returns it as a value (using “wrap_value(…)”).")
export(isdatetime,      name='isdatetime',  doc="isdatetime(thing) → boolean predicate, True if `thing` is an instance of “datetime.datetime”")
export(istimedelta,     name='istimedelta', doc="istimedelta(thing) → boolean predicate, True if `thing` is an instance of “datetime.timedelta”")

# Assign the modules’ `__all__` using the exporter:
__all__ = exporter.all_tuple('fields')
__dir__ = lambda: list(__all__)
