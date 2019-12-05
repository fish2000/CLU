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
    
    __slots__ = ('mapping', 'namespaces', 'prefix')
    
    def __init__(self, mapping, *namespaces):
        self.mapping = mapping
        self.namespaces = namespaces
        self.prefix = prefix_for(*namespaces)
    
    def __len__(self):
        if not self.prefix:
            return len(self.mapping)
        return len([key \
                for key in self.mapping \
                 if key.startswith(self.prefix)])
    
    def __getitem__(self, idx):
        return tuple(self)[idx]
    
    def __repr__(self):
        tn = typename(self)
        nslist = ', '.join(self.namespaces)
        ns = bool(self.prefix) and f"<{nslist}>" or ''
        return f"{tn}{ns}({self.mapping!r})"

@export
class KeyMapKeysView(KeyMapViewBase,
                     collections.abc.Set):
    
    @classmethod
    def _from_iterable(cls, iterable):
        return set(iterable)
    
    def __contains__(self, nskey):
        return nskey in self.mapping.submap(*self.namespaces)
    
    def __iter__(self):
        yield from (nskey \
                for nskey in self.mapping \
                 if nskey.startswith(self.prefix))

@export
class KeyMapItemsView(KeyMapViewBase,
                      collections.abc.Set):
    
    @classmethod
    def _from_iterable(cls, iterable):
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
class KeyMapValuesView(KeyMapViewBase,
                       collections.abc.Collection):
    
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

@export
class FrozenKeyMapBase(collections.abc.Mapping,
                       collections.abc.Reversible):
    
    __slots__ = tuple()
    
    @abstract
    def namespaces(self):
        """ Iterate over all of the namespaces defined in the mapping. """
        ...
    
    @abstract
    def __iter__(self):
        ...
    
    @abstract
    def __reversed__(self):
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
    
    def __missing__(self, nskey):
        if DEBUG:
            print(f"__missing__(…): {nskey}")
        raise KeyError(nskey)
    
    def __bool__(self):
        return len(self) > 0

@export
class KeyMapBase(FrozenKeyMapBase):
    
    __slots__ = tuple()
    
    @abstract
    def __setitem__(self, nskey, value):
        ...
    
    @abstract
    def __delitem__(self, nskey):
        ...

@export
class FrozenKeyMap(FrozenKeyMapBase):
    
    __slots__ = tuple()
    
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
class KeyMap(KeyMapBase,
             FrozenKeyMap,
             collections.abc.MutableMapping):
    
    __slots__ = tuple()
    
    def set(self, key, value, *namespaces):
        """ Set a (possibly namespaced) value for a given key. """
        nskey = pack_ns(key, *namespaces)
        self[nskey] = value
    
    def delete(self, key, *namespaces):
        """ Delete a (possibly namespaced) value from the mapping. """
        nskey = pack_ns(key, *namespaces)
        del self[nskey]
    
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
    
    __slots__ = tuplize('dictionary')
    
    def __init__(self, dictionary=None, *args, **kwargs):
        try:
            super(FrozenFlat, self).__init__(*args, **kwargs)
        except TypeError:
            super(FrozenFlat, self).__init__()
        self.dictionary = dict(dictionary or {})
    
    def nestify(self, cls=None):
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
        return type(self)(dictionary=copy.copy(self.dictionary))

@export
class Flat(FrozenFlat, KeyMap):
    
    def __setitem__(self, nskey, value):
        self.dictionary[nskey] = value
    
    def __delitem__(self, nskey):
        del self.dictionary[nskey]

def DefaultTree():
    return collections.defaultdict(DefaultTree)

def dictify(tree):
    return { key : dictify(tree[key]) for key in tree }

@export
def mapwalk(mapping, pre=None):
    """ Iteratively walk a nested mapping.
        Based on https://stackoverflow.com/a/12507546/298171
    """
    pre = pre and pre[:] or []
    if ismapping(mapping):
        for key, value in mapping.items():
            if ismapping(value):
                for map in mapwalk(value, pre + [key]):
                    yield map
            elif isexpandable(value):
                for item in value:
                    for map in mapwalk(item, pre + [key]):
                        yield map
            else:
                yield pre + [key, value]
    else:
        yield mapping

@export
class Nested(FrozenKeyMap, clu.abstract.ReprWrapper,
                           clu.abstract.Cloneable):
    
    def __init__(self, tree=None, *args, **kwargs):
        try:
            super(Nested, self).__init__(*args, **kwargs)
        except TypeError:
            super(Nested, self).__init__()
        self.tree = tree or DefaultTree()
    
    def flatten(self, cls=None):
        plain_kvs = ((key, value) for key, value in self.tree.items() if not ismapping(value))
        namespaced_kvs = iterchain(((pack_ns(nskey, namespace), nsvalue) for nskey, nsvalue in value.items()) \
                                                                         for namespace, value in self.tree.items() \
                                                                          if ismapping(value))
        if cls is None:
            cls = Flat
        return cls(dictionary=dict(chain(plain_kvs, namespaced_kvs)))
    
    # def namespaces(self):
    #     return tuple(sorted(frozenset(key \
    #                               for key, value in self.tree.items() \
    #                                if ismapping(value))))
    
    def inner_repr(self):
        return repr(self.tree)
    
    def clone(self, deep=False, memo=None):
        return type(self)(tree=copy.copy(self.tree))

export(NAMESPACE_SEP, name='NAMESPACE_SEP')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from pprint import pprint
    
    nestedmaps = {'body': [{'declarations': [{'id': {'name': 'i', 'type': 'Identifier'},
                                             'init': {'type': 'Literal', 'value': 2},
                                             'type': 'VariableDeclarator'}],
                           'kind': 'var',
                           'type': 'VariableDeclaration'},
                          {'declarations': [{'id': {'name': 'j', 'type': 'Identifier'},
                                             'init': {'type': 'Literal', 'value': 4},
                                             'type': 'VariableDeclarator'}],
                           'kind': 'var',
                           'type': 'VariableDeclaration'},
                          {'declarations': [{'id': {'name': 'answer', 'type': 'Identifier'},
                                             'init': {'left': {'name': 'i',
                                                               'type': 'Identifier'},
                                                      'operator': '*',
                                                      'right': {'name': 'j',
                                                                'type': 'Identifier'},
                                                      'type': 'BinaryExpression'},
                                             'type': 'VariableDeclarator'}],
                           'kind': 'var',
                           'type': 'VariableDeclaration'}],
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
        
        print("FLAT DICTIONARY:")
        pprint(flat_dict, indent=4)
        print()
        
        flat = FrozenFlat(flat_dict)
        
        print("FLAT INSTANCE:")
        pprint(flat)
        print()
        
        print("FLAT KEYS:")
        pprint(tuple(flat.keys()))
        print()
        
        print("FLAT VALUES:")
        pprint(tuple(flat.values()))
        print()
        
        print("FLAT NAMESPACES:")
        pprint(tuple(flat.namespaces()))
        print()
    
    pprint(nestedmaps)
    
    test_one()
    test_two()
    test_three()

if __name__ == '__main__':
    test()
