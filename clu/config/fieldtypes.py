# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime, timedelta
from functools import wraps

import abc
import collections.abc
import contextlib
import os
import weakref

from clu.constants.consts import NoDefault
from clu.constants.polyfills import Path
from clu.abstract import Slotted
from clu.config.abc import NAMESPACE_SEP, functional_and, functional_set
from clu.naming import nameof
from clu.predicates import (negate, isclasstype,
                            getpyattr, always, no_op, attr,
                            uncallable, hoist, tuplize, slots_for)
from clu.repr import stringify
from clu.typology import (isderivative, ismapping,
                                        isnumber,
                                        isstring, ispath, isvalidpath)
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class ValidationError(Exception):
    """ An error occuring during field validation or configuration. """
    pass

@export
class FieldBase(abc.ABC, metaclass=Slotted):
    
    """ FieldBase is the base ancestor for all field descriptor classes.
        
        Each descriptor in the “clu.config” package has:
            
            • A name, and an optional namespace;
            • An optional default value, corresponding to the field’s type;
            • An optional validator function (in addition to any validators
              the field requires internally);
            • An optional extractor function, which transforms any incoming
              values (in addition to any extractors the field requires
              internally);
            • A boolean flag indicating whether “None” is a legal value for
              instances of the field.
        
        The field’s name is set via the “__set_name__(…)” special function that
        Python 3.6 introduced – this function is manually called by the metaclass
        employed by “clu.config.settings.Schema”; if you are interested in using
        these field descriptors anywhere outside of defining schemas with the CLU
        Schema class, and you want your stuff to work on older Pythons, that’s on
        you doggie†.
        
        The field’s namespace is set when a field is defined via the pseudo-module
        “clu.config.fieldtypes.fields” – if you import this pseudo-module by doing:
        
            >>> from clu.config.fieldtypes import fields
        
        … you should be good to go‡.
        
        Validator functions, if provided, should be of the arity:
        
            def validator(value: FieldType) -> Bool: ...
        
        Whereas extractor functions should be of the arity:
        
            def extractor(value: FieldType) -> FieldType: ...
        
        Note that, at this time, none of our config-schema or field-descriptor code
        has been actually annotated – but that’s how it should work, dogg. Yes.
        
        † – These descriptors can work without the Schema backing class – but they
            do expect their owning classes’ instances to furnish a “__fields__”
            attribute of type “clu.config.base.NamespacedMutableMapping”.
        
        ‡ – N.B. For the curious, what I am calling a “pseudo-module” here isn’t a
            module at all; it is an instance of a private “NamespacedFieldManager”
            class that manages the statefulness necessary to implement namespacing
            using context-management. When you import it using the “from” import
            statement above, a module-level “__getattr__(…)” function instances the
            class and returns it anew each time. 
    """
    
    __slots__ = ('name', 'namespace',
                         'default',
                         'validator',
                         'extractor',
                         'allow_none')
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True):
        """ FieldBase __init__(…): initialize common underlying attributes:
            
            • A name, and an optional namespace;
            • An optional default value, corresponding to the field’s type;
            • An optional validator function (in addition to any validators
              the field requires internally);
            • An optional extractor function, which transforms any incoming
              values (in addition to any extractors the field requires
              internally);
            • A boolean flag indicating whether “None” is a legal value for
              instances of the field.
        """
        
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
    
    def get_default(self):
        """ Ensure our default value is callable – and then call it: """
        return hoist(self.default)()
    
    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return getpyattr(instance, 'fields').get(attr(self, 'name', 'namespace'),
                                            namespace=self.namespace,
                                              default=self.default or NoDefault)
    
    def __set__(self, instance, value):
        # Check for outlawed Nones:
        if value is None:
            if not self.allow_none:
                raise ValidationError(f"Field “{self.name}” does not allow None values")
        
        # Do extraction and validation:
        try:
            if value is not None:
                value = self.extractor(value)
        except (TypeError, ValueError, ValidationError) as exc:
            raise ValidationError(f"Extraction failue in “{self.name}”: {exc}")
        
        if not (value is None and self.allow_none):
            if not self.validator(value):
                raise ValidationError(f"Validation failue in “{self.name}”: {self.validator!r}")
        
        # Set and return:
        getpyattr(instance, 'fields').set(self.name, value,
                                namespace=self.namespace)
        return value
    
    def __delete__(self, instance):
        getpyattr(instance, 'fields').delete(self.name,
                                   namespace=self.namespace)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return stringify(self,
               slots_for(self),
               try_callables=False)
    
    def __json__(self, **kwargs):
        instance = kwargs.get('instance')
        return self.__get__(instance, cls=None)

