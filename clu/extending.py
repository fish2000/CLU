# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain, product as dot_product

iterchain = chain.from_iterable

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
        
        return super(Extensible, metacls).__new__(metacls, name,
                                                           bases,
                                                           attributes,
                                                         **kwargs)
pairtype_cache = {}

tobject = tuplize(tuple)

@export
def pairtype(cls0, cls1):
    """ `type(pair(a, b))` is “pairtype(type(a), type(b))” """
    try:
        PairType = pairtype_cache[cls0, cls1]
    except KeyError:
        name = f"pairtype({cls0.__name__}, {cls1.__name__})"
        bases0 = [pairtype(base0, cls1) for base0 in cls0.__bases__]
        bases1 = [pairtype(cls0, base1) for base1 in cls1.__bases__]
        bases = tuple(bases0 + bases1) or tobject # tuple is the root base
        PairType = pairtype_cache[cls0, cls1] = Extensible(name, bases, {})
    return PairType

@export
def pairmro(cls0, cls1):
    """ Return the resolution order on pairs of types for double dispatch.
        
        This order is compatible with the mro of `pairtype(cls0, cls1)`
    """
    # N.B. do this with itertools?…
    # for base1 in cls1.__mro__:
    #     for base0 in cls0.__mro__:
    #         yield (base0, base1)
    # for base0 in cls0.__mro__:
    #     for base1 in cls1.__mro__:
    #         yield (base0, base1)
    yield from dot_product(cls0.mro(), cls1.mro())

@export
def pair(one, two):
    """ Return a pair object – a descendant of “__builtin__.tuple” """
    TupleType = pairtype(type(one), type(two))
    return TupleType((one, two))

Ω = pair

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

@export    
def doubledutch(function):
    """ Decorator returning a double-dispatch function.
        
        Usage:
        --------------------------------
        >>> @doubledutch
        ... def func(x, y):
        ...     return 0
        >>> 
        >>> @func.types(str, str)
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
    
    def types(self, cls0, cls1):
        def decorator(function):
            self.registry[cls0, cls1] = function
            return function
        return decorator

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from clu.config.abc import FlatOrderedSet as FOSet
    from clu.config.abc import NamespacedMutableMapping as NaMutMap
    from clu.testing.utils import pout
    
    def test_one():
        pair = []
        product = []
        
        # pout.v((tup, tup))
        for tup in pairmro(FOSet, NaMutMap):
            # pout.r(tup)
            pair.append(tuple(str(el) for el in tup))
        
        for itp in dot_product(FOSet.__mro__, NaMutMap.__mro__):
            # pout.r(itp)
            product.append(tuple(str(el) for el in itp))
        
        # pout.v(pair, product)
        # for t0, t1 in zip(pair, product):
        #     pout.v(t0, t1)
        
        pout.v(pair[:10], product[:10])
        
        sorter = lambda t: ''.join(iterchain(t))
        retros = lambda t: ''.join(reversed(list(iterchain(t))))
        
        assert sorted(pair, key=sorter) == sorted(product, key=sorter)
        assert sorted(pair, key=retros) == sorted(product, key=retros)
        assert sorted(pair) == sorted(product)
        assert pair == product
    
    def test_two():
        pairs    = list(pairmro(FOSet, NaMutMap))
        products = list(dot_product(FOSet.mro(), NaMutMap.mro()))
        # products = list(itertools.product(FOSet.__mro__, NaMutMap.__mro__))
        
        print("PAIRS    »", len(pairs))
        print("PRODUCTS »", len(products))
        
        assert set(pairs) == set(products) # REALLY.
    
    test_one()
    test_two()

if __name__ == '__main__':
    test()

