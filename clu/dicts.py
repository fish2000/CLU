# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain
from reprlib import Repr

iterchain = chain.from_iterable

import clu.abstract
import collections
import collections.abc
import sys

from clu.constants.consts import STRINGPAIR, WHITESPACE, NoDefault
from clu.config.abc import FlatOrderedSet as FOSet
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
    
    def __reversed__(self): # pragma: no cover
        yield from reversed(self._mapping)
    
    def __getitem__(self, idx): # pragma: no cover
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

# CHAINMAP: custom reprlib.Repr subclass

@export
class ChainRepr(Repr):
    
    """ Custom Repr-izer for “clu.dicts.ChainMap” composite
        mappings, which can recursively self-contain, and not
        infinitely recurse all over the living-room floor.
        
        q.v. cpython docs, http://bit.ly/2r1GQ4l supra.
    """
    
    def __init__(self, *args, maxlevel=10,
                              maxstring=120,
                              maxother=120,
                            **kwargs):
        """ Initialize a ChainRepr, with default params
            for ‘maxlevel’, ‘maxstring’, and ‘maxother’.
        """
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()
        self.maxlevel = maxlevel
        self.maxstring = maxstring
        self.maxother = maxother
    
    def subrepr(self, thing, level):
        """ An internal “core” repr helper method. """
        from clu.typology import ismapping
        
        # For mappings, go down another level:
        if ischainmap(thing) or ismapping(thing):
            return self.repr1(thing, level - 1)
        
        # For everything else, defer to the type:
        return repr(thing)
    
    def primerepr(self, mapping, level):
        """ The internal method for “core” repr production
            of all ChainMaps, and related descendant types.
        """
        # Special-case empty and single-item maps:
        if len(mapping) == 0:
            return "{}"
        
        elif len(mapping) == 1:
            key = tuple(mapping.keys())[0]
            item = STRINGPAIR.format(key, self.subrepr(mapping[key], level))
            return f"{{ {item} }}"
        
        # Format all items:
        items = (STRINGPAIR.format(key, self.subrepr(mapping[key], level)) \
                               for key in mapping.keys())
        
        # Compute indentation levels:
        ts = "    " * (int(self.maxlevel - level) + 1)
        ls = "    " * (int(self.maxlevel - level) + 0)
        total = (f",\n{ts}").join(items)
        
        # Return the formatted map contents:
        return f"{{ \n{ts}{total}\n{ls}}}"
    
    def toprepr(self, chainmap, level):
        """ The “top-level” ChainMap-specific repr method –
            this will parse through the individual mappings
            that comprise the ChainMap instance, and dispatch
            sub-repr method calls accordingly.
        """
        from clu.naming import qualified_name
        from clu.testing.utils import multiple
        
        # Typename and map item counts:
        tn = qualified_name(type(chainmap))
        mapcount = len(chainmap.maps)
        keycount = len(chainmap)
        
        # Special-case empty maps:
        if mapcount == 0 and keycount == 0:
            ts = ls = total = ""
            return f"{tn} «{mapcount} map{multiple(mapcount)}, " \
                         f"{keycount} key{multiple(keycount)}» " \
                         f"[{ts}{total}{ls}]"
        
        # Format all items:
        items = (STRINGPAIR.format(qualified_name(type(mapping)),
                                   self.primerepr(mapping, level - 1)) \
                                   for mapping in chainmap.maps)
        
        # Compute indentation levels:
        ts = "    " * (int(self.maxlevel - level) + 1)
        ls = "    " * (int(self.maxlevel - level) + 0)
        total = (f",\n{ts}").join(items)
        
        # Return all formatted sub-reprs:
        return f"{tn} «{mapcount} map{multiple(mapcount)}, " \
                     f"{keycount} key{multiple(keycount)}» " \
                     f"[\n{ts}{total}\n{ls}]"
    
    def repr_dict(self, mapping, level):
        return self.primerepr(mapping, level)
    
    def repr_UserDict(self, mapping, level): # pragma: no cover
        return self.primerepr(mapping, level)
    
    def repr_Directory(self, mapping, level): # pragma: no cover
        return mapping.inner_repr()
    
    def repr_TemporaryDirectory(self, mapping, level): # pragma: no cover
        return mapping.inner_repr()
    
    def repr_SimpleNamespace(self, mapping, level): # pragma: no cover
        return self.primerepr(asdict(mapping), level)
    
    def repr_Namespace(self, mapping, level): # pragma: no cover
        return self.primerepr(asdict(mapping), level)
    
    def repr_Typespace(self, mapping, level): # pragma: no cover
        return self.primerepr(asdict(mapping), level)
    
    def repr_defaultdict(self, mapping, level): # pragma: no cover
        return self.primerepr(mapping, level)
    
    def repr_OrderedDict(self, mapping, level): # pragma: no cover
        return self.primerepr(mapping, level)
    
    def repr_mappingproxy(self, mapping, level): # pragma: no cover
        return self.primerepr(mapping, level)
    
    def repr_ChainMap(self, chainmap, level):
        # Handles both “clu.dict.ChainMap” and “collections.ChainMap”,
        # thanks to “reprlib.Repr” name-based type dispatching:
        return self.toprepr(chainmap, level)
    
    def repr_ChainMapPlusPlus(self, chainmap, level):
        return self.toprepr(chainmap, level)
    
    def shortrepr(self, thing):
        """ Return the “short” repr of a chainmap instance –
            all whitespace will be condensed to single spaces
            without newlines.
        """
        return WHITESPACE.sub(' ', self.repr(thing))