predicate_for = lambda cls: lambda thing: isderivative(thing, cls)

@export
class SchemaField(FieldBase):
    
    def __init__(self, cls, validator=None):
        """ Initialize a SchemaField – a reference from one Schema definition
            to another.
            
            This is like the Django ORM’s ForeignKey field (or, more precisely,
            like a GenericForeignKey, as it can point at whatever, as long as
            it’s a Schema-backed fieldset).
        """
        self.cls = cls
        super(SchemaField, self).__init__(default=cls,
                                          validator=functional_and(validator,
                                                                   predicate_for(cls),
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
        
        """ Initialize a StringField – used to hold instances of Python strings.
            
            In addition to the standard parameters furnished by the FieldBase
            ancestor class, there two additional parameters:
                
                • max_length, and
                • min_length
            
            … each of which is expected to be a positive integer value if not None.
            Specifying either or both of these allows the size of the string instance
            to be bounded.
        """
        
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
        if isstring(out):
            if self.min_length is not None:
                if len(out) < self.min_length:
                    raise ValidationError(f"Validation failure in {nameof(type(self))}: len(string) < min_length")
            if self.max_length is not None:
                if len(out) <= self.max_length:
                    raise ValidationError(f"Validation failure in {nameof(type(self))}: len(string) > max_length")
        return out

@export
class PathField(StringField):
    
    __slots__ = tuplize('requisite')
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True,
                       requisite=False,
                       min_length=None,
                       max_length=None):
        
        """ Initialize a PathField – used to hold objects representing filesystem paths. """
        
        if requisite:
            allow_none = False
        
        super(PathField, self).__init__(default=default,
                                        validator=functional_and(validator,
                                                                 requisite and isvalidpath or ispath),
                                        extractor=functional_set(extractor, os.fspath),
                                        allow_none=allow_none,
                                        min_length=min_length,
                                        max_length=max_length)
        
        self.requisite = requisite
    
    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        out = super(PathField, self).__get__(instance, cls)
        return out and Path(out) or None

@export
class IntField(FieldBase):
    
    __slots__ = ('min_value', 'max_value')
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True,
                       min_value=None,
                       max_value=None):
        
        """ Initialize an IntField – used to hold instances of Python integers.
            
            In addition to the standard parameters furnished by the FieldBase
            ancestor class, there two additional parameters:
                
                • max_value, and
                • min_value
            
            … each of which is expected to be an integer value if not None.
            Specifying either or both of these allows the value of the integer instance
            to be bounded.
        """
        
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
        
        """ Initialize an UIntField – used to hold “unsigned”, or positive, instances
            of Python integers.
            
            Since Python doesn’t have a built-in “unsigned int” type, UIntField is a
            subclass of IntField, with additional bounds-checking validation added.
            
            In addition to the standard parameters furnished by the FieldBase
            ancestor class, there two additional parameters:
                
                • max_value, and
                • min_value
            
            … each of which is expected to be an integer value if not None.
            Specifying either or both of these allows the value of the unsigned integer
            instance to be bounded.
        """
        
        if max_value is not None:
            if max_value < 0:
                raise ValidationError("max_value must be positive for {nameof(type(self))} fields")
        
        super(UIntField, self).__init__(default=default or 0,
                                        validator=functional_and(validator,
                                                                 lambda thing: thing >= 0),
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
        
        """ Initialize an FloatField – used to hold instances of Python floating-point
            numbers.
            
            In addition to the standard parameters furnished by the FieldBase
            ancestor class, there two additional parameters:
                
                • max_value, and
                • min_value
            
            … each of which is expected to be an floating-point value if not None.
            Specifying either or both of these allows the value of the float instance
            to be bounded.
        """
        
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
        
        """ Initialize an BooleanField – used to hold instances of Python boolean values.
            
            This field cannot be None by definition. That would be confusing – having
            BooleanFields holding either True or False in some cases, but in other cases
            holding True, False or None – one Truthy value and two Falsey but distinct
            values… so no, fuck that. No Nones!
        """
        
        super(BooleanField, self).__init__(default=default,
                                           validator=validator,
                                           extractor=functional_set(extractor, bool),
                                           allow_none=False)

isdatetime = predicate_for(datetime)
istimedelta = predicate_for(timedelta)

@export
class DateTimeField(FieldBase):
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None):
        
        """ Initialize a DateTimeField – used to hold instances of “datetime.datetime”. """
        
        super(DateTimeField, self).__init__(default=default,
                                            validator=functional_and(validator,
                                                                     isdatetime),
                                            extractor=extractor,
                                            allow_none=False)

