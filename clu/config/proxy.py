# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

import clu.abstract
import weakref
import sys

from clu.config.defg import FrozenKeyMap, KeyMap
from clu.naming import qualified_name
from clu.predicates import tuplize
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
                               clu.abstract.Cloneable):
    
    __slots__ = tuplize('keymap')
    
    @classmethod
    def get_basetype(cls):
        return getattr(cls, 'basetype', FrozenKeyMap)
    
    def __new__(cls, keymap):
        instance = super().__new__(cls)
        instance.keymap = lambda: None
        return instance
    
    def __init__(self, keymap):
        if not keymap:
            raise ValueError("A valid keymap is required")
        basetype = type(self).get_basetype()
        if not isinstance(keymap, basetype):
            qualname = qualified_name(basetype)
            raise TypeError(f"A descendant of “{qualname}” is required")
        if type(getattr(keymap, 'keymap', None)) is weakref.ReferenceType:
            self.keymap = weakref.ref(keymap.keymap())
        else:
            self.keymap = weakref.ref(keymap)
    
    @selfcheck
    def namespaces(self):
        yield from self.keymap().namespaces()
    
    @selfcheck
    def __iter__(self):
        yield from self.keymap().keys()
    
    @selfcheck
    def __len__(self):
        return self.keymap().__len__()
    
    @selfcheck
    def __contains__(self, nskey):
        return self.keymap().__contains__(nskey)
    
    @selfcheck
    def __getitem__(self, nskey):
        return self.keymap().__getitem__(nskey)
    
    def __bool__(self):
        return self.keymap() is not None
    
    def inner_repr(self):
        return repr(self.keymap())
    
    def clone(self, deep=False, memo=None):
        return type(self)(self.keymap())

@export
class KeyMapProxy(KeyMapView, KeyMap):
    
    basetype = KeyMap
    
    @selfcheck
    def freeze(self):
        return KeyMapView(self.keymap())
    
    @selfcheck
    def __setitem__(self, nskey, value):
        self.keymap().__setitem__(nskey, value)
    
    @selfcheck
    def __delitem__(self, nskey):
        self.keymap().__delitem__(nskey)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from clu.config.defg import mapwalk, pack_ns, unpack_ns
    from clu.config.defg import FrozenFlat, Flat, Nested
    from pprint import pprint
    
    @inline.fixture
    def nestedmaps():
        """ Private nested-dictionary pseudo-fixture """
        return {'body':   {'declare_i': {'id': {'name': 'i', 'type': 'Identifier'},
                                                'init': {'type': 'Literal', 'value': 2},
                                                'type': 'VariableDeclarator'},
                               'kind': 'var',
                               'type': 'VariableDeclaration',
                               'declare_j': {'id': {'name': 'j', 'type': 'Identifier'},
                                                'init': {'type': 'Literal', 'value': 4},
                                                'type': 'VariableDeclarator'},
                               'kind': 'var',
                               'type': 'VariableDeclaration',
                               'declare_answer': {'id': {'name': 'answer', 'type': 'Identifier'},
                                                'init': {'left': {'name': 'i',
                                                                  'type': 'Identifier'},
                                                         'operator': '*',
                                                         'right': {'name': 'j',
                                                                   'type': 'Identifier'},
                                                         'type': 'BinaryExpression'},
                                                'type': 'VariableDeclarator'},
                               'kind': 'var',
                               'type': 'VariableDeclaration'},
                'type':     'Program'}
    
    @inline.fixture
    def flatdict():
        """ Private flat-dictionary pseudo-fixture """
        out = {}
        for mappingpath in mapwalk(nestedmaps()):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            out[nskey] = value
        return out
    
    @inline.precheck
    def show_nestedmaps_fixture():
        """ Pretty-print the “nestedmaps()” fixture """
        pprint(nestedmaps(), indent=4)
    
    def test_one_fn(keymap_type, proxy_type, fixture_fn):
        """ Metafunction test generator for KeyMap proxy types:
            • generate tests for proxy/view type basic functionality
        """
        def test_fn():
            """ %s vs. %s """ % (proxy_type.__name__,
                                keymap_type.__name__)
            
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
            """ %s of %s (&c.) """ % (proxy_type0.__name__,
                                      proxy_type1.__name__)
            
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
            
            assert prox0.keymap() == prox1.keymap()
            assert prox0.keymap == prox1.keymap
            assert bool(prox0)
            assert bool(prox1)
            
            assert weakref.getweakrefcount(kmap) > 0 # this isn’t 2 somehow
            
            prox2 = proxy_type2()
            assert kmap == prox2
            assert prox0 == prox2
            assert prox1 == prox2
            assert bool(prox2)
            
            assert weakref.getweakrefcount(kmap) > 0 # this isn’t 2 somehow
        
        return test_fn
    
    # Add inline test functions using the metafunction test generators:
    inline.add_function(test_one_fn(FrozenFlat, KeyMapView,  flatdict),   'test_one')
    inline.add_function(test_two_fn(FrozenFlat, KeyMapView,  flatdict),   'test_two')
    inline.add_function(test_one_fn(Flat,       KeyMapView,  flatdict),   'test_three')
    inline.add_function(test_one_fn(Flat,       KeyMapProxy, flatdict),   'test_three_point_five')
    inline.add_function(test_two_fn(Flat,       KeyMapProxy, flatdict,
                                                KeyMapView),              'test_four')
    inline.add_function(test_one_fn(Nested,     KeyMapView,  nestedmaps), 'test_five')
    inline.add_function(test_one_fn(Nested,     KeyMapProxy, nestedmaps), 'test_five_point_five')
    
    # Run all test functions:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
