# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

import clu.abstract
import contextlib
import weakref
import sys

from clu.config.abc import FrozenKeyMap, KeyMap
from clu.naming import qualified_name
from clu.predicates import typeof, tuplize
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def selfcheck(function):
    """ Decorator abstracting a boolean self-check for weakref methods """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if not bool(self):
            typename = type(self).__name__
            raise ValueError(f"{typename} referent is dead")
        return function(self, *args, **kwargs)
    return wrapper

@export
class KeyMapView(FrozenKeyMap, clu.abstract.ReprWrapper,
                               clu.abstract.Cloneable,
                               contextlib.AbstractContextManager):
    
    __slots__ = tuplize('referent')
    
    @classmethod
    def get_basetype(cls):
        return getattr(cls, 'basetype', FrozenKeyMap)
    
    def __new__(cls, keymap):
        instance = super().__new__(cls)
        instance.referent = lambda: None
        return instance
    
    def __init__(self, keymap):
        if not keymap:
            raise ValueError("A valid keymap instance is required")
        basetype = type(self).get_basetype()
        if not isinstance(keymap, basetype):
            qualname = qualified_name(basetype)
            raise TypeError(f"A keymap instance descending from “{qualname}” is required")
        if type(getattr(keymap, 'referent', None)) is weakref.ReferenceType:
            self.referent = weakref.ref(keymap.referent())
        else:
            self.referent = weakref.ref(keymap)
    
    @selfcheck
    def get_reftype(self):
        return typeof(self.referent())
    
    @selfcheck
    def namespaces(self):
        yield from self.referent().namespaces()
    
    @selfcheck
    def __iter__(self):
        yield from self.referent()
    
    @selfcheck
    def __len__(self):
        return self.referent().__len__()
    
    @selfcheck
    def __contains__(self, nskey):
        return self.referent().__contains__(nskey)
    
    @selfcheck
    def __getitem__(self, nskey):
        return self.referent().__getitem__(nskey)
    
    @selfcheck
    def keys(self, *namespaces, unprefixed=False):
        return self.referent().keys(*namespaces, unprefixed=unprefixed)
    
    @selfcheck
    def items(self, *namespaces, unprefixed=False):
        return self.referent().items(*namespaces, unprefixed=unprefixed)
    
    @selfcheck
    def values(self, *namespaces, unprefixed=False):
        return self.referent().values(*namespaces, unprefixed=unprefixed)
    
    @selfcheck
    def __enter__(self):
        return self.referent()
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        return exc_type is None
    
    def __bool__(self):
        return self.referent() is not None
    
    def inner_repr(self):
        return repr(self.referent())
    
    def clone(self, deep=False, memo=None):
        return type(self)(self.referent())

