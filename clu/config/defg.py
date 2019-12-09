# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain

iterchain = chain.from_iterable

import abc
import clu.abstract
import collections
import collections.abc
import copy

abstract = abc.abstractmethod

from clu.constants.consts import DEBUG, NoDefault
from clu.predicates import isiterable, isexpandable, tuplize, uniquify
from clu.typology import ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

NAMESPACE_SEP = ':'

typename = lambda thing: type(thing).__name__

def concatenate(*namespaces):
    """ Return the given namespace(s), concatenated with the
        namespace separator.
    """
    return NAMESPACE_SEP.join(namespaces)

def prefix_for(*namespaces):
    """ Return the prefix string for the given namespace(s) """
    out = concatenate(*namespaces)
    return out and f"{out}{NAMESPACE_SEP}" or out

def strip_namespace(nskey):
    """ Strip all namespace-related prefixing from a namespaced key """
    return nskey.rpartition(NAMESPACE_SEP)[-1]

@export
class KeyMapViewBase(collections.abc.Sequence,
                     collections.abc.Sized,
                     metaclass=clu.abstract.Slotted):
    
    """ The base class for KeyMap view classes.
        
        These view classes correspond to, but do not inherit directly from,
        the descendants of “collections.abc.MappingView”. They have been
        specially kitted out to deal with KeyMap namespaces: each instance
        has a ‘mapping’ attribute referring to the parent KeyMap instance,
        a ‘namespaces’ iterable attribute with the unconcatenated namespace
        parts for which the instance was allocated, and a ‘prefix’ shortcut
        attribute containing the concatenated namespace parts as a string
        prefix.
        
        Each concrete subclass of KeyMapViewBase registers itself as a
        “virtual subclass” of its corresponding ‘collections.abc’ view
        class, like for good measure.
    """
    
    __slots__ = ('mapping', 'namespaces', 'prefix')
    
    def __init__(self, mapping, *namespaces):
        """ Initialize a view on a KeyMap instance, for a given namespace """
        self.mapping = mapping
        self.namespaces = namespaces
        self.prefix = prefix_for(*namespaces)
    
    @property
    def _mapping(self):
        """ For compatibility with “collections.abc” stuff """
        return self.mapping
    
    def __len__(self):
        if not self.prefix:
            return len(self.mapping)
        return len([key \
                for key in self.mapping \
                 if key.startswith(self.prefix)])
    
    def __getitem__(self, idx):
        return tuple(self)[idx]
    
    @abstract
    def __contains__(self, nskey):
        ...
    
    @abstract
    def __iter__(self):
        ...
    
    def __repr__(self):
        tn = typename(self)
        nslist = ', '.join(self.namespaces)
        ns = bool(self.prefix) and f"<{nslist}>" or ''
        return f"{tn}{ns}({self.mapping!r})"

@export
@collections.abc.KeysView.register
class KeyMapKeysView(KeyMapViewBase,
                     collections.abc.Set):
    
    """ A KeyMap key view. """
    
    @classmethod
    def _from_iterable(cls, iterable):
        # Required by the “collections.abc.Set” API:
        return set(iterable)
    
    def __contains__(self, nskey):
        return nskey in self.mapping.submap(*self.namespaces)
    
    def __iter__(self):
        yield from (nskey \
                for nskey in self.mapping \
                 if nskey.startswith(self.prefix))

@export
@collections.abc.ItemsView.register
class KeyMapItemsView(KeyMapViewBase,
                      collections.abc.Set):
    
    """ A KeyMap items view. """
    
    @classmethod
    def _from_iterable(cls, iterable):
        # Required by the “collections.abc.Set” API:
        return set(iterable)
    
    def __contains__(self, item):
        nskey, value = item
        try:
            contained = self.mapping.submap(*self.namespaces)[nskey]
        except KeyError:
            return False
        else:
            return contained is value or contained == value
    
    def __iter__(self):
        yield from ((nskey, self.mapping[nskey]) \
                 for nskey in self.mapping \
                  if nskey.startswith(self.prefix))

@export
@collections.abc.ValuesView.register
class KeyMapValuesView(KeyMapViewBase,
                       collections.abc.Collection):
    
    """ A KeyMap values view. """
    
    def __contains__(self, value):
        submap = self.mapping.submap(*self.namespaces)
        for nskey in submap:
            contained = submap[nskey]
            if contained is value or contained == value:
                return True
        return False
    
    def __iter__(self):
        yield from (self.mapping[nskey] \
                             for nskey in self.mapping \
                              if nskey.startswith(self.prefix))

