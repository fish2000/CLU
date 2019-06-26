# -*- coding: utf-8 -*-
from __future__ import print_function
from enum import EnumMeta

class alias(object):
    
    """ Alias one Enum class instance to another. To wit:
        
            @unique
            class Numbers(Enum):
                ONE = 1
                TWO = 2
                THREE = 3
                UNO = alias(ONE)
                DOS = alias(TWO)
                TRÉS = alias(THREE)
        
        … unlike the enum documentation, which would have you
        create another set enum member-instances called UNO,
        DOS and TRÉS with the same values, respectively, as
        ONE, TWO, and THREE – using the alias(…) descriptor
        is a true aliasing operation, as accessing any alias
        instances e.g. `Numbers.DOS` actually gives you the
        actual aliased-to instance `Numbers.TWO` – which, as
        the documentation points out, they are all singletons,
        so `Numbers.TWO is Numbers.DOS` evaluates to `True`.
        
        Note that “@unique” has been used on this enum – alias
        members don’t count as new member-instances, so this
        enum class still contains three unique members, plus
        the three alias descriptors, which that is considered
        OK in the eyes of the @unique decorator.
        
        ISN’T ALL OF THAT FUCKING AWESOME?!?!? I think so. Yes!
    """
    
    # Dunder and sunder name constants for the alias dict:
    DUNDER = '__alias__'
    SUNDER = '_alias_'
    
    def __init__(self, instance, name=None, cls=None):
        """ Set up the alias, passing an enum instance.
            
            N.B. Use the “name” and “cls” arguments under Python 2
            or Python 3 < 3.6 – as they don’t yet support the
            “__set_name__” method (q.v. definition sub.)
            
        """
        self.aliased = instance
        if name is not None and cls is not None:
            self.name = name
            self.register(cls)
    
    def __get__(self, instance=None, cls=None):
        """ Return the aliased enum instance. """
        if cls is None:
            cls = type(instance)
        for thing in cls:
            if thing.value == self.aliased:
                return thing
        return self.aliased
    
    def __set_name__(self, cls, name):
        """ Register the alias within the __aliases__ dict in
            the class (if it has one).
            
            N.B. This only gets called on Python 3.6+
        """
        self.name = name
        self.register(cls)
    
    def register(self, cls):
        """ Register the alias member with the parent class,
            if it supports such things (that is to say, if it
            has a dictionary attribute “__aliases__”).
        """
        if hasattr(cls, '__aliases__'):
            if self.name in cls.__aliases__:
                message = "Enum already contains an alias named %s" % self.name
                raise AttributeError(message)
            cls.__aliases__[self.name] = self.aliased

class AliasingEnumMeta(EnumMeta):
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Ensure __aliases__ is a dictionary attribute on the new class.
            
            It is not strictly necessary to make this class an ancestor to
            your enums in order to use the `alias(…)` descriptor function,
            as defined above – if you do, the enums you define with it will
            conveniently furnish the __aliases__ dictionary, which is like
            the normal enum __members__ directory only with aliases. Yes.
        """
        
        if '__aliases__' not in attributes:
            attributes['__aliases__'] = {}
        
        return super(AliasingEnumMeta, metacls).__new__(metacls, name,
                                                                 bases,
                                                                 attributes,
                                                               **kwargs)

__all__ = ('alias', 'AliasingEnumMeta')
__dir__ = lambda: list(__all__)