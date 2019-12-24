# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain, product as dot_product
from functools import update_wrapper

import clu.abstract
import collections
import collections.abc
import inspect
import sys
import zict # type: ignore

iterchain = chain.from_iterable

from clu.constants.consts import pytuple
from clu.predicates import typeof, tuplize, attr
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

EXCLUDE = pytuple('module', 'package', 'qualname')

@export
class Extensible(clu.abstract.NonSlotted):
    
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
                def method(pair_xy, other, arguments):
                    x, y = pair_xy
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
        
        return super(Extensible, metacls).__new__(metacls, name, # type: ignore
                                                           bases,
                                                           attributes,
                                                         **kwargs)
pairtype_cache = {}
tobject = tuplize(tuple)

@export
def pairtype(cls0, cls1):
    """ `type(pair(a, b))` is “pairtype(typeof(a), typeof(b))” """
    try:
        PairType = pairtype_cache[cls0, cls1]
    except KeyError:
        name = f"pairtype({cls0.__name__}, {cls1.__name__})"
        bases0 = (pairtype(base0, cls1) for base0 in cls0.__bases__)
        bases1 = (pairtype(cls0, base1) for base1 in cls1.__bases__)
        bases = tuple(chain(bases0, bases1)) or tobject # tuple is the root base
        PairType = pairtype_cache[cls0, cls1] = Extensible(name, bases, {})
    return PairType

ΩΩ = pairtype

@export
def pairmro(cls0, cls1):
    """ Return the resolution order on pairs of types for double dispatch.
        
        This order is compatible with the mro of `pairtype(cls0, cls1)`
    """
    yield from dot_product(cls0.mro(), cls1.mro())

ω = pairmro

@export
def pair(one, two):
    """ Return a pair object – a descendant of “__builtin__.tuple” """
    PairType = pairtype(typeof(one), typeof(two))
    return PairType((one, two))

Ω = pair

@export
class DoubleDutchRegistry(clu.abstract.SlottedRepr,
                          collections.abc.MutableMapping,
                          collections.abc.Sized):
    
    __slots__ = ('registry', 'cache')
    
    def __init__(self):
        self.registry = {} # type: dict
        self.cache    = zict.LRU(64, self.registry)
    
    def __len__(self):
        return len(self.registry)
    
    def __contains__(self, clspair):
        return clspair in self.registry
    
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
        self.cache[clspair] = value
    
    def __delitem__(self, clspair):
        del self.cache[clspair]
    
    def __iter__(self):
        yield from self.cache.keys()

ASSIGNMENTS = pytuple('name', 'qualname', 'doc')
UPDATES = tuple() # type: tuple

isempty = lambda param: attr(param, 'annotation', default=inspect._empty) is inspect._empty
annotation = lambda param: isempty(param) and object or typeof(param.annotation)

@export
class DoubleDutchFunction(collections.abc.Callable):
    
    __slots__ = tuplize('registry') \
              + pytuple('wrapped', 'weakref') \
              + ASSIGNMENTS
    
    def __init__(self, function):
        self.registry = DoubleDutchRegistry()
        self.__wrapped__ = function
        update_wrapper(self, function,
                             assigned=ASSIGNMENTS,
                             updated=UPDATES)
    
    def __call__(self, argument0, argument1, *args, **kwargs):
        try:
            function = self.registry[typeof(argument0),
                                     typeof(argument1)]
        except KeyError:
            function = self.__wrapped__
        return function(argument0,
                        argument1,
                       *args,
                      **kwargs)
    
    def domain(self, cls0, cls1):
        def decoration(function):
            self.registry[cls0, cls1] = function
            return self
        return decoration
    
    @property
    def annotated(self):
        def decoration(function):
            classes = [object, object]
            signature = inspect.signature(function)
            for idx, key in enumerate(signature.parameters):
                parameter = signature.parameters[key]
                classes[idx] = annotation(parameter)
            regkey = tuplize(*classes[:2])
            self.registry[regkey] = function
            return self
        return decoration

@export
def doubledutch(function):
    """ Decorator returning a double-dispatch function.
        
        Usage:
        --------------------------------
        >>> @doubledutch
        ... def func(x, y):
        ...     return 42
        >>> 
        >>> @func.domain(str, str)
        ... def func(x, y):
        ...     return "42"
        >>> 
        >>> @func.annotated
        ... def func(x: int, y: int):
        ...     return x * y
        >>> 
        >>> func(None, None)
        42
        >>> func(1, 42)
        42
        >>> func('x', 'y')
        "42"
        --------------------------------
    """
    return DoubleDutchFunction(function)

export(ΩΩ, name='ΩΩ')
export(ω,  name='ω')
export(Ω,  name='Ω')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from clu.config.abc import FlatOrderedSet as FOSet
    from clu.config.abc import NamespacedMutableMapping as NaMutMap
    from clu.testing.utils import pout, inline
    
    @inline
    def test_one():
        pair = []
        product = []
        
        for tup in ω(FOSet, NaMutMap):
            pair.append(tuple(str(el) for el in tup))
        
        for itp in dot_product(FOSet.__mro__, NaMutMap.__mro__):
            product.append(tuple(str(el) for el in itp))
        
        # pout.v(pair[:10], product[:10])
        
        sorter = lambda t: ''.join(iterchain(t))
        retros = lambda t: ''.join(reversed(list(iterchain(t))))
        
        assert sorted(pair, key=sorter) == sorted(product, key=sorter)
        assert sorted(pair, key=retros) == sorted(product, key=retros)
        assert sorted(pair) == sorted(product)
        assert pair == product
    
    @inline
    def test_two():
        pairs    = list(ω(FOSet, NaMutMap))
        products = list(dot_product(FOSet.mro(), NaMutMap.mro()))
        
        print()
        print("PAIRS    »", len(pairs))
        print("PRODUCTS »", len(products))
        
        assert set(pairs) == set(products) # REALLY.
    
    @inline
    def test_three():
        
        class __extend__(ΩΩ(int, int)): # type: ignore
            
            __name__ = "Coordinate"
            
            def ratio(xy):
                x, y = xy
                return x / y
        
        assert Ω(2, 3).ratio() == 2 / 3
        
        class __extend__(ΩΩ(str, str)): # type: ignore
            
            __name__ = "NamespacedKey"
            
            def pack(tup):
                ns, key = tup
                return f"{ns}:{key}"
        
        assert Ω('yo', 'dogg').pack() == "yo:dogg"
    
    # @inline
    def test_four():
        print()
        
        pout.v(__all__)
        pout.v(__dir__())
        pout.v(exporter)
    
    @inline
    def test_five():
        print()
        
        @doubledutch
        def yodogg(x, y):
            return None
        
        @yodogg.domain(int, int)
        def yodogg(x, y):
            return f"INTS: {x}, {y}"
        
        @yodogg.domain(str, str)
        def yodogg(x, y):
            return f"STRS: {x}, {y}"
        
        @yodogg.annotated
        def yodogg(x: float, y: float):
            return f"FLTS: {x}, {y}"
        
        print(yodogg(10, 20))
        print(yodogg('yo', 'dogg'))
        print(yodogg(3.14, 2.78))
        print("DEFAULTING »", yodogg(object(), object()))
        
        print()
        print("REGISTRY »", repr(yodogg.registry))
    
    # Run aggregate inline tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())