reprizer = ChainRepr()
cmrepr = reprizer.repr
cmshortrepr = reprizer.shortrepr

# CHAINMAP: a reimplementation

@export
class ChainMap(collections.abc.MutableMapping,
               clu.abstract.Cloneable,
               metaclass=clu.abstract.Slotted):
    
    __slots__ = ('maps', '__weakref__')
    
    @classmethod
    def fromkeys(cls, iterable, *args, **overrides): # pragma: no cover
        """ Create a new ChainMap instance, using keys plucked from
            “iterable”, and values harvested from the subsequent
            variadic arguments.
        """
        return cls(dict.fromkeys(iterable, *args), **overrides)
    
    @classmethod
    def fromitems(cls, *iterables, **overrides): # pragma: no cover
        """ Create a new ChainMap instance, using key-value pairs
            obtained from one or more iterables, with any keyword
            arguments serving as optional overrides.
        """
        return cls((dict(iterable) for iterable in iterables), **overrides)
    
    @classmethod
    def is_a(cls, instance):
        """ Check if an instance is a ChainMap of any sort – this covers:
            
            • this class (whichever it may be, derived or otherwise)
            • the root clu.dicts.ChainMap type, and
            • the original collections.ChainMap type as well.
        """
        return isinstance(instance, (cls,
                                     ChainMap,
                                     collections.ChainMap))
    
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
            if type(self).is_a(d):
                for map in d.maps:
                    if bool(map):
                        if map not in maps:
                            maps.append(map)
            else:
                if d not in maps:
                    maps.append(d)
        if bool(extras[0]):
            self.maps = list(chain(maps, extras))
        else:
            self.maps = maps
    
    def __missing__(self, key):
        raise KeyError(key)
    
    def __getitem__(self, key):
        from clu.predicates import try_items
        try:
            return try_items(key, *self.maps)
        except KeyError:
            return self.__missing__(key)
    
    def __len__(self):
        return len(set(iterchain(map.keys() for map in self.maps)))
    
    def __iter__(self):
        yield from set(iterchain(map.keys() for map in self.maps))
    
    def __contains__(self, key):
        return any(key in map for map in self.maps)
    
    def __bool__(self):
        return any(self.maps)
    
    def __str__(self):
        return cmshortrepr(self)
    
    def __repr__(self):
        return cmrepr(self)
    
    def get(self, key, default=NoDefault):
        """ Return the value for “key” if it is in any of the mappings
            in the ChainMap, else “default”.
            
            If no “default” is specified and the key is not found,
            a KeyError will be raised.
        """
        if default is NoDefault:
            return self[key]
        from clu.predicates import getitem
        return getitem(self, key, default=default)
    
    def mapchain(self):
        """ Return a generator over all of the ChainMap’s mappings """
        yield from self.maps
    
    @property
    def top(self):
        """ Return the first mapping – aka ``car(maps)`` """
        return self.maps[0]
    
    @property
    def rest(self):
        """ Return all of the mappings behind the first – aka ``cdr(maps)`` """
        return self.maps[1:]
    
    def shift(self):
        """ Create and return a new ChainMap instance from “maps[1:]” –
            the “cdr(maps)”, for you Little Lispers out there –
            as a shallow copy.
        """
        # Equivalent to collections.ChainMap.parents:
        return type(self)(*self.rest)
    
    def unshift(self, map=None):
        """ Create and return a new ChainMap with a new map followed
            by all previous maps.
            
            If no map is provided, an empty dict is used.
            
            If the map provided is a ChainMap – either one from the
            standard library “collections” module or from CLU, its
            constituent maps will be torn from it and each gruesomely
            vivisected into the new instance, as if the subject of a
            scene deleted from a kind of Pythonic Saw movie.
        """
        # Equivalent to collections.ChainMap.new_child(…)
        return type(self)(map or {}, *self.maps)
    
    def __setitem__(self, key, value):
        self.top[key] = value
    
    def __delitem__(self, key):
        try:
            del self.top[key]
        except KeyError as exc:
            raise KeyError(f'Key not found in the topmost mapping: {key!r}') from exc
    
    def popitem(self):
        """ chainmap.popitem() → (key, value), remove & return a (key, value)
            pair, nondeterministically, as a 2-tuple; but raise a KeyError
            if the top mapping of the ChainMap (aka ‘self.maps[0]’) is empty.
        """
        try:
            return self.top.popitem()
        except KeyError as exc:
            raise KeyError('No keys found in the topmost mapping') from exc
    
    def pop(self, key, default=NoDefault):
        """ chainmap.pop(key[, default]) → v, remove specified “key” from
            the top mapping of the ChainMap, and return the corresponding
            value.
            
            If “key” is not found, “default” is returned if given –
            otherwise a KeyError is raised.
        """
        if default is NoDefault:
            return self.top.pop(key)
        return self.top.pop(key, default)
    
    def clear(self):
        """ Remove all items from the top mapping of the ChainMap. """
        self.top.clear()
        return self
    
    def mapcontaining(self, itx, default=NoDefault):
        """ Search the ChainMap’s internal mappings for an item, by name,
            and return the first mapping in which an item by this name
            can be found.
            
            A default value, returned when no mappings are to be found
            containing an item by the specified name, may optionally
            be passsed in as well.
        """
        from clu.predicates import finditem
        if default is NoDefault:
            return finditem(itx, *self.maps) or { itx : self.__missing__(itx) }
        return finditem(itx, *self.maps, default=default)
    
    def flatten(self):
        """ Dearticulate the ChainMap instances’ internal map stack
            into a new, single, flat dictionary instance.
        """
        return merge_fast(*reversed(self.maps))
    
    def clone(self, deep=False, memo=None):
        """ Return a cloned copy of the ChainMap instance """
        from copy import copy, deepcopy
        cls = type(self)
        if not deep:
            return cls(copy(self.top),
                           *self.rest)
        return cls(deepcopy(self.top),
                 *(deepcopy(map) for map in self.rest))

