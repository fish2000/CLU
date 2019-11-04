# -*- coding: utf-8 -*-
from __future__ import print_function
import abc

abstract = abc.abstractmethod

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
            del attributes['__slots__']
        
        return super(NonSlotted, metacls).__new__(metacls, name,
                                                           bases,
                                                           attributes,
                                                         **kwargs)

class ValueDescriptor(object):
    
    __slots__ = ('value',)
    
    def __init__(self, value):
        self.value = value
    
    def __get__(self, *args):
        return self.value
    
    def __set__(self, instance, value):
        pass
    
    def __repr__(self):
        from clu.constants.consts import ENCODING
        return isinstance(self.value, str)   and self.value or \
               isinstance(self.value, bytes) and self.value.decode(ENCODING) or \
                                            repr(self.value)

class AppName(abc.ABC):
    
    __slots__ = tuple()
    
    @classmethod
    def __init_subclass__(cls, appname=None, **kwargs):
        """ Translate the “appname” class-keyword into an “appname” read-only
            descriptor value
        """
        super(AppName, cls).__init_subclass__(**kwargs)
        cls.appname = ValueDescriptor(appname)
    
    def __init__(self, *args, **kwargs):
        """ Stub __init__(…) method, throwing a lookup error for subclasses
            upon which the “appname” value is None
        """
        if type(self).appname is None:
            raise LookupError("Cannot instantiate a base config class "
                              "(appname is None)")

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
    
    def __repr__(self):
        """ This classes’ object instances’ unique string representation """
        from clu.repr import typename_hexid
        cnm, hxa = typename_hexid(self)
        rpr = self.inner_repr()
        return f"{cnm}({rpr}) @ {hxa}"

__all__ = ('Slotted', 'NonSlotted',
           'ValueDescriptor',
           'AppName',
           'Cloneable',
           'ReprWrapper')

__dir__ = lambda: list(__all__)
