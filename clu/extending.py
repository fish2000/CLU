# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants.consts import pytuple
from clu.predicates import tuplize
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

EXCLUDE = pytuple('module', 'package', 'qualname')

@export
class Extensible(type):
    
    """ Two magic tricks for classes:
            
            # In one file…
            class X(metaclass=Extensible):
                ...
            
            # In some other file…
            class __extend__(X):
                ...      # and here you can add new methods
                         # and class attributes to X!
            
        Mostly useful together with the second trick, which lets you build
        methods whose “self” is a pair of objects, instead of just one:
            
            class __extend__(pairtype(X, Y)):
                attribute = 42
                def method((x, y), other, arguments):
                    ...
            
            pair(x, y).attribute
            pair(x, y).method(other, arguments)
            
        This finds methods and class attributes based on the actual
        class of both objects that go into the “pair()”, with the usual
        rules of method/attribute overriding in (pairs of) subclasses.
    """
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Override for `type.__new__(…)` setting up a new
            extensible class.
        """
        if name == '__extend__':
            for cls in bases:
                for key, value in attributes.items():
                    if key in EXCLUDE:
                        continue
                    setattr(cls, key, value)
            return None
        
        return super(Extensible, metacls).__new__(metacls, name,
                                                           bases,
                                                           attributes,
                                                         **kwargs)

@export
def pair(one, two):
    """ Return a pair object """
    tup = pairtype(type(one), type(two))
    return tup((one, two))

Ω = pair
pairtype_cache = {}

@export
def pairtype(cls0, cls1):
    """ `type(pair(a, b))` is “pairtype(type(a), type(b))” """
    try:
        pair = pairtype_cache[cls0, cls1]
    except KeyError:
        name = f"pairtype({cls0.__name__}, {cls1.__name__})"
        bases0 = [pairtype(base0, cls1) for base0 in cls0.__bases__]
        bases1 = [pairtype(cls0, base1) for base1 in cls1.__bases__]
        bases = tuple(bases0 + bases1) or tuplize(tuple) # tuple is the root base
        pair = pairtype_cache[cls0, cls1] = Extensible(name, bases, {})
    return pair

@export
def pairmro(cls0, cls1):
    """ Return the resolution order on pairs of types for double dispatch.
        
        This order is compatible with the mro of `pairtype(cls0, cls0)`
    """
    # N.B. do this with itertools?…
    for base1 in cls1.__mro__:
        for base0 in cls0.__mro__:
            yield (base0, base1)

@export
class DoubleDutchRegistry(object):
    
    def __init__(self):
        self.registry = {}
        self.cache    = {}
    
    def __getitem__(self, clspair):
        try:
            return self.cache[clspair]
        except KeyError:
            cls0, cls1 = clspair
            for cc0, cc1 in pairmro(cls0, cls1):
                if (cc0, cc1) in self.cache:
                    return self.cache[(cc0, cc1)]
            else:
                raise
    
    def __setitem__(self, clspair, value):
        self.registry[clspair] = value
        self.cache = self.registry.copy()
    
    def doubledutch(function):
        """ Decorator returning a double-dispatch function.
            
            Usage:
            --------------------------------
            >>> @doubledutch
            ... def func(x, y):
            ...     return 0
            >>> 
            >>> @func.register(str, str)
            ... def func_str_str(x, y):
            ...     return 42
            >>> 
            >>> func(1, 2)
            0
            >>> func('x', 'y')
            42
            --------------------------------
        """
        return DoubleDutchFunction(function)

@export
class DoubleDutchFunction(object):
    
    def __init__(self, function):
        self.registry = DoubleDutchRegistry()
        self._default = function
    
    def __call__(self, argument0, argument1, *args, **kwargs):
        try:
            function = self.registry[type(argument0),
                                     type(argument1)]
        except KeyError:
            function = self._default
        return function(argument0, argument1, *args, **kwargs)
    
    def register(self, cls0, cls1):
        def decorator(function):
            self.registry[cls0, cls1] = function
            return function
        return decorator

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