@export
class KeyMapProxy(KeyMapView, KeyMap):
    
    basetype = KeyMap
    
    @selfcheck
    def freeze(self):
        return KeyMapView(self.referent())
    
    @selfcheck
    def __setitem__(self, nskey, value):
        self.referent().__setitem__(nskey, value)
    
    @selfcheck
    def __delitem__(self, nskey):
        self.referent().__delitem__(nskey)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from clu.config.ns import unpack_ns
    from clu.config.keymap import FrozenFlat, Flat
    from clu.config.keymap import nestedmaps, flatdict
    from pprint import pprint
    
    @inline.precheck
    def show_nestedmaps_fixture():
        """ Pretty-print the “nestedmaps()” fixture """
        pprint(nestedmaps(), indent=4)
    
    def test_one_fn(keymap_type, proxy_type, fixture_fn):
        """ Metafunction test generator for KeyMap proxy types:
            • generate tests for proxy/view type basic functionality
        """
        def test_fn():
            kmap = keymap_type(fixture_fn())
            prox = proxy_type(kmap)
            
            assert kmap == prox
            assert len(kmap) == len(prox)
            
            for ns0, ns1 in zip(kmap.namespaces(), prox.namespaces()):
                assert ns0 == ns1
            
            for iter0, iter1 in zip(kmap, prox):
                assert iter0 == iter1
                assert iter0 in kmap
                assert iter0 in prox
                assert iter1 in kmap
                assert iter1 in prox
            
            for keys0, keys1 in zip(kmap.keys(), prox.keys()):
                assert keys0 == keys1
                key0, ns0 = unpack_ns(keys0)
                key1, ns1 = unpack_ns(keys1)
                assert kmap.get(key0, *ns0) == prox.get(key1, *ns1)
                assert kmap.get(key1, *ns1) == prox.get(key0, *ns0)
            
            for items0, items1 in zip(kmap.items(), prox.items()):
                key0, val0 = items0
                key1, val1 = items1
                assert key0 == key1
                assert val0 == val1
            
            for val0, val1 in zip(kmap.values(), prox.values()):
                assert val0 == val1
        
        test_fn.__doc__ = """ %s vs. %s """ % (proxy_type.__name__,
                                              keymap_type.__name__)
        
        return test_fn
    
    def test_two_fn(keymap_type, proxy_type0, fixture_fn,
                                              proxy_type1=None,
                                              proxy_type2=None):
        """ Metafunction test generator for KeyMap proxy types:
            • generate tests for views-of-views and weakref integrity
        """
        if not proxy_type1:
            proxy_type1 = proxy_type0
        
        def test_fn():
            nonlocal proxy_type2
            
            kmap = keymap_type(fixture_fn())
            prox0 = proxy_type0(kmap)
            prox1 = proxy_type1(prox0)
            
            if not proxy_type2:
                if hasattr(kmap, 'freeze'):
                    proxy_type2 = kmap.freeze
                else:
                    proxy_type2 = lambda: proxy_type0(kmap)
            
            assert kmap == prox0
            assert kmap == prox1
            assert prox0 == prox1
            
            assert prox0.referent() == prox1.referent()
            assert prox0.referent == prox1.referent
            assert bool(prox0)
            assert bool(prox1)
            
            assert weakref.getweakrefcount(kmap) > 0 # this isn’t 2 somehow
            
            prox2 = proxy_type2()
            assert kmap == prox2
            assert prox0 == prox2
            assert prox1 == prox2
            assert bool(prox2)
            
            assert weakref.getweakrefcount(kmap) > 0 # this isn’t 2 somehow
        
        test_fn.__doc__ = """ %s of %s (&c.) """ % (proxy_type0.__name__,
                                                    proxy_type1.__name__)
        
        return test_fn
    
    # Add inline test functions using the metafunction test generators:
    inline.add_function(test_one_fn(FrozenFlat, KeyMapView,  flatdict),   'test_one')
    inline.add_function(test_two_fn(FrozenFlat, KeyMapView,  flatdict),   'test_two')
    inline.add_function(test_one_fn(Flat,       KeyMapView,  flatdict),   'test_three')
    inline.add_function(test_one_fn(Flat,       KeyMapProxy, flatdict),   'test_three_point_five')
    inline.add_function(test_two_fn(Flat,       KeyMapProxy, flatdict,
                                                KeyMapView),              'test_four')
    
    # N.B. These two take FUCKING FOREVER to run:
    # inline.add_function(test_one_fn(Nested,     KeyMapView,  nestedmaps), 'test_five')
    # inline.add_function(test_one_fn(Nested,     KeyMapProxy, nestedmaps), 'test_five_point_five')
    
    @inline.diagnostic
    def show_fixture_cache_stats():
        """ Show the per-fixture-function cache stats """
        from clu.config.keymap import inline as keymap_inline
        from clu.dicts import merge_fast_two
        
        fixtures = merge_fast_two(inline.fixtures,
                           keymap_inline.fixtures)
        total = len(fixtures)
        
        for idx, name in enumerate(fixtures.keys()):
            if idx > 0:
                print()
            print(f"FUNCTION CACHE INFO: {name} ({idx+1} of {total})")
            print(fixtures[name].cache_info())
    
    # Run all test functions:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