class ChainMapPlusPlus(ChainMap):
    
    def __init__(self, *dicts, **overrides):
        
        maps = []
        
        for d in dicts:
            if type(self).is_a(d):
                maps.append(FOSet(*d.maps, predicate=bool))
            else:
                maps.append(d)
        
        if bool(overrides):
            maps.append(FOSet(dict(**overrides)))
        
        self.maps = FOSet(*maps)

@export
def ischainmap(thing):
    """ ischainmap(thing) → boolean predicate, True if the
        type of “thing” is a ChainMap or a descendant of same –
        either a “clu.dicts.ChainMap”, a “collections.ChainMap”;
        anything will do… if this was the last time, then you should
        tell us what to do.
        
        I was afraid I guess, now I can’t think no more – I was so
        concentrated on keeping things together; I’ve learned to
        focus on. I didn’t want to disappoint. Now I miss everybody,
        is it still light outside?
    """
    from clu.typology import subclasscheck
    return subclasscheck(thing, (ChainMap, collections.ChainMap))

# DICT FUNCTIONS: dictionary-merging

@export
def merge_fast_two(one, two):
    """ Merge two dictionaries performantly into an instance of “dict”.
        
        Based on this extremely beloved SO answer:
            https://stackoverflow.com/a/26853961/298171
    """
    # N.B. the dict-expanded operands appear here in the opposite order
    # from their positions in the function signature due to the way keys
    # take precedence in this sort of expression – this is detailed further
    # in the SO post – but the upshot is that this is the functional
    # equivalent to the “merge_two(…)” function, below.
    return { **two, **one }

