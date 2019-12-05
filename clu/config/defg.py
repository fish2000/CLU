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

@export
class NamespacedMappingView(collections.abc.Sized,
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
    
    def __repr__(self):
        tn = typename(self)
        nslist = ', '.join(self.namespaces)
        ns = bool(self.prefix) and f"<{nslist}>" or ''
        return f"{tn}{ns}({self.mapping!r})"

@export
class NamespacedKeysView(NamespacedMappingView,
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
class NamespacedItemsView(NamespacedMappingView,
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
class NamespacedValuesView(NamespacedMappingView,
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


@export
class NamespacedMutableMapping(collections.abc.MutableMapping,
                               collections.abc.Reversible):
    
    __slots__ = tuple()
    
    @staticmethod
    def validate_ns(*namespaces):
        """ Raise a ValueError if any of the given namespaces are invalid. """
        for namespace in namespaces:
            if not namespace.isidentifier():
                raise ValueError(f"Invalid namespace: “{namespace}”")
            if NAMESPACE_SEP in namespace:
                raise ValueError(f"Namespace contains separator: “{namespace}”")
    
    @staticmethod
    def unpack_ns(string):
        """ Unpack a namespaced key into a set of namespaces and a key name.
            
            To wit: if the namespaced key is “yo:dogg:i-heard”, calling “unpack_ns(…)”
            on it will return the tuple ('i-heard', ('yo', 'dogg'));
            
            If the key is not namespaced (like e.g. “wat”) the “unpack_ns(…)”
            call will return the tuple ('wat', tuple()).
        """
        *namespaces, value = string.split(NAMESPACE_SEP)
        return value, tuple(namespaces)
    
    @staticmethod
    def pack_ns(value, *namespaces):
        """ Pack a key and a set of (optional) namespaces into a namespaced key.
            
            To wit: if called as “pack_ns('i-heard, 'yo', 'dogg')” the return
            value will be the string "yo:dogg:i-heard".
            
            If no namespaces are provided (like e.g. “pack_ns('wat')”)
            the return value will be the string "wat".
        """
        itervalue = isexpandable(value) and value or tuplize(value)
        return NAMESPACE_SEP.join(chain(namespaces, itervalue))
    
    @classmethod
    def get_ns(cls, string):
        """ Get the namespace portion of a namespaced key as a packed string. """
        _, namespaces = cls.unpack_ns(string)
        return concatenate(*namespaces)
    
    def get(self, key, *namespaces, default=NoDefault):
        """ Retrieve a (possibly namespaced) value for a given key.
            
            An optional default value may be specified, to be returned
            if the key in question is not found in the mapping.
        """
        nskey = self.pack_ns(key, *namespaces)
        if default is NoDefault:
            return self[nskey]
        if nskey in self:
            return self[nskey]
        return default
    
    def set(self, key, value, *namespaces):
        """ Set a (possibly namespaced) value for a given key. """
        nskey = self.pack_ns(key, *namespaces)
        self[nskey] = value
    
    def delete(self, key, *namespaces):
        """ Delete a (possibly namespaced) value from the mapping. """
        nskey = self.pack_ns(key, *namespaces)
        del self[nskey]
    
    def submap(self, *namespaces):
        """ Return a standard dict containing only the namespaced items. """
        prefix = prefix_for(*namespaces)
        if not prefix:
            return dict(self)
        return { nskey : self[nskey] for nskey in self if nskey.startswith(prefix) }
    
    def keys(self, *namespaces):
        """ Return a namespaced view over either all keys in the mapping,
            or over only those keys in the mapping matching the specified
            namespace values.
        """
        return NamespacedKeysView(self, *namespaces)
    
    def items(self, *namespaces):
        """ Return a namespaced view over either all key/value pairs in the
            mapping, or over only those key/value pairs in the mapping whose
            keys match the specified namespace values.
        """
        return NamespacedItemsView(self, *namespaces)
    
    def values(self, *namespaces):
        """ Return a namespaced view over either all values in the mapping,
            or over only those values in the mapping whose keys match the
            specified namespace values.
        """
        return NamespacedValuesView(self, *namespaces)
    
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
    
    @abstract
    def __setitem__(self, nskey, value):
        ...
    
    @abstract
    def __delitem__(self, nskey):
        ...
    
    def __missing__(self, nskey):
        if DEBUG:
            print(f"__missing__(…): {nskey}")
        raise KeyError(nskey)
    
    def __bool__(self):
        return len(self) > 0

@export
class Flat(NamespacedMutableMapping,
           clu.abstract.ReprWrapper,
           clu.abstract.Cloneable):
    
    def __init__(self, dictionary=None, *args, **kwargs):
        try:
            super(Flat, self).__init__(*args, **kwargs)
        except TypeError:
            super(Flat, self).__init__()
        self.dictionary = dict(dictionary or {})
    
    # def nestify(self, cls=None):
    #     if cls is None:
    #         cls = Nested
    #     out = cls()
    #     out.update(self.dictionary)
    #     return out
    
    def namespaces(self):
        yield from uniquify(sorted([self.get_ns(key) \
                                            for key in self \
                                             if NAMESPACE_SEP in key]))
    
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
    
    def __setitem__(self, nskey, value):
        self.dictionary[nskey] = value
    
    def __delitem__(self, nskey):
        del self.dictionary[nskey]
    
    def inner_repr(self):
        return repr(self.dictionary)
    
    def clone(self, deep=False, memo=None):
        return type(self)(dictionary=copy.copy(self.dictionary))

export(NAMESPACE_SEP, name='NAMESPACE_SEP')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