@export
class TimeDeltaField(FieldBase):
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None):
        
        """ Initialize a TimeDeltaField – used to hold instances of “datetime.timedelta”. """
        
        super(TimeDeltaField, self).__init__(default=default,
                                             validator=functional_and(validator,
                                                                      istimedelta),
                                             extractor=extractor,
                                             allow_none=False)

optional = lambda abcls: (lambda thing: isinstance(thing, abcls) or (thing is None))

maybemapping    = optional(collections.abc.Mapping)
maybesequence   = optional(collections.abc.Sequence)
maybeset        = optional(collections.abc.Set)
maybefieldbase  = optional(FieldBase)

@export
class ListField(FieldBase):
    
    __slots__ = tuplize('value')
    
    def __init__(self, default=list,
                       value=None,
                       validator=None,
                       extractor=None):
        
        super(ListField, self).__init__(default=default,
                                        validator=functional_and(validator,
                                                                 maybesequence),
                                        extractor=extractor,
                                        allow_none=False)
        
        if not maybefieldbase(value):
            raise TypeError(f'value must be either None or derived from FieldBase (not {value})')
        
        self.value = value
        self.value.__set_name__(None, 'interstitial')
    
    def __set__(self, instance, value):
        from clu.config.settings import Schema
        
        if value is None:
            value = self.get_default()
        
        if self.value is not None:
            newvalue = list()
            schema = Schema()
            for thing in value:
                try:
                    thing = self.value.__set__(schema, thing)
                except ValidationError as exc:
                    raise ValidationError(f'Validation failure in {self.name}: {exc}')
                newvalue.append(thing)
            value = newvalue
        
        return super(ListField, self).__set__(instance, value)

@export
class TupleField(FieldBase):
    
    __slots__ = tuplize('value')
    
    def __init__(self, default=tuple,
                       value=None,
                       validator=None,
                       extractor=None):
        
        super(TupleField, self).__init__(default=default,
                                         validator=functional_and(validator,
                                                                  maybesequence),
                                         extractor=extractor,
                                         allow_none=False)
        
        if not maybefieldbase(value):
            raise TypeError(f'value must be either None or derived from FieldBase (not {value})')
        
        self.value = value
        self.value.__set_name__(None, 'interstitial')
    
    def __set__(self, instance, value):
        from clu.config.settings import Schema
        
        if value is None:
            value = self.get_default()
        
        if self.value is not None:
            newvalue = tuple()
            schema = Schema()
            for thing in value:
                try:
                    thing = self.value.__set__(schema, thing)
                except ValidationError as exc:
                    raise ValidationError(f'Validation failure in {self.name}: {exc}')
                newvalue += tuplize(thing)
            value = tuple(newvalue)
        
        return super(TupleField, self).__set__(instance, value)

@export
class SetField(FieldBase):
    
    __slots__ = tuplize('value')
    
    def __init__(self, default=set,
                       value=None,
                       validator=None,
                       extractor=None):
        
        super(SetField, self).__init__(default=default,
                                       validator=functional_and(validator,
                                                                maybeset),
                                       extractor=extractor,
                                       allow_none=False)
        
        if not maybefieldbase(value):
            raise TypeError(f'value must be either None or derived from FieldBase (not {value})')
        
        self.value = value
        self.value.__set_name__(None, 'interstitial')
    
    def __set__(self, instance, value):
        from clu.config.settings import Schema
        
        if value is None:
            value = self.get_default()
        
        if self.value is not None:
            newvalue = set()
            schema = Schema()
            for thing in value:
                try:
                    thing = self.value.__set__(schema, thing)
                except ValidationError as exc:
                    raise ValidationError(f'Validation failure in {self.name}: {exc}')
                newvalue.add(thing)
            value = newvalue
        
        return super(SetField, self).__set__(instance, value)

@export
class FrozenSetField(FieldBase):
    
    __slots__ = tuplize('value')
    
    def __init__(self, default=frozenset,
                       value=None,
                       validator=None,
                       extractor=None):
        
        super(FrozenSetField, self).__init__(default=default,
                                             validator=functional_and(validator,
                                                                      maybeset),
                                             extractor=extractor,
                                             allow_none=False)
        
        if not maybefieldbase(value):
            raise TypeError(f'value must be either None or derived from FieldBase (not {value})')
        
        self.value = value
        self.value.__set_name__(None, 'interstitial')
    
    def __set__(self, instance, value):
        from clu.config.settings import Schema
        
        if value is None:
            value = self.get_default()
        
        if self.value is not None:
            newvalue = set()
            schema = Schema()
            for thing in value:
                try:
                    thing = self.value.__set__(schema, thing)
                except ValidationError as exc:
                    raise ValidationError(f'Validation failure in {self.name}: {exc}')
                newvalue.add(thing)
            value = frozenset(newvalue)
        
        return super(FrozenSetField, self).__set__(instance, value)