@export
def merge_fast(*dicts, **extras):
    """ Merge all dictionary arguments into a new instance of “dict”.
        passing all additional keyword arguments as an additional dict instance.
        
        Based on this extremely beloved SO answer:
            https://stackoverflow.com/a/26853961/298171
    """
    length = len(dicts)
    if length == 10:
        return { **extras,   **dicts[9], **dicts[8], **dicts[7], **dicts[6],
                 **dicts[5], **dicts[4], **dicts[3], **dicts[2],
                 **dicts[1], **dicts[0] }
    elif length == 9:
        return { **extras,   **dicts[8], **dicts[7], **dicts[6],
                 **dicts[5], **dicts[4], **dicts[3], **dicts[2],
                 **dicts[1], **dicts[0] }
    elif length == 8:
        return { **extras,   **dicts[7], **dicts[6],
                 **dicts[5], **dicts[4], **dicts[3], **dicts[2],
                 **dicts[1], **dicts[0] }
    elif length == 7:
        return { **extras,   **dicts[6],
                 **dicts[5], **dicts[4], **dicts[3], **dicts[2],
                 **dicts[1], **dicts[0] }
    elif length == 6:
        return { **extras,
                 **dicts[5], **dicts[4], **dicts[3], **dicts[2],
                 **dicts[1], **dicts[0] }
    elif length == 5:
        return { **extras,   **dicts[4], **dicts[3], **dicts[2],
                 **dicts[1], **dicts[0] }
    elif length == 4:
        return { **extras,   **dicts[3], **dicts[2],
                 **dicts[1], **dicts[0] }
    elif length == 3:
        return { **extras,   **dicts[2],
                 **dicts[1], **dicts[0] }
    elif length == 2:
        return { **extras,   **dicts[1], **dicts[0] }
    elif length == 1:
        return { **extras,   **dicts[0] }
    else:
        merged = { **extras }
        for d in dicts:
            merged = { **merged, **d }
    return merged

