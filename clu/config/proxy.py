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
    
    def __new__(cls, keymap):
        instance = super().__new__(cls)
        instance.keymap = lambda: None
        return instance
    
    def __init__(self, keymap):
        if not keymap:
            raise ValueError("A valid keymap is required")
        if not isinstance(keymap, FrozenKeyMap):
            qualname = qualified_name(FrozenKeyMap)
            raise TypeError(f"A descendant of “{qualname}” is required")
        if isinstance(keymap, type(self)):
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
    
    def __init__(self, keymap):
        if not isinstance(keymap, KeyMap):
            qualname = qualified_name(KeyMap)
            raise TypeError(f"A descendant of “{qualname}” is required")
        super().__init__(keymap)
    
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
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