@export
class DictField(FieldBase):
    
    __slots__ = tuplize('value')
    
    def __init__(self, default=dict,
                       key=None,
                       value=None,
                       validator=None,
                       extractor=None):
        
        super(DictField, self).__init__(default=default,
                                        validator=functional_and(validator,
                                                                 maybemapping),
                                        extractor=extractor,
                                        allow_none=False)
        
        if not maybefieldbase(key):
            raise TypeError(f'key must be either None or derived from FieldBase (not {value})')
        
        self.key = key
        self.key.__set_name__(None, 'interstitial_key')
        
        if not maybefieldbase(value):
            raise TypeError(f'value must be either None or derived from FieldBase (not {value})')
        
        self.value = value
        self.value.__set_name__(None, 'interstitial_value')
    
    def __set__(self, instance, value):
        from clu.config.settings import Schema
        
        if value is None:
            value = self.get_default()
        
        newvalue = {}
        schema = Schema()
        for k, v in value.items():
            if self.key is not None:
                try:
                    k = self.key.__set__(schema, k)
                except ValidationError as exc:
                    raise ValidationError(f'Validation failure in {self.name} [key]: {exc}')
            if self.value is not None:
                try:
                    v = self.value.__set__(schema, v)
                except ValidationError as exc:
                    raise ValidationError(f'Validation failure in {self.name} [value]: {exc}')
            newvalue[k] = v
        return super(DictField, self).__set__(instance, newvalue)

class NamespaceContext(contextlib.AbstractContextManager,
                       metaclass=Slotted):
    
    """ NamespaceContext is a private context-manager proxy class, employed by the
        NamespacedFieldManager pseudo-module class to perform the actual context
        switches necessary to record namespaces used during field definition.
    """
    
    __slots__ = ('fieldmgr', 'namespace')
    
    def __init__(self, fieldmgr, namespace):
        """ Initialize a NamespaceContext for a given NamespacedFieldManager instance.
            
            The NamespacedFieldManager instance is stored via a “weakref.ReferenceType”
            instance, forgoing hard (and potentially circular) references. The namespace
            argument must be passed as a string type.
        """
        if not fieldmgr:
            raise ValueError("A truthy fieldmanager instance is required")
        if not namespace:
            raise ValueError("A truthy namespace declaration is required")
        if not isstring(namespace):
            raise ValueError("A string namespace declaration is required")
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
        instance = method(self)(*args, **kwargs)
        instance.namespace = self.namespace
        return instance
    return namespacer

class NamespacedFieldManager(object):
    
    """ The class defining the stateful pseudo-module access point for namespaced
        Schema-backed field definitions.
        
        This class should not be imported or instanced directly by users. Instead,
        by importing the pseudo-module “clu.config.fieldtypes.fields” like e.g.:
        
            >>> from clu.config.fieldtypes import fields
        
        … the module-level “__getattr__(…)” hook in “fieldtypes” will freshly create
        a new instance of “NamespacedFieldManager” each time this import statement is
        executed. This will ensure the stateful namespace-related bookkeeping mechanism
        furnished by “NamespacedFieldManager” instances will always work properly for
        your schema definitions.
    """
    
    def __init__(self):
        """ Initialize a new “NamespacedFieldManager” instance.
        
            No parameters are accepted.
        """
        self.namespace_stack = []
        self.__qualname__ = self.__name__ = 'fields'
        self.__file__ = __file__
    
    def push(self, namespace):
        """ Push a namespace onto the stack. """
        self.namespace_stack.append(namespace)
    
    def pop(self):
        """ Remove the uppermost namespace from the stack. """
        return self.namespace_stack.pop()
    
    def _clear(self):
        """ Reset the namespace stack to a pristine list, returning the previous value. """
        out = self.namespace_stack
        self.namespace_stack = []
        return out
    
    def ns(self, namespace):
        """ The context-management wrapper method for creating a new namespace.
            
            To create a new namespace during a schema class definition, use:
                
                with fields.ns('namespace_name'):
                    […]
        """
        return NamespaceContext(self, namespace)
    
    @property
    def namespace(self):
        """ The current namespace stack, expressed as a string.
            
            Q.v. “clu.config.base.NamespacedMutableMapping” definition supra.
        """
        return NAMESPACE_SEP.join(self.namespace_stack) or None
    
    def __len__(self):
        return len(self.namespace_stack)
    
    def __iter__(self):
        # TODO: make this iterate over the currently defined field instances:
        yield from self.namespace_stack
    
    def __repr__(self):
        return f"<pseudo-module '{self.__module__}.{self.__name__}' from '{self.__file__}' " \
               f"[{self.__module__}.{self.__class__.__name__} instance @ {hex(id(self))}]>"
    
    def __bool__(self):
        return True
    
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
    def Path(self,          default=None,
                            validator=None,
                            extractor=None,
                            allow_none=True,
                            requisite=False,
                            min_length=None,
                            max_length=None): return PathField
    
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
                            extractor=None): return DateTimeField
    
    @field
    def TimeDelta(self,     default=None,
                            validator=None,
                            extractor=None): return TimeDeltaField
    
    @field
    def List(self,          value=None,
                            validator=None,
                            extractor=None): return ListField
    
    @field
    def Tuple(self,         value=None,
                            validator=None,
                            extractor=None): return TupleField
    
    @field
    def Set(self,           value=None,
                            validator=None,
                            extractor=None): return SetField
    
    @field
    def FrozenSet(self,     value=None,
                            validator=None,
                            extractor=None): return FrozenSetField
    
    @field
    def Dict(self,          key=None,
                            value=None,
                            validator=None,
                            extractor=None): return DictField