@export
def merge_two(one, two, cls=dict):
    """ Merge two dictionaries into an instance of the specified class.
        
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
    cls = overrides.pop('cls', dict)
    return merge_as(*dicts, cls=cls, **overrides)

# DICT STUFF: asdict(…)

@export
def asdict(thing): # pragma: no cover
    """ asdict(thing) → returns either thing, thing.__dict__, or dict(thing) as necessary """
    from clu.predicates import haspyattr, or_none, typeof
    from clu.typology import ismapping
    from clu.typespace.namespace import isnamespace
    if typeof(thing) is thing:
        return thing
    if isnamespace(thing):
        return dict(thing.__dict__)
    if hasattr(thing, '_asdict'):
        return asdict(thing._asdict())
    if hasattr(thing, 'to_dict'):
        return asdict(thing.to_dict())
    if hasattr(thing, 'dict'):
        return asdict(thing.dict)
    if ischainmap(thing):
        return set(iterchain(thing.maps))
    if ismapping(thing):
        return dict(thing)
    if callable(or_none(thing, 'items')):
        return dict(thing.items())
    if haspyattr(thing, 'dict'):
        return asdict(thing.__dict__)
    if isinstance(thing, dict):
        return thing
    return dict(thing)

with exporter as export:
    
    export(reprizer,    name='reprizer')
    export(cmshortrepr, name='cmshortrepr')
    export(cmrepr,      name='cmrepr',          doc="Return the “core” repr for any descendant ChainMap type.")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.constants.consts import TEST_PATH
    from clu.constants.data import XDGS
    from clu.fs.filesystem import Directory
    from clu.predicates import try_items
    from clu.testing.utils import inline
    # from clu.testing.utils import format_environment
    import os
    
    stash = {}
    
    @inline.fixture
    def dict_arbitrary():
        """ Return an arbitrary flat dictionary """
        return {
            'yo'    : "dogg",
            'i'     : "heard",
            'you'   : "liked",
            'dict'  : "chains"
        }
    
    @inline.fixture
    def fsdata():
        """ Return the path to testing data """
        return Directory(TEST_PATH).subdirectory('data')
    
    @inline.fixture
    def environment():
        """ Return the environment access dict """
        for key in XDGS:
            if key in os.environ:
                del os.environ[key]
        return os.environ
    
    @inline.precheck
    def stash_environment():
        """ Stash environment state before testing """
        nonlocal stash
        stash = os.environ.copy()
    
    @inline
    def test_one():
        """ Shallow clone membership check """
        chain0 = ChainMap(dict_arbitrary(),
                                  fsdata(),
                             environment())
        
        chain1 = chain0.clone()
        assert len(chain0) == len(chain1)
        
        for key in chain0.keys():
            assert key in chain0
            assert key in chain1
            
            # N.B. SLOW AS FUCK:
            assert key in chain0.flatten()
            
            assert try_items(key, *chain0.maps, default=None) == try_items(key, *chain1.maps, default=None)
            assert try_items(key, *chain0.maps, default=None) == chain0[key]
            assert try_items(key, *chain0.maps, default=None) == chain1[key]
    
    @inline
    def test_two():
        """ Deep clone membership check """
        chain0 = ChainMap(dict_arbitrary(),
                                  fsdata(),
                             environment())
        
        chainX = chain0.clone(deep=True)
        assert len(chain0) == len(chainX)
        
        for key in chain0.keys():
            assert key in chain0
            assert key in chainX
            
            # N.B. SLOW AS FUCK:
            # assert key in chain0.flatten()
            
            assert try_items(key, *chain0.maps, default=None) == try_items(key, *chainX.maps, default=None)
            assert try_items(key, *chain0.maps, default=None) == chain0[key]
            assert try_items(key, *chain0.maps, default=None) == chainX[key]
    
    @inline
    def test_three():
        """ Equality comparisons across the board """
        from clu.config.keymap import flatdict, Flat
        from itertools import product
        
        chain0 = ChainMap(dict_arbitrary(),
                          Flat(flatdict()))
        chain1 = chain0.clone()
        chainX = chain0.clone(deep=True)
        chainZ = ChainMap(dict_arbitrary(),
                          Flat(flatdict()))
        
        chains = (chain0, chain1, chainX, chainZ)
        
        # Assert that they’re all equal to one another:
        for first, second in product(chains, chains):
            if first is not second:
                assert first == second
        
        print("REPR»CHAIN0:")
        print()
        print(repr(chain0))
        print()
    
    @inline
    def test_four_experimental():
        """ Nested map source for ChainMap """
        from clu.config.keymap import nestedmaps
        
        chainN = ChainMap(nestedmaps(), {})
        
        print("REPR»CHAINÑ:")
        print()
        print(repr(chainN))
        print()
    
    @inline
    def test_five():
        """ Compatibility checks with “collections.ChainMap” """
        from clu.config.keymap import flatdict, Flat
        
        overrides = { 'WTF' : 'HAX' }
        
        chain0 = ChainMap(dict_arbitrary(), Flat(flatdict()), **overrides)
        chainO = collections.ChainMap(dict_arbitrary(), Flat(flatdict()), overrides)
        
        assert len(chain0) == len(chainO)
        
        for key in chain0.keys():
            assert chain0[key] == chainO[key]
        
        chainZ = ChainMap(chainO)
        
        assert chainZ == chain0
        assert chainZ == chainO
        
        repr_instance = ChainRepr()
        
        print("REPR»CHAIN-OH:")
        print()
        print(repr_instance.repr(chainO))
        print()
    
    @inline
    def test_six_experimental():
        """ Parity checks for experimental `ChainMapPlusPlus` """
        chain0 = ChainMapPlusPlus(dict_arbitrary(),
                                          fsdata(),
                                     environment())
        
        chain1 = chain0.clone()
        assert len(chain0) == len(chain1)
        
        for key in chain0.keys():
            assert key in chain0
            assert key in chain1
            
            # N.B. SLOW AS FUCK:
            # assert key in chain0.flatten()
            
            assert try_items(key, *chain0.maps, default=None) == try_items(key, *chain1.maps, default=None)
            assert try_items(key, *chain0.maps, default=None) == chain0[key]
            assert try_items(key, *chain0.maps, default=None) == chain1[key]
    
    @inline
    def test_seven_experimental():
        """ Equality comparisons with `ChainMapPlusPlus` """
        from clu.config.keymap import flatdict, Flat
        from itertools import product
        
        chain0 = ChainMapPlusPlus(dict_arbitrary(),
                                  Flat(flatdict()))
        chain1 = chain0.clone()
        chainX = chain0.clone(deep=True)
        
        chain00 = ChainMap(dict_arbitrary(),
                           Flat(flatdict()))
        chain11 = chain00.clone()
        chainXX = chain00.clone(deep=True)
        
        pp = (chain0,  chain1,  chainX)
        cm = (chain00, chain11, chainXX)
        
        # Assert that they’re all equal to one another:
        for first, second in product(pp+cm, cm+pp):
            if first is not second:
                assert first == second
        
        print("REPR»CHAIN0:")
        print()
        print(repr(chain0))
        print()
    
    @inline
    def test_eight():
        """ Check OrderedMappingView reversals """
        for key0, key1 in zip(reversed(fsdata().keys()), reversed(fsdata())):
            assert key0 == key1
        
        for val0, key1 in zip(reversed(fsdata().values()), reversed(fsdata())):
            assert val0 == fsdata()[key1]
        
        for items0, key1 in zip(reversed(fsdata().items()), reversed(fsdata())):
            key0, val0 = items0
            assert key0 == key1
            assert val0 == fsdata()[key1]
    
    @inline
    def test_nine():
        """ Check OrderedMappingView indexing """
        for idx, key in enumerate(fsdata().keys()):
            val = fsdata()[key]
            assert key == fsdata().keys()[idx]
            assert val == fsdata().values()[idx]
            key0, val0 = fsdata().items()[idx]
            assert key == key0
            assert val == val0
    
    @inline.diagnostic
    def restore_environment():
        """ Restore environment from stashed values """
        os.environ = stash
    
    # Run all inline tests, return POSIX status
    return inline.test(10)

if __name__ == '__main__':
    sys.exit(test())