# NAMESPACE-MANIPULATION FUNCTION API:

def validate_ns(*namespaces):
    """ Raise a ValueError if any of the given namespaces are invalid. """
    for namespace in namespaces:
        if not namespace.isidentifier():
            raise ValueError(f"Invalid namespace: “{namespace}”")
        if NAMESPACE_SEP in namespace:
            raise ValueError(f"Namespace contains separator: “{namespace}”")

def unpack_ns(string):
    """ Unpack a namespaced key into a set of namespaces and a key name.
        
        To wit: if the namespaced key is “yo:dogg:i-heard”, calling “unpack_ns(…)”
        on it will return the tuple ('i-heard', ('yo', 'dogg'));
        
        If the key is not namespaced (like e.g. “wat”) the “unpack_ns(…)”
        call will return the tuple ('wat', tuple()).
    """
    *namespaces, value = string.split(NAMESPACE_SEP)
    return value, tuple(namespaces)

def pack_ns(value, *namespaces):
    """ Pack a key and a set of (optional) namespaces into a namespaced key.
        
        To wit: if called as “pack_ns('i-heard, 'yo', 'dogg')” the return
        value will be the string "yo:dogg:i-heard".
        
        If no namespaces are provided (like e.g. “pack_ns('wat')”)
        the return value will be the string "wat".
    """
    itervalue = isexpandable(value) and value or tuplize(value)
    return NAMESPACE_SEP.join(chain(namespaces, itervalue))

def get_ns(string):
    """ Get the namespace portion of a namespaced key as a packed string. """
    _, namespaces = unpack_ns(string)
    return concatenate(*namespaces)

def compare_ns(iterone, itertwo):
    """ Boolean predicate to compare a pair of namespace iterables, value-by-value """
    for one, two in zip(iterone, itertwo):
        if one != two and one is not two:
            return False
    return True

@export
class FrozenKeyMapBase(collections.abc.Mapping,
                       collections.abc.Reversible,
                       metaclass=clu.abstract.Slotted):
    
    """ Abstract sub-base interface class for immutable namespaced mappings.
        This is the root of the namespaced-mapping (née “KeyMap”) class tower.
        
        Don’t subclass this, it’s just a bunch of abstract dunder methods and
        other stuff to pass the buck properly from the ‘collections.abc’ bases
        on up to our own API. You, for your purposes, should employ “FrozenKeyMap”
        (without the “Base”) – q.v. the class definition below, sub.
    """
    
    @abstract
    def namespaces(self):
        """ Iterate over all of the namespaces defined in the mapping. """
        ...
    
    @abstract
    def __iter__(self):
        ...
    
    @abstract
    def __len__(self):
        ...
    
    @abstract
    def __contains__(self, nskey):
        ...
    
    @abstract
    def __getitem__(self, nskey):
        ...
    
    def __reversed__(self):
        yield from reversed(tuple(self))
    
    def __missing__(self, nskey):
        if DEBUG:
            print(f"__missing__(…): {nskey}")
        raise KeyError(nskey)
    
    def __bool__(self):
        return len(self) > 0

@export
class KeyMapBase(FrozenKeyMapBase,
                 collections.abc.MutableMapping):
    
    """ Abstract sub-base interface class for mutable namespaced mappings.
        
        Don’t subclass this anemic vestigial thing. You want “KeyMap” (sans
        the “Base”) as your ancestor; see below.
    """
    
    @abstract
    def freeze(self):
        """ Return a “frozen” – or immutable – version of the KeyMap instance. """
        ...
    
    @abstract
    def __setitem__(self, nskey, value):
        ...
    
    @abstract
    def __delitem__(self, nskey):
        ...

