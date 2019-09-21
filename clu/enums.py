# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants.polyfills import Enum, EnumMeta # type: ignore
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()
    
# Dunder and sunder name constants for the alias dict:
DUNDER = '__aliases__'
SUNDER = '_aliases_'

@export
class alias(object):
    
    __slots__ = ('name', 'aliased')
    
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
    
    def __init__(self, instance, name=None, cls=None):
        """ Set up the alias, passing an enum instance.
            
            N.B. Use the “name” and “cls” arguments under Python 2
            or Python 3 < 3.6 – as they don’t yet support the
            “__set_name__” method (q.v. definition sub.)
            
        """
        self.aliased = instance
        if name is not None and cls is not None:
            self.register(cls, name)
    
    def __get__(self, instance=None, cls=None):
        """ Return the aliased enum instance. """
        if cls is None:
            cls = type(instance)
        return self.member_for_value(cls, self.aliased)
    
    def __set_name__(self, cls, name):
        """ Register the alias within the __aliases__ dict in
            the class (if it has one).
            
            N.B. This only gets called on Python 3.6+
        """
        self.register(cls, name)
    
    def member_for_value(self, cls, value):
        """ Retrieve the original enum member corresponding
            to the stored aliases’ instance value.
        """
        for thing in cls:
            if thing.value == value:
                return thing
        for thing_name, thing_value in cls.__members__.items():
            if thing_value == value:
                return cls.__members__[thing_name]
        return value
    
    def register(self, cls, name):
        """ First, set the name of the alias.
            
            Second, register the alias member with the parent
            class, if it supports such things (that is to say,
            if it has a dictionary attribute “__aliases__”).
        """
        self.name = name
        if hasattr(cls, '__aliases__'):
            if self.name in cls.__aliases__:
                message = f"Enum already contains an alias named {self.name}"
                raise AttributeError(message)
            cls.__aliases__[self.name] = self.member_for_value(cls, self.aliased)

@export
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

@export
class AliasingEnum(Enum, metaclass=AliasingEnumMeta):
    """ An Enum subclass intermediate, suitable for subclassing
        itself, that uses `AliasingEnumMeta` as its metaclass.
        
        …Thus, any member aliases that one makes in concrete
        classes derived from this class will find them registered
        upon class creation in an `__aliases__` directory on the
        derived class.
    """
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
