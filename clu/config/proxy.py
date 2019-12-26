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
    
    basetype = FrozenKeyMap
    
    @classmethod
    def get_basetype(cls):
        return cls.basetype
    
    def __new__(cls, keymap):
        instance = super().__new__(cls)
        instance.keymap = lambda: None
        return instance
    
    def __init__(self, keymap):
        if not keymap:
            raise ValueError("A valid keymap is required")
        basetype = type(self).basetype
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
    
    @inline
    def test_one():
        """ KeyMapView vs. FrozenFlat """
        from clu.config.defg import FrozenFlat
        
        flat = FrozenFlat(flatdict())
        view = KeyMapView(flat)
        
        assert flat == view
        assert len(flat) == len(view)
        
        for ns0, ns1 in zip(flat.namespaces(), view.namespaces()):
            assert ns0 == ns1
        
        for iter0, iter1 in zip(flat, view):
            assert iter0 == iter1
            assert iter0 in flat
            assert iter0 in view
            assert iter1 in flat
            assert iter1 in view
        
        for keys0, keys1 in zip(flat.keys(), view.keys()):
            assert keys0 == keys1
            key0, ns0 = unpack_ns(keys0)
            key1, ns1 = unpack_ns(keys1)
            assert flat.get(key0, *ns0) == view.get(key1, *ns1)
            assert flat.get(key1, *ns1) == view.get(key0, *ns0)
        
        for items0, items1 in zip(flat.items(), view.items()):
            key0, val0 = items0
            key1, val1 = items1
            assert key0 == key1
            assert val0 == val1
        
        for val0, val1 in zip(flat.values(), view.values()):
            assert val0 == val1
    
    @inline
    def test_two():
        """ KeyMapView of KeyMapView """
        from clu.config.defg import FrozenFlat
        
        flat = FrozenFlat(flatdict())
        view0 = KeyMapView(flat)
        view1 = KeyMapView(view0)
        
        assert flat == view0
        assert flat == view1
        assert view0 == view1
        
        assert view0.keymap() == view1.keymap()
        assert view0.keymap == view1.keymap
        assert bool(view0)
        assert bool(view1)
        
        assert weakref.getweakrefcount(flat) > 0 # this isn’t 2 somehow
        
        view2 = KeyMapView(flat)
        assert flat == view2
        assert view0 == view2
        assert view1 == view2
        assert bool(view2)
        
        assert weakref.getweakrefcount(flat) > 0 # this isn’t 2 somehow
    
    @inline
    def test_three():
        """ KeyMapView vs. Flat """
        from clu.config.defg import Flat
        
        flat = Flat(flatdict())
        view = KeyMapView(flat)
        
        assert flat == view
        assert len(flat) == len(view)
        
        for ns0, ns1 in zip(flat.namespaces(), view.namespaces()):
            assert ns0 == ns1
        
        for iter0, iter1 in zip(flat, view):
            assert iter0 == iter1
            assert iter0 in flat
            assert iter0 in view
            assert iter1 in flat
            assert iter1 in view
        
        for keys0, keys1 in zip(flat.keys(), view.keys()):
            assert keys0 == keys1
            key0, ns0 = unpack_ns(keys0)
            key1, ns1 = unpack_ns(keys1)
            assert flat.get(key0, *ns0) == view.get(key1, *ns1)
            assert flat.get(key1, *ns1) == view.get(key0, *ns0)
        
        for items0, items1 in zip(flat.items(), view.items()):
            key0, val0 = items0
            key1, val1 = items1
            assert key0 == key1
            assert val0 == val1
        
        for val0, val1 in zip(flat.values(), view.values()):
            assert val0 == val1
    
    @inline
    def test_three_point_five():
        """ KeyMapProxy vs. Flat """
        from clu.config.defg import Flat
        
        flat = Flat(flatdict())
        prox = KeyMapProxy(flat)
        
        assert flat == prox
        assert len(flat) == len(prox)
        
        for ns0, ns1 in zip(flat.namespaces(), prox.namespaces()):
            assert ns0 == ns1
        
        for iter0, iter1 in zip(flat, prox):
            assert iter0 == iter1
            assert iter0 in flat
            assert iter0 in prox
            assert iter1 in flat
            assert iter1 in prox
        
        for keys0, keys1 in zip(flat.keys(), prox.keys()):
            assert keys0 == keys1
            key0, ns0 = unpack_ns(keys0)
            key1, ns1 = unpack_ns(keys1)
            assert flat.get(key0, *ns0) == prox.get(key1, *ns1)
            assert flat.get(key1, *ns1) == prox.get(key0, *ns0)
        
        for items0, items1 in zip(flat.items(), prox.items()):
            key0, val0 = items0
            key1, val1 = items1
            assert key0 == key1
            assert val0 == val1
        
        for val0, val1 in zip(flat.values(), prox.values()):
            assert val0 == val1
    
    @inline
    def test_four():
        """ KeyMapView of KeyMapProxy (and soforth) """
        from clu.config.defg import Flat
        
        flat = Flat(flatdict())
        prox = KeyMapProxy(flat)
        view = KeyMapView(prox)
        
        assert flat == view
        assert flat == prox
        assert view == prox
        
        assert view.keymap() == prox.keymap()
        assert view.keymap == prox.keymap
        assert bool(view)
        assert bool(prox)
        
        assert weakref.getweakrefcount(flat) > 0 # this isn’t 2 somehow
        
        proxview = prox.freeze()
        assert flat == proxview
        assert view == proxview
        assert prox == proxview
        assert bool(proxview)
        
        assert weakref.getweakrefcount(flat) > 0 # this isn’t 2 somehow
    
    @inline
    def test_five():
        """ KeyMapView vs. Nested """
        from clu.config.defg import Nested
        
        nest = Nested(nestedmaps())
        view = KeyMapView(nest)
        
        assert nest == view
        assert len(nest) == len(view)
        
        for ns0, ns1 in zip(nest.namespaces(), view.namespaces()):
            assert ns0 == ns1
        
        for iter0, iter1 in zip(nest, view):
            assert iter0 == iter1
            assert iter0 in nest
            assert iter0 in view
            assert iter1 in nest
            assert iter1 in view
        
        for keys0, keys1 in zip(nest.keys(), view.keys()):
            assert keys0 == keys1
            key0, ns0 = unpack_ns(keys0)
            key1, ns1 = unpack_ns(keys1)
            assert nest.get(key0, *ns0) == view.get(key1, *ns1)
            assert nest.get(key1, *ns1) == view.get(key0, *ns0)
        
        for items0, items1 in zip(nest.items(), view.items()):
            key0, val0 = items0
            key1, val1 = items1
            assert key0 == key1
            assert val0 == val1
        
        for val0, val1 in zip(nest.values(), view.values()):
            assert val0 == val1
    
    @inline
    def test_five_point_five():
        """ KeyMapProxy vs. Nested """
        from clu.config.defg import Nested
        
        nest = Nested(nestedmaps())
        prox = KeyMapProxy(nest)
        
        assert nest == prox
        assert len(nest) == len(prox)
        
        for ns0, ns1 in zip(nest.namespaces(), prox.namespaces()):
            assert ns0 == ns1
        
        for iter0, iter1 in zip(nest, prox):
            assert iter0 == iter1
            assert iter0 in nest
            assert iter0 in prox
            assert iter1 in nest
            assert iter1 in prox
        
        for keys0, keys1 in zip(nest.keys(), prox.keys()):
            assert keys0 == keys1
            key0, ns0 = unpack_ns(keys0)
            key1, ns1 = unpack_ns(keys1)
            assert nest.get(key0, *ns0) == prox.get(key1, *ns1)
            assert nest.get(key1, *ns1) == prox.get(key0, *ns0)
        
        for items0, items1 in zip(nest.items(), prox.items()):
            key0, val0 = items0
            key1, val1 = items1
            assert key0 == key1
            assert val0 == val1
        
        for val0, val1 in zip(nest.values(), prox.values()):
            assert val0 == val1
    
    return inline.test(50)

if __name__ == '__main__':
    sys.exit(test())