@export
class FrozenKeyMap(FrozenKeyMapBase):
    
    """ The abstract base class for frozen – immutable once created – namespaced mappings,
        also known as “FrozenKeyMaps”.
        
        Subclasses must implement a bunch of typical Python dunder methods like e.g.
        ‘__iter__’, ‘__len__’ &c, plus a “namespaces()” method which takes no arguments
        and then iterates in order over all the THATS RIGHT YOU GUESSED IT namespaces
        contained in the KeyMap’s keys.
        
        Optionally one may override ‘__missing__’, which can be kind of interesting,
        and ‘__bool__’ which generally is less so. Q.v. the “FrozenKeyMapBase” source
        supra. for further deets, my doggie
    """
    
    def get(self, key, *namespaces, default=NoDefault):
        """ Retrieve a (possibly namespaced) value for a given key.
            
            An optional default value may be specified, to be returned
            if the key in question is not found in the mapping.
        """
        nskey = pack_ns(key, *namespaces)
        if default is NoDefault:
            return self[nskey]
        if nskey in self:
            return self[nskey]
        return default
    
    def submap(self, *namespaces, unprefixed=False):
        """ Return a standard dict containing only the namespaced items. """
        if unprefixed:
            return { nskey : self[nskey] for nskey in self if NAMESPACE_SEP not in nskey }
        prefix = prefix_for(*namespaces)
        if not prefix:
            return dict(self)
        return { nskey : self[nskey] for nskey in self if nskey.startswith(prefix) }
    
    def keys(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all keys in the mapping,
            or over only those keys in the mapping matching the specified
            namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).keys()
        return KeyMapKeysView(self, *namespaces)
    
    def items(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all key/value pairs in the
            mapping, or over only those key/value pairs in the mapping whose
            keys match the specified namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).items()
        return KeyMapItemsView(self, *namespaces)
    
    def values(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all values in the mapping,
            or over only those values in the mapping whose keys match the
            specified namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).values()
        return KeyMapValuesView(self, *namespaces)
    
    def namespaces(self):
        """ Iterate over all of the namespaces defined in the mapping.
            
            This is the generic implementation. It depends on “__iter__(…)”
            and uses “uniquify(…)” from ‘clu.predicates’, which some might
            consider somewhat inefficient (q.v. “uniquify(…)” predicate
            utility function supra.)
        """
        yield from sorted(uniquify(get_ns(key) \
                                      for key in self \
                                       if NAMESPACE_SEP in key))

@export
class KeyMap(KeyMapBase, FrozenKeyMap):
    
    """ The abstract base class for mutable namespaced mappings (née “KeyMaps”).
        
        Subclasses must implement all the requisite Python dunder methods required by
        the ancestor “FrozenKeyMap”, like e.g. ‘__iter__’, ‘__len__’ &c, plus also a
        “namespaces()” method which takes no arguments and iterates in order over all
        namespaces contained in the KeyMap’s keys.
        
        OK AND FURTHERMORE for mutability, you also need to do your own ‘__setattr__’
        and ‘__delattr__’ (which maybe we’ll make that last one optional as delete
        methods in Python are totally gauche and a sign of a sort of naïve vulgar
        un-Pythonicism, I feel like).
        
        Optionally one may override ‘__missing__’, which can be kind of interesting,
        and ‘__bool__’ which generally is less so. Q.v. the “FrozenKeyMapBase” source
        supra. for further deets, my doggie
    """
    
    def set(self, key, value, *namespaces):
        """ Set a (possibly namespaced) value for a given key. """
        nskey = pack_ns(key, *namespaces)
        self[nskey] = value
    
    def delete(self, key, *namespaces):
        """ Delete a (possibly namespaced) value from the mapping. """
        nskey = pack_ns(key, *namespaces)
        del self[nskey]
    
    def pop(self, key, *namespaces, default=NoDefault):
        """ Pop a (possibly namespaced) value off the mapping
            and eitehr return it or a default if it doesn’t
            exist – raising a KeyError if no default is given.
        """
        value = self.get(key, *namespaces, default=default)
        try:
            self.delete(key, *namespaces)
        except KeyError:
            pass
        return value
    
    def clear(self, *namespaces, unprefixed=False):
        """ Remove all items from the mapping – either in totality,
            or only those matching a specific namespace.
        """
        if unprefixed:
            for key in self.submap(unprefixed=unprefixed).keys():
                del self[key]
            return None
        prefix = prefix_for(*namespaces)
        if not prefix:
            return super().clear()
        for nskey in self:
            if nskey.startswith(prefix):
                del self[nskey]
        return None
    
    def update(self, dictish=NoDefault, **updates):
        """ NamespacedMutableMapping.update([E, ]**F) -> None.
            
            Update D from dict/iterable E and/or F.
        """
        if dictish is not NoDefault:
            if hasattr(dictish, 'items'):
                dictish = dictish.items()
            if not isiterable(dictish):
                raise TypeError(f"{dictish!r} is not iterable")
            for key, value in dictish:
                self[key] = value
        for key, value in updates.items():
            self[key] = value

