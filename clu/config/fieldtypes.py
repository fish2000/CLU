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
from clu.predicates import (negate, isclasstype,
                            getpyattr, always, no_op,
                            uncallable, isexpandable, iscontainer,
                            tuplize, slots_for)
from clu.typology import ismapping, isnumber, isstring
from clu.exporting import Slotted, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class ValidationError(Exception):
    """ An error occuring during field validation or configuration. """
    pass

hoist = lambda thing: uncallable(thing) and wrap_value(thing) or thing

@export
class FlatOrderedSet(collections.abc.Set,
                     collections.abc.Sequence,
                     collections.abc.Hashable,
                     metaclass=Slotted):
    
    """ FlatOrderedSet is a structure designed to coalesce any nested
        elements with which it is initialized into a flat, ordered sequence
        devoid of None-values. It has both set and sequence properties –
        membership can be tested as with a set; comparisons can be made with
        less-than and greater-than operators, as with a set; recombinant 
        operations are performed with binary-and and binary-or operators, as
        with a set – but like a sequence, iterating a FlatOrderedSet has a
        stable and deterministic order and items may be retrieved from an
        instance using subscript indexes (e.g. flat_ordered_set[3]). 
        
        Here’s an example of the coalescing behavior:
        
            stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
            summary = FlatOrderedSet("a", "b", "c", "d")
            
            assert stuff == summary
        
        One can optionally specify, as a keyword-only argument, a unary boolean
        function “predicate” that will be used to filter out any of the items
        used to initialize the FlatOrderedSet for which the predicate returns
        a Falsey value. 
    """
    
    __slots__ = tuplize('things')
    
    def __init__(self, *things, predicate=always):
        """ Initialize a new FlatOrderedSet instance with zero or more things.
            
            Optionally, a unary boolean function “predicate” may be specified
            to filter the list of things.
        """
        if uncallable(predicate):
            raise ValueError("FlatOrderedSet requires a callable predicate")
        thinglist = []
        if len(things) == 1:
            if isexpandable(things[0]):
                things = things[0]
            elif iscontainer(things[0]):
                things = tuple(things[0])
        for thing in things:
            if thing is not None:
                if isinstance(thing, type(self)):
                    for other in thing.things:
                        if predicate(other):
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
    
    """ The “functional_and” FlatOrderedSet subclass is designed to hold
        a sequence of functions. Instances of “functional_and” are callable –
        calling “functional_and_instance(thing)” will apply each item held
        by the instance to “thing”, returning True only if the instances’
        functions all return a Truthy value. 
    """
    
    def __init__(self, *functions):
        """ Initialize a “functional_and” callable FlatOrderedSet with a list
            of unary boolean functions.
        """
        super(functional_and, self).__init__(predicate=callable, *functions)
    
    def __call__(self, thing):
        """ Apply each of the functions held by this “functional_and” instance;
            True is returned if all of the functions return a Truthy value –
            otherwise, False is returned.
        """
        return all(function(thing) \
               for function in reversed(self.things) \
                if function is not None)

@export
class functional_set(FlatOrderedSet,
                     collections.abc.Callable):
    
    """ The “functional_set” FlatOrderedSet subclass is designed to hold
        a sequence of functions. Instances of “functional_set” are callable –
        calling “functional_set_instance(thing)” will successively apply
        each function to either “thing” or the return value of the previous
        function – finally returning the last return value when the sequence
        of functions has been exhausted.
    """
    
    def __init__(self, *functions):
        """ Initialize a “functional_and” callable FlatOrderedSet with a list
            of functions accepting a “thing” and returning something like it.
        """
        super(functional_set, self).__init__(predicate=callable, *functions)
    
    def __call__(self, thing):
        """ Apply each of the functions held by this “functional_and” instance
            successively to “thing”, replacing “thing” with the return value of
            each function in turn, and finally returning the last return value
            once the sequence of functions has been exhausted.
        """
        for function in reversed(self.things):
            if function is not None:
                thing = function(thing)
        return thing

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
        
        … you should be good to go†.
        
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
        return stringify(self, slots_for(type(self)))

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

isdatetime = lambda thing: isinstance(thing, datetime)
istimedelta = lambda thing: isinstance(thing, timedelta)

@export
class DateTimeField(FieldBase):
    
    def __init__(self, default=None,
                       validator=None,
                       extractor=None,
                       allow_none=True):
        
        """ Initialize a DateTimeField – used to hold instances of “datetime.datetime”. """
        
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
        
        """ Initialize a TimeDeltaField – used to hold instances of “datetime.timedelta”. """
        
        super(BooleanField, self).__init__(default=default,
                                           validator=functional_and(validator,
                                                                    istimedelta),
                                           extractor=extractor,
                                           allow_none=False)

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
    
    def push(self, namespace):
        """ Push a namespace onto the stack. """
        self.namespace_stack.append(namespace)
    
    def pop(self):
        """ Remove the uppermost namespace from the stack. """
        return self.namespace_stack.pop()
    
    def _clear(self):
        """ Reset the namespace stack to a pristine empty list. """
        self.namespace_stack = []
    
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

def test():
    from pprint import pprint
    from clu.config.base import Nested
    import os
    
    yodogg_file = '/tmp/yodogg.txt'
    
    class SampleContext(object):
        
        with open(yodogg_file, 'w') as write_handle:
            write_handle.write("Yo dogg.")
            write_handle.flush()
        
        with open(yodogg_file, 'r') as read_handle:
            contextualized = read_handle.read()
    
    sampctx = SampleContext()
    print("» SAMPLE:")
    print(sampctx.contextualized)
    print()
    
    os.unlink(yodogg_file)
    
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
    
    

if __name__ == '__main__':
    test()