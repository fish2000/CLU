# -*- coding: utf-8 -*-
from __future__ import print_function
from reprlib import recursive_repr

import abc
import contextlib
import collections.abc
import os

abstract = abc.abstractmethod
recursive = recursive_repr(fillvalue="…")

from clu.constants import consts

class Slotted(abc.ABCMeta):
    
    """ A metaclass that ensures its classes, and all subclasses,
        will be slotted types.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Override for `abc.ABCMeta.__new__(…)` setting up a
            derived slotted class.
        """
        if '__slots__' not in attributes:
            attributes['__slots__'] = tuple()
        
        return super().__new__(metacls, name, # type: ignore
                                        bases,
                                        attributes,
                                      **kwargs)

class SlotMatch(Slotted):
    
    """ A metaclass that ensures its classes, and all subclasses,
        will be slotted types with “__match_args__” set to the
        sum of the “__slots__” values for this and all ancestors.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Override for `abc.ABCMeta.__new__(…)` setting up a
            derived slotted class with “__match_args__” set.
        """
        from clu.predicates import slots_for
        
        # Ensure the new class will have a “__match_args__” attribute
        if '__match_args__' not in attributes:
            attributes['__match_args__'] = tuple()
        
        # Create the new class via “super(…)” – calling “Slotted.__new__(…)”
        cls = super().__new__(metacls, name, # type: ignore
                                       bases,
                                       attributes,
                                     **kwargs)
        
        # Set “__match_args__” using “slots_for(…)” and return
        cls.__match_args__ = slots_for(cls)
        return cls

class NonSlotted(abc.ABCMeta):
    
    """ A metaclass that ensures its classes, and all subclasses,
        will •not• use the “__slots__” optimization.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Override for `abc.ABCMeta.__new__(…)` setting up a
            derived un-slotted class.
        """
        if '__slots__' in attributes:
            attributes.pop('__slots__')
        
        return super().__new__(metacls, name,
                                        bases,
                                        attributes,
                                      **kwargs)

class UnhashableMeta(Slotted):
    
    """ A slotted metaclass that ensures its classes, and all
        subclasses, will *not* be hashable types.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Override for `abc.ABCMeta.__new__(…)` setting up a
            derived slotted un-hashable class.
        """
        if '__hash__' in attributes:
            attributes.pop('__hash__')
        attributes['__hash__'] = None
        
        return super().__new__(metacls, name,
                                        bases,
                                        attributes,
                                      **kwargs)

class Unhashable(abc.ABC, metaclass=UnhashableMeta):
    
    __slots__ = tuple()
    
    @classmethod
    def __subclasshook__(cls, subcls):
        if cls is Unhashable:
            return getattr(subcls, '__hash__', None) is None
        return NotImplemented

class Appreciative(abc.ABC):
    
    """ An abstract class representing a type that “appreciates”
        an instance. But what?? you may ask. What is this – WHAT
        DOES IT MEAN?!? It means that the class has a class method
        called “appreciates.” This takes an instance of… something,
        and returns a boolean.
        
        A class usually “appreciates” an instance if that instance
        is of that class, or one like it. It can be for any reason,
        but any ABCs or other CLU stuff based on the `Appreciative`
        class will assume that classes will appreciate… something
        like that. OK? OK.
    """
    __slots__ = tuple()
    
    @classmethod
    @abstract
    def appreciates(cls, instance):
        """ Boolean, tests if the class “appreciates” an instance """
        ...
    
    @classmethod
    def __subclasshook__(cls, subcls):
        appreciates = getattr(subcls, 'appreciates', None)
        return callable(appreciates)

class Format(collections.abc.Callable, metaclass=Slotted):
    
    """ An abstract class representing something that formats something
        else. It only offers the one abstract method, “render(…)” at
        this time.
    """
    __slots__ = tuple()
    
    @abstract
    def render(self, string):
        """ Render a string with respect to the Format instance. """
        ...
    
    def __call__(self, string):
        return self.render(string)

class NonFormat(Format):
    
    """ A “format” type whose “render(…)” method is a no-op. """
    __slots__ = tuple()
    
    def __init__(self, *args):
        pass
    
    def render(self, string):
        """ Return a string, unchanged """
        return str(string)

class SlottedFormat(Format):
    
    """ A base format type, with a slot for a format-operation string. """
    __slots__ = 'opstring'