@export
class FrozenFlat(FrozenKeyMap, clu.abstract.ReprWrapper,
                               clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class with a flat internal topology. """
    
    __slots__ = tuplize('dictionary')
    
    def __init__(self, dictionary=None, *args, **kwargs):
        """ Initialize a flat KeyMap instance from a target dictionary.
            
            The dictionary can contain normal key-value items as long as the
            keys are strings; namespaces can be specified per-key as per the
            output of ‘pack_ns(…)’ (q.v. function definition supra.)
        """
        try:
            super(FrozenFlat, self).__init__(*args, **kwargs)
        except TypeError:
            super(FrozenFlat, self).__init__()
        if hasattr(dictionary, 'dictionary'):
            dictionary = getattr(dictionary, 'dictionary')
        elif hasattr(dictionary, 'flatten'):
            dictionary = getattr(dictionary.flatten(), 'dictionary')
        self.dictionary = dict(dictionary or {})
    
    def nestify(self, cls=None):
        """ Articulate a flattened KeyMap instance out into one that is nested. """
        if cls is None:
            cls = Nested
        out = cls()
        out.update(self.dictionary)
        return out
    
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

@export
class Flat(FrozenFlat, KeyMap):
    
    """ A concrete mutable KeyMap class with a flat internal topology. """
    
    def freeze(self):
        return FrozenFlat(dictionary=copy.deepcopy(self.dictionary))
    
    def __setitem__(self, nskey, value):
        self.dictionary[nskey] = value
    
    def __delitem__(self, nskey):
        del self.dictionary[nskey]

def DefaultTree():
    return collections.defaultdict(DefaultTree)

@export
def dictify(tree):
    if ismapping(tree):
        return { key : dictify(tree[key]) for key in tree }
    return tree

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
            # elif isexpandable(value):
            #     for idx, item in enumerate(value):
            #         yield from mapwalk(item, pre + [key, str(idx)])
            else:
                yield pre + [key, value]
    else:
        yield mapping

@export
class FrozenNested(FrozenKeyMap, clu.abstract.ReprWrapper,
                                 clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class with an articulated –
        or, if you will, a nested – internal topology.
    """
    
    __slots__ = tuplize('tree')
    
    def __init__(self, tree=None, *args, **kwargs):
        """ Initialize an articulated (née “nested”) KeyMap instance from a
            target nested dictionary (or a “tree” of dicts).
        """
        try:
            super(FrozenNested, self).__init__(*args, **kwargs)
        except TypeError:
            super(FrozenNested, self).__init__()
        if hasattr(tree, 'tree'):
            tree = getattr(tree, 'tree')
        elif hasattr(tree, 'nestify'):
            tree = getattr(tree.nestify(), 'tree')
        self.tree = tree or DefaultTree()
    
    def mapwalk(self):
        """ Iteratively walk the nested KeyMap’s tree of dicts. """
        yield from mapwalk(self.tree)
    
    def flatten(self, cls=None):
        """ Dearticulate an articulated KeyMap instance into one that is flat. """
        if cls is None:
            cls = Flat
        out = cls()
        for *namespaces, key, value in self.mapwalk():
            out.set(key, value, *namespaces)
        return out
    
    def namespaces(self):
        """ Iterate over all of the namespaces defined in the mapping. """
        # N.B. Dunno if this is faster or more worth-it than what one finds
        # upstream in the implementation furnished by FrozenKeyMap…
        out = []
        for *namespaces, key, value in self.mapwalk():
            if namespaces:
                out.append(concatenate(*namespaces))
        yield from sorted(uniquify(out))
    
    def __iter__(self):
        for *namespaces, key, value in self.mapwalk():
            yield pack_ns(key, *namespaces)
    
    def __len__(self):
        return len(tuple(self.mapwalk()))
    
    def __contains__(self, nskey):
        key, namespaces = unpack_ns(nskey)
        for *ns, k, value in self.mapwalk():
            if (k == key or k is key):
                if compare_ns(ns, namespaces):
                    return True
        return False
    
    def __getitem__(self, nskey):
        key, namespaces = unpack_ns(nskey)
        for *ns, k, value in self.mapwalk():
            if (k == key or k is key):
                if compare_ns(ns, namespaces):
                    return value
        raise KeyError(nskey)
    
    def inner_repr(self):
        return repr(self.tree)
    
    def clone(self, deep=False, memo=None):
        copier = deep and copy.deepcopy or copy.copy
        return type(self)(tree=copier(self.tree))

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
                    d = d[namespace] = type(d)()
            d[key] = value
    
    def __delitem__(self, nskey):
        key, namespaces = unpack_ns(nskey)
        if not namespaces:
            del self.tree[key]
        else:
            d = self.tree
            for namespace in namespaces:
                d = d[namespace]
            del d[key]

export(NAMESPACE_SEP, name='NAMESPACE_SEP')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from pprint import pprint
    
    nestedmaps = {'body': {'declare_i': {'id': {'name': 'i', 'type': 'Identifier'},
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
                 'type': 'Program'}
    
    @inline
    def test_one():
        dictderive = tuple(mapwalk(nestedmaps))
        return dictderive
    
    @inline
    def test_two():
        for mappingpath in mapwalk(nestedmaps):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            print("NAMESPACES:", ", ".join(namespaces))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_three():
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            flat_dict[nskey] = value
        
        print(f"FLAT DICTIONARY (length={len(flat_dict)}):")
        pprint(flat_dict, indent=4)
        print()
        
        flat = FrozenFlat(flat_dict)
        
        print(f"FLAT FROZEN INSTANCE (length={len(flat)}):")
        pprint(flat)
        print()
        
        keys = tuple(flat.keys())
        print(f"FLAT KEYS (length={len(keys)}):")
        pprint(keys)
        print()
        
        values = tuple(flat.values())
        print(f"FLAT VALUES (length={len(values)}):")
        pprint(values)
        print()
        
        namespaces = tuple(flat.namespaces())
        print(f"FLAT NAMESPACES (length={len(namespaces)}):")
        pprint(namespaces)
        print()
        
        nested = Nested(flat)
        assert nested.flatten() == flat
        # assert nested == flat
    
    @inline
    def test_three_point_five():
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            flat_dict[nskey] = value
        
        print(f"FLAT DICTIONARY (length={len(flat_dict)}):")
        pprint(flat_dict, indent=4)
        print()
        
        flat = Flat(flat_dict)
        
        print(f"FLAT MUTABLE INSTANCE (length={len(flat)}):")
        pprint(flat)
        print()
        
        keys = tuple(flat.keys())
        print(f"FLAT KEYS (length={len(keys)}):")
        pprint(keys)
        print()
        
        values = tuple(flat.values())
        print(f"FLAT VALUES (length={len(values)}):")
        pprint(values)
        print()
        
        namespaces = tuple(flat.namespaces())
        print(f"FLAT NAMESPACES (length={len(namespaces)}):")
        pprint(namespaces)
        print()
        
        frozen_flat = flat.freeze()
        assert frozen_flat == flat
        
        nested = flat.nestify()
        flattened = nested.flatten()
        assert flattened == flat
    
    @inline
    def test_four():
        nested = FrozenNested(tree=nestedmaps)
        
        for mappingpath in mapwalk(nested.tree):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            print("NAMESPACES:", ", ".join(namespaces))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_four_point_five():
        nested = Nested(tree=nestedmaps)
        
        for mappingpath in mapwalk(nested.tree):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            print("NAMESPACES:", ", ".join(namespaces))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_four_point_seven_five():
        nested = FrozenNested(tree=nestedmaps)
        
        print(f"NESTED FROZEN INSTANCE (length={len(nested)}):")
        pprint(nested)
        print()
        
        keys = tuple(nested.keys())
        print(f"NESTED KEYS (length={len(keys)}):")
        pprint(keys)
        print()
        
        values = tuple(nested.values())
        print(f"NESTED VALUES (length={len(values)}):")
        pprint(values)
        print()
        
        namespaces = tuple(nested.namespaces())
        print(f"NESTED NAMESPACES (length={len(namespaces)}):")
        pprint(namespaces)
        print()
        
        flat = Flat(nested)
        assert flat.nestify() == nested
    
    @inline
    def test_five():
        nested = Nested(tree=nestedmaps)
        
        print(f"NESTED MUTABLE INSTANCE (length={len(nested)}):")
        pprint(nested)
        print()
        
        keys = tuple(nested.keys())
        print(f"NESTED KEYS (length={len(keys)}):")
        pprint(keys)
        print()
        
        values = tuple(nested.values())
        print(f"NESTED VALUES (length={len(values)}):")
        pprint(values)
        print()
        
        namespaces = tuple(nested.namespaces())
        print(f"NESTED NAMESPACES (length={len(namespaces)}):")
        pprint(namespaces)
        print()
        
        frozen_nested = nested.freeze()
        assert frozen_nested == nested
        
        flat = nested.flatten()
        renested = flat.nestify()
        assert renested == nested
    
    
    pprint(nestedmaps)
    
    test_one()
    test_two()
    test_three()
    test_three_point_five()
    # test_four()
    # test_four_point_five()
    test_four_point_seven_five()
    test_five()

if __name__ == '__main__':
    test()