def __getattr__(key):
    """ Module __getattr__(…) instances the NamespacedFieldManager on-demand """
    if key == 'fields':
        return NamespacedFieldManager()
    raise AttributeError(f"module {__name__} has no attribute {key}")

# MODULE EXPORTS:
export(predicate_for,   name='predicate_for',   doc="predicate_for(cls) → a predicate factory, returning a new predicate function that returns True for instances of “cls”")
export(isdatetime,      name='isdatetime',      doc="isdatetime(thing) → boolean predicate, True if `thing` is an instance of “datetime.datetime”")
export(istimedelta,     name='istimedelta',     doc="istimedelta(thing) → boolean predicate, True if `thing` is an instance of “datetime.timedelta”")

export(optional,        name='optional',        doc="optional(cls) → Returns a new “maybe” boolean predicate, which will return True if passed either None or an instance of “cls”")
export(maybemapping,    name='maybemapping',    doc="maybemapping(thing) → “maybe” boolean predicate, returning True for either None or an instance of “collections.abc.Mapping”")
export(maybesequence,   name='maybesequence',   doc="maybesequence(thing) → “maybe” boolean predicate, returning True for either None or an instance of “collections.abc.Sequence”")
export(maybeset,        name='maybeset',        doc="maybeset(thing) → “maybe” boolean predicate, returning True for either None or an instance of “collections.abc.Set”")
export(maybefieldbase,  name='maybefieldbase',  doc="maybefieldbase(thing) → “maybe” boolean predicate, returning True for either None or an instance of “clu.config.fieldtypes.FieldBase”")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir('fields')

def test():
    
    from clu.testing.utils import inline
    from clu.config.base import Nested
    from pprint import pprint
    import os
    
    @inline
    def test_one():
        """ Proof-of-concept class/with-statement checks """
        
        yodogg_file = '/tmp/yodogg.txt'
        
        class SampleContext(object):
            
            with open(yodogg_file, 'w') as write_handle:
                write_handle.write("Yo dogg.")
                write_handle.flush()
            
            with open(yodogg_file, 'r') as read_handle:
                contextualized = read_handle.read()
        
        try:
            sampctx = SampleContext()
            print("» SAMPLE:")
            print(sampctx.contextualized)
            print()
        
        finally:
            os.unlink(yodogg_file)
    
    @inline
    def test_two():
        """ NamespacedFieldManager context-management check """
        
        fields = NamespacedFieldManager()
        
        class Context(object):
            
            __fields__ = Nested()
            
            yo = fields.String("«yo»")
            dogg = fields.String("«yo»")
            
            print("NAMESPACE [0]:", fields.namespace)
            
            with fields.ns("iheard"):
                
                yodogg = fields.String()
                youlike = fields.String()
                
                print("NAMESPACE [1]:", fields.namespace)
            
            print("NAMESPACE [0]:", fields.namespace)
            
            with fields.ns("so"):
                
                weput = fields.Int(0)
                some = fields.UInt(0)
                
                print("NAMESPACE [1]:", fields.namespace)
            
            print("NAMESPACE [0]:", fields.namespace)
        
        ctx = Context()
        
        print("» CONTEXTUALIZED:")
        pprint(ctx.__fields__)
        print()
    
    # Run all tests:
    inline.test(100)

if __name__ == '__main__':
    test()