class Sanitizer(Format):
    
    """ A base format type, with a slot for a compiled regular expression. """
    __slots__ = 'regex'
    
    def render(self, string):
        return self.regex.sub('', string)

class Serializable(abc.ABC):
    
    """ An abstract class for something “serializable” – furnishing two
        functions. A “from_dict(…)” class method takes a standard dict,
        and returns a corresponding instance of the serializable class.
        
        The “to_dict(…)” instance method, by contrast, takes no arguments
        and returns a plain dict based on the instance of the serializable
        class. This dict is based on the class, and contains whatever the
       “from_dict(…)” method expects.
    """
    __slots__ = tuple()
    
    @classmethod
    def from_dict(cls, instance_dict):
        """ Returns an instance, per the plain dict passed """
        ...
    
    def to_dict(self):
        """ Returns a plain dict, representing the instance """
        ...

class Cloneable(abc.ABC):
    
    """ An abstract class representing something “clonable.” A cloneable
        subclass need only implement the one method, “clone()” – taking no
        arguments and returning a new instance of said class, populated
        as a cloned copy of the instance upon which the “clone()” method
        was called.
        
        Implementors are at liberty to use shallow- or deep-copy methods,
        or a mixture of the two, in creating these cloned instances.
    """
    __slots__ = tuple()
    
    @abstract
    def clone(self, deep=False, memo=None):
        """ Return a cloned copy of this instance """
        ...
    
    def __copy__(self):
        """ Return a shallow copy of this instance """
        return self.clone()
    
    def __deepcopy__(self, memo):
        """ Return a deep copy of this instance """
        return self.clone(deep=True, memo=memo)

class ReprWrapper(abc.ABC):
    
    """ ReprWrapper fills in a default template for __repr__ results,
        based on a standard display including the type name and the
        hex ID of the instance:
        
            TypeName( ••• ) @ 0xDEADBEEF
        
        … The “ ••• ” string gets filled in by a new abstract method,
        “inner_repr()”, which subclasses must provide. This new method
        takes no arguments and should return a string.
        
        Example 1: Return the repr of a relevant sub-instance value:
        
            FlatOrderedSet(('a', 'b', 'c', 'd')) @ 0x115299650
        
        … Note that the parenthesized value is the repr of an internal
        tuple value. The “inner_repr()” method returns something like
        “repr(self.internal_tuple)”.
        
        Example 2: Return some interesting meta-information:
        
            Env([prefix=“CLU_*”, namespaces=4, keys=13]) @ 0x115373690
        
        … Here the return value of “inner_repr()” is composed freely,
        like any other repr-string, instead of delegated wholesale to
        another objects repr value. 
    """
    __slots__ = tuple()
    
    @abstract
    def inner_repr(self):
        """ Return a repr string for instances of this class """
        ...
    
    @recursive
    def __repr__(self):
        """ This classes’ object instances’ unique string representation """
        from clu.repr import fullrepr
        return fullrepr(self, self.inner_repr())

class SlottedRepr(ReprWrapper, metaclass=Slotted):
    
    """ A simple, default version of a ReprWrapper class that uses its
        inheritance chain’s value for “__slots__” to build the repr
        string for its instances
    """
    __slots__ = tuple()
    
    def inner_repr(self):
        """ Use the union of __slots__, defined across this classes’
            inheritance chain, to build the instances’ repr string
        """
        from clu.predicates import slots_for
        from clu.repr import strfields
        return strfields(self,
               slots_for(type(self)),
                         try_callables=False)

class MappingViewRepr(ReprWrapper):
    
    """ A ReprWrapper class that simply returns the repr for a
        “self._mapping” value – of which most MappingView types make use.
    """
    __slots__ = tuple()
    
    def inner_repr(self): # pragma: no cover
        """ Return the repr string for “self._mapping” """
        return repr(self._mapping)

evict_announcer = lambda key, value: print(f"Cache dropped: {key}") # pragma: no cover

class BaseDescriptor(abc.ABC):
    
    __slots__ = tuple()
    
    @abstract
    def __get__(self, instance, cls=None):
        ...

class DataDescriptor(BaseDescriptor):
    
    __slots__ = tuple()
    
    @abstract
    def __set__(self, instance, value):
        ...
    
    def __delete__(self, instance):
        pass

