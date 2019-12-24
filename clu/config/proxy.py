# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

import clu.abstract
import weakref

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
class KeyMapProxy(KeyMap):
    
    def __init__(self, keymap):
        if not isinstance(keymap, KeyMap):
            qualname = qualified_name(KeyMap)
            raise TypeError(f"A descendant of “{qualname}” is required")
        super().__init__(keymap)
    
    @selfcheck
    def freeze(self):
        # if not bool(self):
        #     raise ValueError("KeyMapView referent is dead")
        return KeyMapView(self.keymap())
    
    @selfcheck
    def __setitem__(self, nskey, value):
        self.keymap().__setitem__(nskey, value)
    
    @selfcheck
    def __delitem__(self, nskey):
        self.keymap().__delitem__(nskey)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
