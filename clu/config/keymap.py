# -*- coding: utf-8 -*-
from __future__ import print_function

import clu.abstract
import copy
import sys, re

from clu.config import abc, ns
from clu.config.keymaputils import thaw_name, thaw_class, freeze_name, freeze_class
from clu.constants import consts
from clu.predicates import tuplize, typeof
from clu.typology import ismapping, isset
from clu.exporting import Exporter, sysmods, itermodule

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
        key, fragments = ns.unpack_ns(nskey)
        yield fragments + [key, mapping[nskey]]

@export
def articulate(mapping, walker=flatwalk):
    """ Articulate a given mapping with namespaced keys into
        one that is nested. By default, use the “flatwalk(…)”
        walking function.
    """
    tree = {}
    for *fragments, key, value in walker(mapping):
        d = tree
        for fragment in fragments:
            try:
                d = d[fragment]
            except KeyError:
                d[fragment] = {}
                d = d[fragment]
        d[key] = value
    return tree

@export
class FrozenFlat(abc.FrozenKeyMap, clu.abstract.ReprWrapper,
                                   clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class with a flat internal topology. """
    
    __slots__ = 'dictionary'
    
    def __init__(self, dictionary=None, **updates):
        """ Initialize a flat KeyMap instance from a target dictionary.
            
            The dictionary can contain normal key-value items as long as the
            keys are strings; namespaces can be specified per-key as per the
            output of ‘pack_ns(…)’ (q.v. function definition supra.)
        """
        # Call up:
        super().__init__(**updates)
        
        # Sort out our passed-in dictionary:
        if hasattr(dictionary, 'dictionary'):
            dictionary = getattr(dictionary, 'dictionary')
        elif hasattr(dictionary, 'flatten'):
            dictionary = getattr(dictionary.flatten(), 'dictionary')
        
        # Assign things:
        self.dictionary = dict(dictionary or {})
        if updates:
            self.dictionary.update(**updates)
    
    def thaw(self):
        return thaw_class(type(self))(dictionary=copy.copy(self.dictionary))
    
    def nestify(self, cls=None, walker=flatwalk):
        """ Articulate a flattened KeyMap instance out into one that is nested. """
        if cls is None:
            cls = FrozenNested
        return cls(tree=articulate(self.dictionary, walker=walker),
                nskeyset=frozenset(self.keys()))
    
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
        return copy.copy(self.dictionary)

@export
class Flat(FrozenFlat, abc.KeyMap):
    
    """ A concrete mutable KeyMap class with a flat internal topology. """
    
    def freeze(self):
        return freeze_class(type(self))(dictionary=copy.copy(self.dictionary))
    
    def __setitem__(self, nskey, value):
        self.dictionary[nskey] = value
    
    def __delitem__(self, nskey):
        del self.dictionary[nskey]
    
    def keys(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all keys in the mapping,
            or over only those keys in the mapping which match the specified
            namespace values.
        """
        if unprefixed:
            return super().keys(unprefixed=True)
        if not namespaces:
            return super().keys()
        return (key for key in self.dictionary.keys() \
                if any(ns.namespace_matches(key, namespace) for namespace in namespaces))
    
    def items(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all key/value pairs in the
            mapping, or over only those key/value pairs in the mapping whose
            keys match the specified namespace values.
        """
        if unprefixed:
            return super().items(unprefixed=True)
        if not namespaces:
            return super().items()
        return ((key, value) for key, value in self.dictionary.items() \
                if any(ns.namespace_matches(key, namespace) for namespace in namespaces))
    
    def values(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all values in the mapping,
            or over only those values in the mapping whose keys match the
            specified namespace values.
        """
        if unprefixed:
            return super().values(unprefixed=True)
        if not namespaces:
            return super().values()
        return (value for key, value in self.dictionary.items() \
                if any(ns.namespace_matches(key, namespace) for namespace in namespaces))

@export
def dictify(treeish, cls=dict):
    """ Recursively convert a possibly nested mapping to dicts.
        
        Standard Python dicts will be created by default; specify
        a custom class with the “cls” argument to use your own.
    """
    if ismapping(treeish):
        return cls({ key : dictify(value, cls=cls) for key, value in treeish.items() })
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
class FrozenNested(abc.NamespaceWalker, clu.abstract.ReprWrapper,
                                        clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class with an articulated –
        or, if you will, a nested – internal topology.
    """
    
    __slots__ = ('tree', 'nskeys')
    
    @classmethod
    def from_dict(cls, instance_dict):
        """ Used by `clu.config.codecs` to deserialize keymaps """
        out = cls(nskeyset=instance_dict.get('nskeyset', None))
        out.tree = instance_dict['tree']
        return out
    
    def __init__(self, tree=None, *, nskeyset=None, **updates):
        """ Initialize an articulated (née “nested”) KeyMap instance from a
            target nested dictionary (or a “tree” of dicts).
        """
        # Call up:
        super().__init__()
        
        # Sort out the nature of the input:
        if hasattr(tree, 'tree'):
            tree = getattr(tree, 'tree')
        elif hasattr(tree, 'nestify'):
            tree = getattr(tree.nestify(), 'tree')
        
        # Assign, and deal with updates:
        self.tree = dictify(tree or {})
        if updates:
            for nskey, value in updates.items():
                key, fragments = ns.unpack_ns(nskey)
                d = self.tree
                for fragment in fragments:
                    try:
                        d = d[fragment]
                    except KeyError:
                        d[fragment] = {}
                        d = d[fragment]
                d[key] = value
        
        # Keep the keyset we got:
        self.nskeys = nskeyset and frozenset(nskeyset) or None
    
    def walk(self):
        """ Iteratively walk the nested KeyMap’s tree of dicts. """
        yield from mapwalk(self.tree)
    
    def nskeyset(self):
        """ Walk the tree, and assemble a set of the namespaced keys """
        yield from (ns.pack_ns(key, *fragments) \
               for *fragments, key, value in self.walk() \
                   if not ismapping(value))
    
    def thaw(self):
        return thaw_class(type(self))(tree=copy.copy(self.tree),
                                  nskeyset=copy.copy(self.nskeys))
    
    def submap(self, *namespaces, unprefixed=False, cls=None):
        """ Return a flattened mapping, if possible a mutable one,
            containing only items with keys matching the specified
            namespaces (as namespaced:key:paths).
        """
        # We’ll need this later:
        if not cls:
            cls = freeze_class(type(self))
        
        # Short-circuit for returning unprefixed top-level items:
        if unprefixed:
            return cls({ key: value \
                     for key, value in self.tree.items() \
                         if not ismapping(value) })
        
        # If it’s not unprefixed, and we have no namespaces,
        # we cough up a new instance with our data:
        if not namespaces:
            return cls(self.tree, nskeyset=self.nskeys)
        
        # Our namespaces, their output data:
        ours = frozenset(self._get_namespace_foset().things)
        theirs = {}
        
        # Go through the namespaces we were passed, and copy anything
        # we have that matches those namespaces into a new output dict –
        # wholesale and sans any namespaced-key prefixes:
        for namespace in namespaces:
            if namespace not in ours:
                continue
            d = self.tree
            for fragment in ns.split_ns(namespace):
                d = d[fragment]
            theirs[namespace] = d
        
        # Return a (possibly frozen) instance containing the specified
        # namespaced data, as a namespaced instance:
        return cls(theirs)
    
    def inner_repr(self):
        return repr(self.tree)
    
    def clone(self, deep=False, memo=None):
        copier = deep and copy.deepcopy or copy.copy
        return type(self)(tree=copier(self.tree),
                      nskeyset=copier(self.nskeys))
    
    def to_dict(self):
        """ Used by `clu.config.codecs` to serialize the keymap """
        return { 'tree'     : copy.copy(self.tree),
                 'nskeyset' : None }
    
    def __contains__(self, nskey):
        if not isset(self.nskeys):
            self.nskeys = frozenset(self.nskeyset())
        return nskey in self.nskeys
    
    def __getitem__(self, nskey):
        key, fragments = ns.unpack_ns(nskey)
        d = self.tree
        for fragment in fragments:
            d = d[fragment]
        return d[key]

@export
class Nested(FrozenNested, abc.KeyMap):
    
    """ A concrete mutable KeyMap class with an articulated (or nested)
        internal topology.
    """
    
    def __init__(self, tree=None, *, nskeyset=None, **updates):
        """ Initialize an articulated (née “nested”) KeyMap instance from a
            target nested dictionary (or a “tree” of dicts).
        """
        # Call up, without passing nskeyset:
        super().__init__(tree=tree, nskeyset=None, **updates)
        
        # Mutable-ize the keyset:
        self.nskeys = nskeyset and set(nskeyset) or set(self.nskeyset())
    
    def freeze(self):
        return freeze_class(type(self))(tree=copy.copy(self.tree),
                                    nskeyset=frozenset(self.nskeys))
    
    def __setitem__(self, nskey, value):
        key, fragments = ns.unpack_ns(nskey)
        d = self.tree
        for fragment in fragments:
            try:
                d = d[fragment]
            except KeyError:
                d[fragment] = {}
                d = d[fragment]
        d[key] = value
        self.nskeys.add(nskey)
    
    def __delitem__(self, nskey):
        if nskey not in self:
            raise KeyError(nskey)
        key, fragments = ns.unpack_ns(nskey)
        d = self.tree
        for fragment in fragments:
            d = d[fragment]
        del d[key]
        self.nskeys.remove(nskey)

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
        *fragments, key, value = mappingpath
        nskey = ns.pack_ns(key, *fragments)
        out[nskey] = value
    return out

@inline.fixture
def frozenclasses():
    """ Scan `sys.modules` for “frozen”-looking types """
    from clu.naming import qualified_name
    seen = set()
    out = list()
    for module in sysmods():
        for key, value in itermodule(module):
            if key.startswith("rozen", 1):
                if key not in seen:
                    seen.add(key)
                    modname = qualified_name(module)
                    if modname == '__main__':
                        modname = exporter.dotpath
                    out.append((key, value, modname, thaw_name(key)))
    return tuple(out)

@inline.fixture
def frozenclassnames():
    """ Same as the `frozenclasses()` fixture but with just the names """
    out = list()
    for quadruple in frozenclasses():
        out.append((quadruple[0], quadruple[2], quadruple[3]))
    return tuple(out)

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
        """ Nested maps fixture contents """
        pprint(nestedmaps())
    
    @inline.precheck
    def show_frozenclasses():
        """ Frozen classes (by name) found in sys.modules """
        from clu.config.env import FrozenEnviron
        
        freezer = tuple(frozenclasses())
        for popsicle in freezer:
            pprint(tuplize(popsicle[0], popsicle[1]))

        print()
        
        fridge = tuple(frozenclassnames())
        for meat in fridge:
            pprint(meat)
    
    @inline.precheck
    def show_mapwalk_content():
        """ Verbose “mapwalk(…)” content check """
        for mappingpath in mapwalk(nestedmaps()):
            *fragments, key, value = mappingpath
            nskey = ns.pack_ns(key, *fragments)
            print("NAMESPACES:", ", ".join(fragments))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_mapwalk():
        """ Simple “mapwalk(…)” content """
        dictderive = tuple(mapwalk(nestedmaps()))
        return dictderive
    
    @inline
    def test_frozenflat_nested_eq():
        """ FrozenFlat and Nested equivalence """
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps()):
            *fragments, key, value = mappingpath
            nskey = ns.pack_ns(key, *fragments)
            flat_dict[nskey] = value
        
        assert flat_dict == flatdict()
        
        flat = FrozenFlat(flat_dict)
        nested = Nested(flat)
        flattened = nested.flatten()
        
        assert flattened == flat
        assert flattened.dictionary == flatdict()
        assert flattened.thaw() == flat
        
        assert len(flat) == len(nested)
    
    @inline
    def test_flat_nested_eq():
        """ Flat, FrozenFlat and Nested equivalence """
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps()):
            *fragments, key, value = mappingpath
            nskey = ns.pack_ns(key, *fragments)
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
        nested = FrozenNested(tree=nestedmaps())
        
        for mappingpath in mapwalk(nested.tree):
            *fragments, key, value = mappingpath
            nskey = ns.pack_ns(key, *fragments)
            assert nskey in nested
    
    @inline
    def test_nested_contains():
        """ Nested contains namespaced key """
        nested = Nested(tree=nestedmaps(), **arbitrary())
        
        for mappingpath in mapwalk(nested.tree):
            *fragments, key, value = mappingpath
            nskey = ns.pack_ns(key, *fragments)
            assert nskey in nested
    
    @inline
    def test_frozennested_flat_eq():
        """ FrozenNested and Flat roundtrip commutativity """
        nested = FrozenNested(tree=nestedmaps())
        flat = Flat(nested)
        renested = flat.nestify()
        assert renested == nested
        assert renested.thaw() == nested
    
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
        """ Check submap(…) equality """
        nested = Nested(tree=nestedmaps())
        frozen_nested = nested.freeze()
        
        assert frozen_nested.submap() == dict(frozen_nested)
        assert nested.submap('body') == frozen_nested.submap('body')
        assert nested.submap('body:declare_i') == frozen_nested.submap('body:declare_i')
        assert nested.submap('WTF:HAX') == {}
        assert frozen_nested.submap('WTF:HAX') == {}
        assert nested.submap(unprefixed=True) == FrozenNested({ 'type' : 'Program' })
        assert nested.submap() == dict(nested)
    
    @inline.diagnostic
    def show_nested_contents():
        """ Evaluate submap(…) contents """
        nested = Nested(tree=nestedmaps())
        frozen_nested = nested.freeze()
        
        typ0 = typeof(nested).__name__
        print(f"NESTED ({typ0}) SUBMAP:")
        print(nested.submap('body:declare_i'))
        print()
        
        typ1 = typeof(frozen_nested).__name__
        print(f"FROZEN NESTED ({typ1}) SUBMAP:")
        print(frozen_nested.submap('body:declare_i'))
        print()
        
        print(f"NESTED ({typ0}) TREE:")
        pprint(nested.tree)
        print()
        
        print(f"FROZEN NESTED ({typ1}) TREE:")
        pprint(nested.tree)
        print()
    
    @inline.diagnostic
    def show_function_cache_stats():
        """ Show stats for the cached freeze/thaw functions """
        from clu.naming import nameof
        
        # Which functions?
        cached = (thaw_name, thaw_class,
                  freeze_name, freeze_class)
        total = len(cached)
        
        # Let’s see them:
        for idx, function in enumerate(cached):
            if idx > 0:
                print()
            print(f"FUNCTION CACHE INFO: {nameof(function)} ({idx+1} of {total})")
            print(function.cache_info())
    
    @inline.diagnostic
    def show_fixture_cache_stats():
        """ Show the per-fixture-function cache stats """
        total = len(inline.fixtures)
        for idx, name in enumerate(inline.fixtures.keys()):
            if idx > 0:
                print()
            print(f"FIXTURE CACHE INFO: {name} ({idx+1} of {total})")
            print(inline.fixtures[name].cache_info())
    
    # Run all inline tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
