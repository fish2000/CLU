# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain

iterchain = chain.from_iterable

import clu.abstract
import collections
import collections.abc
import sys

from clu.constants.consts import NoDefault
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# DICT VIEWS: OrderedMappingView and friends

@export
class OrderedMappingView(collections.abc.MappingView,
                         collections.abc.Sequence,
                         collections.abc.Reversible,
                         clu.abstract.MappingViewRepr):
    
    """ A mapping view class implementing “collections.abc.Sequence”
        and “collections.abc.Reversible”
    """
    
    def __reversed__(self):
        yield from reversed(self._mapping)
    
    def __getitem__(self, idx):
        return tuple(self)[idx]

@export
class OrderedItemsView(collections.abc.ItemsView,
                       collections.abc.Sequence,
                       collections.abc.Reversible,
                       clu.abstract.MappingViewRepr):
    
    """ An items-view class implementing “collections.abc.Sequence”
        and “collections.abc.Reversible”
    """
    
    def __reversed__(self):
        for key in reversed(self._mapping):
            yield (key, self._mapping[key])
    
    def __getitem__(self, idx):
        return tuple(self)[idx]

@export
class OrderedKeysView(collections.abc.KeysView,
                      collections.abc.Sequence,
                      collections.abc.Reversible,
                      clu.abstract.MappingViewRepr):
    
    """ A keys-view class implementing “collections.abc.Sequence”
        and “collections.abc.Reversible”
    """
    
    def __reversed__(self):
        yield from reversed(self._mapping)
    
    def __getitem__(self, idx):
        return tuple(self)[idx]

@export
class OrderedValuesView(collections.abc.ValuesView,
                        collections.abc.Sequence,
                        collections.abc.Reversible,
                        clu.abstract.MappingViewRepr):
    
    """ A values-view class implementing “collections.abc.Sequence”
        and “collections.abc.Reversible”
    """
    
    def __reversed__(self):
        for key in reversed(self._mapping):
            yield self._mapping[key]
    
    def __getitem__(self, idx):
        return tuple(self)[idx]

# CHAINMAP: a reimplementation

@export
class ChainMap(collections.abc.MutableMapping,
               clu.abstract.Cloneable,
               clu.abstract.ReprWrapper,
               metaclass=clu.abstract.Slotted):
    
    __slots__ = ('maps', '__weakref__')
    
    @classmethod
    def fromkeys(cls, iterable, *args):
        return cls(dict.fromkeys(iterable, *args))
    
    @classmethod
    def fromitems(cls, *iterables, **overrides):
        return cls(dict(iterchain(iterables)), **overrides)
    
    def __init__(self, *dicts, **overrides):
        """ Initialize a new ChainMap, using as many maps as specified as varargs,
            with any additional keyword args going into a new first map.
            
            The signature of “clu.dicts.ChainMap.__init__(…)” is functionally the
            same as as “clu.dicts.merge(…)” (q.v. definition sub.)
            
            Instances of either “clu.dicts.ChainMap” or its spiritual predecessor,
            “collections.ChainMap”, will have their constituent dicts extracted
            and individually appended to the new ChainMaps’ internal list.
        """
        extras = [dict(**overrides)]
        maps = [] # type: list
        for d in dicts:
            if isinstance(d, (type(self), collections.ChainMap)):
                for map in d.maps:
                    if bool(map):
                        if map not in maps:
                            maps.append(map)
            else:
                if d not in maps:
                    maps.append(d)
        if extras[0]:
            self.maps = list(chain(maps, extras))
        else:
            self.maps = list(maps) or extras
    
    def __missing__(self, key):
        raise KeyError(key)
    
    def __getitem__(self, key):
        from clu.predicates import try_items
        return try_items(key, *self.maps, default=None) or self.__missing__(key)
    
    def __len__(self):
        return len(frozenset(iterchain(self.maps)))
    
    def __bool__(self):
        return any(self.maps)
    
    def __contains__(self, key):
        return any(key in map for map in self.maps)
    
    def __iter__(self):
        yield from merge(*reversed(self.maps))
    
    def get(self, key, default=NoDefault):
        if default is NoDefault:
            return self[key]
        from clu.predicates import getitem
        return getitem(self, key, default=default)
    
    def shift(self):
        """ Create and return a new ChainMap instance from “maps[1:]” """
        # Equivalent to collections.ChainMap.parents:
        return type(self)(*self.maps[1:])
    
    def unshift(self, map=None):
        """ Create and return a new ChainMap with a new map followed
            by all previous maps.
            
            If no map is provided, an empty dict is used.
        """
        # Equivalent to collections.ChainMap.new_child(…)
        cls = type(self)
        if isinstance(map, (cls, collections.ChainMap)):
            return cls(*(m for m in map.maps if bool(m)), *self.maps)
        return cls(map or {}, *self.maps)
    
    def __setitem__(self, key, value):
        self.maps[0][key] = value
    
    def __delitem__(self, key):
        try:
            del self.maps[0][key]
        except KeyError:
            raise KeyError(f'Key not found in the first mapping: {key!r}')
    
    def popitem(self):
        try:
            return self.maps[0].popitem()
        except KeyError:
            raise KeyError('No keys found in the first mapping')
    
    def pop(self, key, default=NoDefault):
        if default is NoDefault:
            return self.maps[0].pop(key)
        return self.maps[0].pop(key, default)
    
    def clear(self):
        self.maps[0].clear()
        return self
    
    def mapcontaining(self, itx, default=NoDefault):
        from clu.predicates import finditem
        if default is NoDefault:
            return finditem(itx, *self.maps) or self.__missing__(itx)
        return finditem(itx, *self.maps, default=default)
    
    def flatten(self):
        return merge(*reversed(self.maps))
    
    def clone(self, deep=False, memo=None):
        cls = type(self)
        if not deep:
            return cls(self.maps[0].copy(),
                      *self.maps[1:])
        from copy import deepcopy
        return cls(deepcopy(self.maps[0]),
                 *(deepcopy(map) for map in self.maps[1:]))
    
    def inner_repr(self):
        from pprint import pformat
        return pformat(self.maps)