class NamedDescriptor(DataDescriptor):
    
    __slots__ = tuple()
    
    @abstract
    def __set_name__(self, cls, name):
        ...

class CacheDescriptor(DataDescriptor, ReprWrapper):
    
    __slots__ = ('cache', 'lru')
    
    def __init__(self):
        import zict
        
        self.cache = {}
        self.lru = zict.LRU(18, self.cache,
                                on_evict=(consts.DEBUG \
                                      and evict_announcer \
                                       or None))
    
    def __get__(self, *args):
        return self.lru
    
    def __set__(self, instance, value):
        self.lru = value
    
    def inner_repr(self): # pragma: no cover
        return repr(self.lru)[1:-1]

class Descriptor(NamedDescriptor, SlottedRepr):
    
    """ A simple, generic desciptor, wrapping one value, and storing its name """
    
    __slots__ = ('name', 'value')
    
    def __init__(self, value, name=None):
        self.name = name or "«unknown»"
        self.value = value
    
    def __set_name__(self, cls, name):
        self.name = name
    
    def __get__(self, *args):
        return self.value
    
    def __set__(self, instance, value):
        if value != self.value:
            raise ValueError("cannot alter {self.name} value")
    
    def alternative_inner_repr(self): # pragma: no cover
        from clu.repr import strfield
        value = strfield(self.value)
        return f"name={self.name}, value={value}"

class ValueDescriptor(Descriptor):
    
    """ A descriptor whose repr-string tries to be a literal reflection
        of its wrapped value
    """
    __slots__ = tuple()
    
    def __repr__(self):
        """ A custom repr for the ValueDescriptor’s literal value """
        return isinstance(self.value, str)   and self.value or \
               isinstance(self.value, bytes) and self.value.decode(consts.ENCODING) or \
                                            repr(self.value)

class BasePath(Slotted):
    
    """ A metaclass to assign a “basepath” class property,
        extracted from a “basepath” class keyword, to a new
        slotted type. 
    """
    
    @classmethod
    def __prepare__(metacls, name, bases, basepath="/", **kwargs):
        """ Remove the “basepath” class keyword before calling up """
        return super().__prepare__(name, bases, **kwargs)
    
    def __new__(metacls, name, bases, attributes, basepath="/", **kwargs):
        """ Override for `Slotted.__new__(…)` setting up a
            derived slotted class that pulls from a “basepath”
            with the requisite methods defined for access.
        """
        if 'basepath' not in attributes:
            attributes['basepath'] = ValueDescriptor(basepath  \
                                       and os.fspath(basepath) \
                                                  or basepath)
        
        return super().__new__(metacls, name,
                                        bases,
                                        attributes,
                                      **kwargs)

class AppName(abc.ABC):
    
    __slots__ = tuple()
    
    @classmethod
    def __init_subclass__(cls, appname=None, **kwargs):
        """ Translate the “appname” class-keyword into an “appname” read-only
            descriptor value
        """
        from clu.predicates import mro, attr_search
        if 'appspace' in kwargs:
            del kwargs['appspace']
        super().__init_subclass__(**kwargs)
        cls.appname = ValueDescriptor(appname or attr_search('appname', *mro(cls)))
    
    def __init__(self, *args, **kwargs):
        """ Stub __init__(…) method, throwing a lookup error for subclasses
            upon which the “appname” value is None
        """
        if type(self).appname is None:
            raise LookupError("Cannot instantiate a base config class "
                              "(appname is None)")

class ManagedContext(contextlib.AbstractContextManager):
    
    __slots__ = tuple()
    
    @abstract
    def setup(self):
        ...
    
    @abstract
    def teardown(self):
        ...
    
    def __enter__(self):
        return self.setup()
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        self.teardown()
        return exc_type is None

__all__ = ('Slotted', 'SlotMatch', 'NonSlotted',
           'UnhashableMeta', 'Unhashable',
           'Appreciative',
           'Format', 'NonFormat', 'SlottedFormat', 'Sanitizer',
           'Serializable', 'Cloneable',
           'ReprWrapper', 'SlottedRepr', 'MappingViewRepr',
           'evict_announcer',
           'BaseDescriptor', 'DataDescriptor', 'NamedDescriptor',
           'CacheDescriptor', 'Descriptor', 'ValueDescriptor',
           'BasePath', 'AppName',
           'ManagedContext')

__dir__ = lambda: list(__all__)
