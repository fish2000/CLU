# -*- coding: utf-8 -*-
from __future__ import print_function

import clu.abstract
import copy
import sys

from clu.config.abc import FrozenKeyMap, KeyMap, NamespaceWalker
from clu.config.ns import concatenate_ns, unpack_ns, pack_ns
from clu.typology import ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# CONCRETE SUBCLASSES: FrozenFlat and Flat

@export
def flatwalk(mapping):
    """ Iteratively walk a flat mapping with namespaced keys,
        as found in a FrozenFlat or Flat instance.
        
        Based on https://stackoverflow.com/a/12507546/298171
    """
    for nskey in mapping.keys():
        key, namespaces = unpack_ns(nskey)
        yield namespaces + [key, mapping[nskey]]

@export
def articulate(mapping):
    """ Articulate a flat mapping with namespaced keys into
        one that is nested.
    """
    tree = {}
    for *namespaces, key, value in flatwalk(mapping):
        d = tree
        for namespace in namespaces:
            try:
                d = d[namespace]
            except KeyError:
                d[namespace] = {}
                d = d[namespace]
        d[key] = value
    return tree

@export
class FrozenFlat(FrozenKeyMap, clu.abstract.ReprWrapper,
                               clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class with a flat internal topology. """
    
    __slots__ = 'dictionary'
    
    def __init__(self, dictionary=None, **updates):
        """ Initialize a flat KeyMap instance from a target dictionary.
            
            The dictionary can contain normal key-value items as long as the
            keys are strings; namespaces can be specified per-key as per the
            output of ‘pack_ns(…)’ (q.v. function definition supra.)
        """
        try:
            super().__init__(**updates)
        except TypeError:
            super().__init__()
        if hasattr(dictionary, 'dictionary'):
            dictionary = getattr(dictionary, 'dictionary')
        elif hasattr(dictionary, 'flatten'):
            dictionary = getattr(dictionary.flatten(), 'dictionary')
        self.dictionary = dict(dictionary or {})
        if updates:
            self.dictionary.update(**updates)
    
    def nestify(self, cls=None):
        """ Articulate a flattened KeyMap instance out into one that is nested. """
        if cls is None:
            cls = FrozenNested
        return cls(tree=articulate(self.dictionary))
    
    def __iter__(self):
        yield from self.dictionary
    
    def __reversed__(self):
        yield from reversed(self.dictionary.keys())
    
    def __len__(self):
        return len(self.dictionary)
    
    def __contains__(self, nskey):
        return nskey in self.dictionary
    
    def __getitem__(self, nskey):
        return self.dictionary[nskey]
    
    def inner_repr(self):
        return repr(self.dictionary)
    
    def clone(self, deep=False, memo=None):
        copier = deep and copy.deepcopy or copy.copy
        return type(self)(dictionary=copier(self.dictionary))
    
    def to_dict(self):
        """ Used by `clu.config.codecs` to serialize the keymap """
        return copy.deepcopy(self.dictionary)

@export
class Flat(FrozenFlat, KeyMap):
    
    """ A concrete mutable KeyMap class with a flat internal topology. """
    
    def freeze(self):
        return FrozenFlat(dictionary=copy.deepcopy(self.dictionary))
    
    def __setitem__(self, nskey, value):
        self.dictionary[nskey] = value
    
    def __delitem__(self, nskey):
        del self.dictionary[nskey]

@export
def dictify(treeish):
    """ Recursively convert a possibly nested mapping to standard dicts. """
    if ismapping(treeish):
        return { key : dictify(value) for key, value in treeish.items() }
    return treeish

@export
def mapwalk(mapping, pre=None):
    """ Iteratively walk a nested mapping.
        
        Based on https://stackoverflow.com/a/12507546/298171
    """
    pre = pre and pre[:] or []
    if ismapping(mapping):
        for key, value in mapping.items():
            if ismapping(value):
                yield from mapwalk(value, pre + [key])
            else:
                yield pre + [key, value]
    else:
        yield mapping

# CONCRETE SUBCLASSES: FrozenNested and Nested

@export
class FrozenNested(NamespaceWalker, clu.abstract.ReprWrapper,
                                    clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class with an articulated –
        or, if you will, a nested – internal topology.
    """
    
    __slots__ = 'tree'
    
    def __init__(self, tree=None, **updates):
        """ Initialize an articulated (née “nested”) KeyMap instance from a
            target nested dictionary (or a “tree” of dicts).
        """
        try:
            super().__init__(**updates)
        except TypeError:
            super().__init__()
        if hasattr(tree, 'tree'):
            tree = getattr(tree, 'tree')
        elif hasattr(tree, 'nestify'):
            tree = getattr(tree.nestify(), 'tree')
        self.tree = dictify(dict(tree or {}))
        if updates:
            self.tree.update(**updates)
    
    def walk(self):
        """ Iteratively walk the nested KeyMap’s tree of dicts. """
        yield from mapwalk(self.tree)
    
    def submap(self, *namespaces, unprefixed=False):
        """ Return a flattened dict containing only the namespaced items. """
        if unprefixed:
            return { key : value for key, value in self.tree.items() \
                                  if not ismapping(value) }
        if not namespaces:
            return dict(self)
        if not concatenate_ns(*namespaces) in self.namespaces():
            return {}
        d = self.tree
        for namespace in namespaces:
            d = d[namespace]
        return { pack_ns(key, *namespaces) : value for key, value in d.items() }
    
    def inner_repr(self):
        return repr(self.tree)
    
    def clone(self, deep=False, memo=None):
        copier = deep and copy.deepcopy or copy.copy
        return type(self)(tree=copier(self.tree))
    
    def to_dict(self):
        """ Used by `clu.config.codecs` to serialize the keymap """
        return copy.deepcopy(self.tree)
    
    def __contains__(self, nskey):
        key, namespaces = unpack_ns(nskey)
        if not namespaces:
            # Test for mappings to prevent false positives:
            return not ismapping(self.tree.get(key, {}))
        d = self.tree
        for namespace in namespaces:
            try:
                d = d[namespace]
            except KeyError:
                return False
        # Test for mappings to prevent false positives:
        return not ismapping(d.get(key, {}))
    
    def __getitem__(self, nskey):
        key, namespaces = unpack_ns(nskey)
        if not namespaces:
            return self.tree[key]
        d = self.tree
        for namespace in namespaces:
            d = d[namespace]
        return d[key]

@export
class Nested(FrozenNested, KeyMap):
    
    """ A concrete mutable KeyMap class with an articulated (or nested)
        internal topology.
    """
    
    def freeze(self):
        return FrozenNested(tree=copy.deepcopy(self.tree))
    
    def __setitem__(self, nskey, value):
        key, namespaces = unpack_ns(nskey)
        if not namespaces:
            self.tree[key] = value
        else:
            d = self.tree
            for namespace in namespaces:
                try:
                    d = d[namespace]
                except KeyError:
                    d[namespace] = {}
                    d = d[namespace]
            d[key] = value
    
    def __delitem__(self, nskey):
        if nskey in self:
            key, namespaces = unpack_ns(nskey)
            if not namespaces:
                del self.tree[key]
            else:
                d = self.tree
                for namespace in namespaces:
                    d = d[namespace]
                del d[key]
        else:
            raise KeyError(nskey)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

from clu.testing.utils import inline

@inline.fixture
def nestedmaps():
    """ Nested-dictionary fixture function """
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
    """ Flat-dictionary fixture function """
    out = {}
    for mappingpath in mapwalk(nestedmaps()):
        *namespaces, key, value = mappingpath
        nskey = pack_ns(key, *namespaces)
        out[nskey] = value
    return out

@inline.fixture
def arbitrary():
    return {
        'yo'     : 'dogg',
        'iheard' : 'you like dict literals'
    }

def test():
    
    from pprint import pprint
    
    @inline.precheck
    def show_nestedmaps():
        print("Nested maps fixture output:")
        pprint(nestedmaps())
    
    @inline
    def test_mapwalk():
        """ Simple “mapwalk(…)” content """
        dictderive = tuple(mapwalk(nestedmaps()))
        return dictderive
    
    @inline
    def test_mapwalk_content():
        """ Verbose “mapwalk(…)” content check """
        for mappingpath in mapwalk(nestedmaps()):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            print("NAMESPACES:", ", ".join(namespaces))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_frozenflat_nested_eq():
        """ FrozenFlat and Nested equivalence """
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps()):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            flat_dict[nskey] = value
        
        assert flat_dict == flatdict()
        
        flat = FrozenFlat(flat_dict)
        nested = Nested(flat)
        
        # print("FLAT:")
        # pprint(flat)
        # print()
        
        # print("NESTED:")
        # pprint(nested)
        # print()
        
        # print("NESTED FLATTEN:")
        # pprint(nested.flatten())
        # print()
        
        assert nested.flatten() == flat
        assert nested.flatten().dictionary == flatdict()
        assert nested == flat
    
    @inline
    def test_flat_frozenflat_nested_eq():
        """ Flat, FrozenFlat and Nested equivalence """
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps()):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            flat_dict[nskey] = value
        
        assert flat_dict == flatdict()
        
        flat = Flat(flat_dict)
        frozen_flat = flat.freeze()
        assert frozen_flat == flat
        assert frozen_flat.dictionary == flatdict()
        
        nested = flat.nestify()
        flattened = nested.flatten()
        assert flattened == flat
        assert flattened.dictionary == flatdict()
    
    @inline
    def test_frozennested_contains():
        """ FrozenNested contains namespaced key """
        nested = FrozenNested(tree=nestedmaps(), **arbitrary())
        
        for mappingpath in mapwalk(nested.tree):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            assert nskey in nested or nskey in arbitrary()
    
    @inline
    def test_nested_contains():
        """ Nested contains namespaced key """
        nested = Nested(tree=nestedmaps(), **arbitrary())
        
        for mappingpath in mapwalk(nested.tree):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            assert nskey in nested or nskey in arbitrary()
    
    @inline
    def test_frozennested_flat_eq():
        """ FrozenNested and Flat roundtrip commutativity """
        nested = FrozenNested(tree=nestedmaps())
        flat = Flat(nested)
        assert flat.nestify() == nested
        assert flat == nested
    
    @inline
    def test_nested_frozennested_eq():
        """ Nested and FrozenNested commutativity """
        nested = Nested(tree=nestedmaps())
        frozen_nested = nested.freeze()
        assert frozen_nested == nested
        
        flat = nested.flatten()
        renested = flat.nestify()
        assert renested == nested
    
    @inline
    def test_nested_submaps():
        nested = Nested(tree=nestedmaps())
        frozen_nested = nested.freeze()
        
        assert frozen_nested.submap() == dict(frozen_nested)
        assert nested.submap('body') == frozen_nested.submap('body')
        assert nested.submap('body', 'declare_i') == frozen_nested.submap('body', 'declare_i')
        assert nested.submap('WTF', 'HAX') == {}
        assert nested.submap(unprefixed=True) == { 'type' : 'Program' }
        assert nested.submap() == dict(nested)
    
    @inline.diagnostic
    def show_fixture_cache_stats():
        """ Show the per-fixture-function cache stats """
        total = len(inline.fixtures)
        for idx, name in enumerate(inline.fixtures.keys()):
            if idx > 0:
                print()
            print(f"FUNCTION CACHE INFO: {name} ({idx+1} of {total})")
            print(inline.fixtures[name].cache_info())
    
    # Run all inline tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())