# DICT FUNCTIONS: dictionary-merging

@export
def merge_two(one, two, cls=dict):
    """ Merge two dictionaries into an instance of the specified class
        Based on this docopt example source: https://git.io/fjCZ6
    """
    from clu.predicates import typeof, item_search
    cls = typeof(cls or one)
    keys = frozenset(one) | frozenset(two)
    return cls((key, item_search(key, one, two)) for key in keys)

@export
def merge_as(*dicts, cls=dict, **overrides):
    """ Merge all dictionary arguments into a new instance of the specified class,
        passing all additional keyword arguments to the class constructor as overrides
    """
    from clu.predicates import typeof
    cls = typeof(cls or (dicts and dicts[0] or dict))
    merged = cls(**overrides)
    for d in dicts:
        merged = merge_two(merged, d, cls=cls)
    return merged

@export
def merge(*dicts, **overrides):
    """ Merge all dictionary arguments into a new `dict` instance, using any
        keyword arguments as item overrides in the final `dict` instance returned
    """
    if 'cls' in overrides:
        raise NameError('Cannot override the `cls` value')
    return merge_as(*dicts, cls=dict, **overrides)

# DICT STUFF: asdict(…)

@export
def asdict(thing):
    """ asdict(thing) → returns either thing, thing.__dict__, or dict(thing) as necessary """
    from clu.predicates import haspyattr
    from clu.typology import ismapping
    if isinstance(thing, dict):
        return thing
    if haspyattr(thing, 'dict'):
        return asdict(thing.__dict__)
    if hasattr(thing, '_asdict'):
        return asdict(thing._asdict())
    if hasattr(thing, 'to_dict'):
        return asdict(thing.to_dict())
    if hasattr(thing, 'dict'):
        return asdict(thing.dict)
    if ismapping(thing):
        return dict(thing)
    return dict(thing)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from clu.constants.consts import TEST_PATH
    from clu.constants.data import XDGS
    from clu.fs.filesystem import Directory
    from clu.predicates import try_items
    from clu.testing.utils import inline
    from pprint import pprint
    import os
    
    dirname = Directory(TEST_PATH)
    data = dirname.subdirectory('data')
    stash = os.environ.copy()
    
    # Arbitrary:
    dict_one = {
        'yo'    : "dogg",
        'i'     : "heard",
        'you'   : "liked",
        'dict'  : "chains" }
    
    @inline.fixture
    def environment():
        for key in XDGS:
            if key in os.environ:
                del os.environ[key]
        return os.environ
    
    @inline
    def test_one():
        try:
            env = environment()
            
            chain0 = ChainMap(dict_one, data, env)
            
            # pout.v(sorted(env.keys()))
            # pout.v(sorted(chain0.keys()))
            pprint(sorted(chain0.keys()))
            print()
            
            # First: shallow clone
            chain1 = chain0.clone()
            assert len(chain0) == len(chain1)
            for key in chain0.keys():
                assert key in chain0
                assert key in chain0.flatten()
                assert key in chain1
                assert key in chain1.flatten()
                assert try_items(key, *chain0.maps, default=None) is not None
                assert try_items(key, *chain1.maps, default=None) is not None
                assert try_items(key, *chain0.maps, default=None) == try_items(key, *chain1.maps, default=None)
                assert try_items(key, *chain0.maps, default=None) == chain0[key]
                assert try_items(key, *chain0.maps, default=None) == chain1[key]
            
            # Next: deep clone
            chainX = chain0.clone(deep=True)
            assert len(chain0) == len(chainX)
            for key in chain0.keys():
                assert key in chain0
                assert key in chain0.flatten()
                assert key in chainX
                assert key in chainX.flatten()
                assert try_items(key, *chain0.maps, default=None) is not None
                assert try_items(key, *chainX.maps, default=None) is not None
                assert try_items(key, *chain0.maps, default=None) == try_items(key, *chainX.maps, default=None)
                assert try_items(key, *chain0.maps, default=None) == chain0[key]
                assert try_items(key, *chain0.maps, default=None) == chainX[key]
            
            assert chain0 == ChainMap(dict_one, data, env)
            assert chain0 == chain1
            assert chain0 == chainX
            assert chainX == chain1
            
            # pout.v(sorted(chainX.keys()))
            pprint(sorted(chainX.keys()))
            print()
            
        finally:
            os.environ = stash # type: ignore
    
    # Run all inline tests:
    return inline.test(10)

if __name__ == '__main__':
    sys.exit(test())