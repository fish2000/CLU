# -*- coding: utf-8 -*-
from __future__ import print_function

class TestExtending(object):
    
    """ Run the tests for extensible and pair types. """
    
    def test_doubledutch(self):
        from clu.extending import doubledutch
        
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
        
        assert yodogg(10, 20).startswith('INTS')
        assert yodogg('yo', 'dogg').startswith('STRS')
        assert yodogg(3.14, 2.78).startswith('FLTS')
        assert yodogg(object(), object()) is None
    
    def test_extend_pair_pairtype(self):
        from clu.extending import pairtype, pair
        
        class __extend__(pairtype(int, int)):
            
            __name__ = "Coordinate"
            
            def ratio(xy):
                x, y = xy
                return x / y
        
        assert pair(2, 3).ratio() == 2 / 3
        
        class __extend__(pairtype(str, str)):
            
            __name__ = "NamespacedKey"
            
            def pack(tup):
                ns, key = tup
                return f"{ns}:{key}"
        
        assert pair('yo', 'dogg').pack() == "yo:dogg"
    
    def test_pairmro0(self):
        from clu.config.abc import FlatOrderedSet as FOSet
        from clu.config.abc import NamespacedMutableMapping as NaMutMap
        from clu.extending import pairmro
        from itertools import chain, product as dot_product
        
        iterchain = chain.from_iterable
        
        pair = []
        product = []
        
        for tup in pairmro(FOSet, NaMutMap):
            pair.append(tuple(str(el) for el in tup))
        
        for itp in dot_product(FOSet.__mro__, NaMutMap.__mro__):
            product.append(tuple(str(el) for el in itp))
        
        sorter = lambda t: ''.join(iterchain(t))
        retros = lambda t: ''.join(reversed(list(iterchain(t))))
        
        assert sorted(pair, key=sorter) == sorted(product, key=sorter)
        assert sorted(pair, key=retros) == sorted(product, key=retros)
        assert sorted(pair) == sorted(product)
        assert pair == product
    
    def test_pairmro1(self):
        from clu.config.abc import FlatOrderedSet as FOSet
        from clu.config.abc import NamespacedMutableMapping as NaMutMap
        from clu.extending import pairmro
        from itertools import product as dot_product
        
        pairs    = list(pairmro(FOSet, NaMutMap))
        products = list(dot_product(FOSet.mro(), NaMutMap.mro()))
        
        assert set(pairs) == set(products) # REALLY.
    
    def test_extensible_metaclass(self, dirname, consts):
        from clu.extending import Extensible
        import os
        
        class X(metaclass=Extensible):
            
            appname = consts.PROJECT_NAME
            filepath = os.getcwd()
            
            def __init__(self, name=None):
                self._name = name
            
            @property
            def name(self):
                return self._name or type(self).appname
        
        class __extend__(X):
            
            appname = "YoDogg".lower()
            filepath = dirname.subpath(appname)
            
            def __fspath__(self):
                return os.path.realpath(
                       type(self).filepath)
        
        class __extend__(X):
            
            @property
            def path(self):
                return os.fspath(self)
        
        ex = X(name='dogg')
        ux = X()
        
        assert ex.name == 'dogg'
        assert ux.name == 'yodogg'
        assert ex.path == os.path.join(consts.TEST_PATH, ex.appname)
        assert ux.path == os.path.join(consts.TEST_PATH, ux.appname)
        