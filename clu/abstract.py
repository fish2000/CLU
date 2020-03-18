# -*- coding: utf-8 -*-
from __future__ import print_function
from reprlib import recursive_repr

import abc
import contextlib
import collections.abc

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
        
        return super(Slotted, metacls).__new__(metacls, name, # type: ignore
                                                        bases,
                                                        attributes,
                                                      **kwargs)

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
        
        return super(NonSlotted, metacls).__new__(metacls, name,
                                                           bases,
                                                           attributes,
                                                         **kwargs)

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
        from clu.repr import typename_hexid
        cnm, hxa = typename_hexid(self)
        rpr = self.inner_repr()
        return f"{cnm}({rpr}) {consts.REPR_DELIMITER} {hxa}"

class SlottedRepr(ReprWrapper, metaclass=Slotted):
    
    """ A simple, default version of a ReprWrapper class that uses its
        inheritance chain’s value for “__slots__” to build the repr
        string for its instances
    """
    
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
    
    def inner_repr(self):
        """ Return the repr string for “self._mapping” """
        return repr(self._mapping)

evict_announcer = lambda key, value: print(f"Cache dropped: {key}")

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
        # raise NotImplementedError("DataDescriptor.__delete__()")
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
    
    def inner_repr(self):
        return repr(self.lru)

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
    
    def alternative_inner_repr(self):
        from clu.repr import strfield
        value = strfield(self.value)
        return f"[name={self.name}, value={value}]"

class ValueDescriptor(Descriptor):
    
    """ A descriptor whose repr-string tries to be a literal reflection
        of its wrapped value
    """
    
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
        return super(BasePath, metacls).__prepare__(name, bases, **kwargs)
    
    def __new__(metacls, name, bases, attributes, basepath="/", **kwargs):
        """ Override for `Slotted.__new__(…)` setting up a
            derived slotted class that pulls from a “basepath”
            with the requisite methods defined for access.
        """
        if 'basepath' not in attributes:
            attributes['basepath'] = ValueDescriptor(basepath)
        
        return super(BasePath, metacls).__new__(metacls, name,
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
        if 'appspace' in kwargs:
            del kwargs['appspace']
        super(AppName, cls).__init_subclass__(**kwargs)
        cls.appname = ValueDescriptor(appname)
    
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

if consts.PYTHON_VERSION >= 3.7:
    
    class AsyncManagedContext(ManagedContext,
                              contextlib.AbstractAsyncContextManager):
        
        async def __aenter__(self):
            self.setup()
            if hasattr(self, '__await__'):
                if callable(self.__await__):
                    await self
            return self
        
        async def __aexit__(self, exc_type=None,
                                  exc_val=None,
                                  exc_tb=None):
            self.teardown()
            return exc_type is None

else:
    
    class AsyncManagedContext(ManagedContext):
        pass

__all__ = ('Slotted', 'NonSlotted',
           'Format', 'NonFormat', 'SlottedFormat', 'Sanitizer',
           'Cloneable',
           'ReprWrapper', 'SlottedRepr', 'MappingViewRepr',
           'evict_announcer',
           'BaseDescriptor', 'DataDescriptor', 'NamedDescriptor',
           'CacheDescriptor', 'Descriptor', 'ValueDescriptor',
           'BasePath', 'AppName',
           'ManagedContext', 'AsyncManagedContext')

__dir__ = lambda: list(__all__)
