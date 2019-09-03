# -*- coding: utf-8 -*-
from __future__ import print_function
from copy import copy
from itertools import chain

iterchain = chain.from_iterable

import abc
import collections.abc

abstract = abc.abstractmethod

from clu.constants.consts import NoDefault
from clu.naming import nameof
from clu.predicates import isiterable
from clu.typology import ismapping
from clu.exporting import ValueDescriptor, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

NAMESPACE_SEP = ':'

@export
class AppName(abc.ABC):
    
    @classmethod
    def __init_subclass__(cls, appname=None, **kwargs):
        """ Translate the “appname” class-keyword into an “appname” read-only
            descriptor value
        """
        super(AppName, cls).__init_subclass__(**kwargs)
        cls.appname = ValueDescriptor(appname)
    
    def __init__(self, *args, **kwargs):
        """ Stub __init__(…) method, throwing a lookup error for subclasses
            upon which the “appname” value is None
        """
        if type(self).appname is None:
            raise LookupError("Cannot instantiate a base config class "
                              "(appname is None)")

@export
class NamespacedMutableMapping(collections.abc.MutableMapping,
                               collections.abc.Collection):
    
    @staticmethod
    def unpack_ns(string):
        """ Unpack a namespaced key into a namespace name and a key name.
            
            To wit: if the namespaced key is “yo:dogg”, calling “unpack_ns(…)”
            on it will return the tuple ('yo', 'dogg');
            
            If the key is not namespaced (like e.g. “wat”) the “unpack_ns(…)”
            call will return the tuple (None, 'wat').
        """
        if NAMESPACE_SEP not in string:
            return None, string
        return string.split(NAMESPACE_SEP, 1)
    
    @staticmethod
    def pack_ns(string, namespace=None):
        """ Pack a key and an (optional) namespace name into a namespaced key.
            
            To wit: if called as “pack_ns('dogg', namespace='yo')” the return
            value will be the string "yo:dogg".
            
            If “None” is the namespace (like e.g. “pack_ns('wat', namespace=None)”)
            the return value will be the string "wat".
        """
        if namespace is None:
            return string
        return NAMESPACE_SEP.join((namespace, string))
    
    @abstract
    def get(self, key, namespace=None, default=NoDefault):
        """ Retrieve a (possibly namespaced) value for a given key.
            
            An optional default value may be specified, to be returned
            if the key in question is not found in the mapping.
        """
        ...
    
    @abstract
    def set(self, key, value, namespace=None):
        """ Set a (possibly namespaced) value for a given key. """
        ...
    
    def delete(self, key, namespace=None):
        """ Delete a (possibly namespaced) value from the mapping.
            
            N.B. – The default implementation is a no-op. Subclasses must
                   explicitly override this method to allow deletion.
        """
        pass
    
    @abstract
    def keys(self, namespace=None):
        """ Return an iterable generator over either all keys in the mapping,
            or over only those keys in the mapping matching the specified
            namespace value.
        """
        ...
    
    @abstract
    def values(self, namespace=None):
        """ Return an iterable generator over either all values in the mapping,
            or over only those values in the mapping whose keys match the specified
            namespace value.
        """
        ...
    
    def items(self, namespace=None):
        """ Return an iterable generator over either all keys and values in the
            mapping, or over only those values in the mapping whose keys match the
            specified namespace value.
            
            The generator yields the keys and values as two-tuples containing both:
                
                >>> (key, value)
        """
        return zip(self.keys(namespace),
                   self.values(namespace))
    
    @abstract
    def namespaces(self):
        """ Return a sorted tuple listing all of the namespaces defined in
            the mapping.
        """
        ...
    
    def clone(self):
        """ Return a cloned copy of this NamespacedMutableMapping instance. """
        raise NotImplementedError("clone() not implemented")
    
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
    
    def __iter__(self):
        return iter(self.keys())
    
    def __len__(self):
        return len(tuple(self.keys()))
    
    def __contains__(self, key):
        ns, string = self.unpack_ns(key)
        try:
            self.get(string, namespace=ns)
        except KeyError:
            return False
        else:
            return True
    
    def __getitem__(self, key):
        ns, string = self.unpack_ns(key)
        return self.get(string, namespace=ns)
    
    def __setitem__(self, key, value):
        ns, string = self.unpack_ns(key)
        return self.set(string, value, namespace=ns)
    
    def __delitem__(self, key):
        ns, string = self.unpack_ns(key)
        return self.delete(string, namespace=ns)
    
    def __bool__(self):
        return len(self.keys()) > 0

@export
class Flat(NamespacedMutableMapping):
    
    def __init__(self, dictionary=None, *args, **kwargs):
        try:
            super(Flat, self).__init__(*args, **kwargs)
        except TypeError:
            super(Flat, self).__init__()
        self.dictionary = dict(dictionary or {})
    
    def get(self, key, namespace=None, default=NoDefault):
        nskey = self.pack_ns(key, namespace=namespace)
        if default is NoDefault:
            return self.dictionary.get(nskey)
        return self.dictionary.get(nskey, default)
    
    def set(self, key, value, namespace=None):
        nskey = self.pack_ns(key, namespace=namespace)
        self.dictionary[nskey] = value
    
    def delete(self, key, namespace=None):
        nskey = self.pack_ns(key, namespace=namespace)
        del self.dictionary[nskey]
    
    def keys(self, namespace=None):
        if namespace is None:
            return self.dictionary.keys()
        return (key for key in self.dictionary.keys() \
                     if key.startswith(namespace + NAMESPACE_SEP))
    
    def values(self, namespace=None):
        if namespace is None:
            return self.dictionary.values()
        return (value for key, value in self.dictionary.items() \
                       if key.startswith(namespace + NAMESPACE_SEP))
    
    def nestify(self, cls=None):
        if cls is None:
            cls = Nested
        out = cls()
        out.update(self.dictionary)
        return out
    
    def namespaces(self):
        return tuple(sorted(frozenset(self.unpack_ns(key)[0] \
                           for key in self.dictionary.keys() \
                            if NAMESPACE_SEP in key)))
    
    def clone(self):
        return type(self)(dictionary=copy(self.dictionary))
    
    def __repr__(self):
        cnm = nameof(type(self))
        dic = repr(self.dictionary)
        hxa = hex(id(self))
        return f"{cnm}({dic}) @ {hxa}"

@export
class Nested(NamespacedMutableMapping):
    
    def __init__(self, tree=None, *args, **kwargs):
        try:
            super(Nested, self).__init__(*args, **kwargs)
        except TypeError:
            super(Nested, self).__init__()
        self.tree = dict(tree or {})
    
    def get(self, key, namespace=None, default=NoDefault):
        if namespace is None:
            if default is NoDefault:
                return self.tree.get(key)
            return self.tree.get(key, default)
        elif namespace in self.namespaces():
            if default is NoDefault:
                return self.tree[namespace].get(key)
            return self.tree[namespace].get(key, default)
        raise KeyError(f"Unknown namespace: {namespace}")
    
    def set(self, key, value, namespace=None):
        if not key.isidentifier():
            raise KeyError(f"Invalid key: {key}")
        if namespace is None:
            self.tree[key] = value
            return
        if namespace not in self.tree:
            if not namespace.isidentifier():
                raise KeyError(f"Invalid namespace: “{namespace}”")
            self.tree[namespace] = {}
        self.tree[namespace][key] = value
    
    def delete(self, key, namespace=None):
        if namespace is None:
            del self.tree[key]
        elif namespace in self.namespaces():
            del self.tree[namespace][key]
        raise KeyError(f"Unknown namespace: {namespace}")
    
    def keys(self, namespace=None):
        if namespace is None:
            keys = (key for key, value in self.tree.items() if not ismapping(value))
            nskeys = iterchain((self.pack_ns(nskey, namespace=key) for nskey in value.keys()) \
                                                                   for key, value in self.tree.items() \
                                                                    if ismapping(value))
            return chain(keys, nskeys)
        elif namespace in self.namespaces():
            return self.tree[namespace].keys()
        raise KeyError(f"Unknown namespace: {namespace}")
    
    def values(self, namespace=None):
        if namespace is None:
            values = (value for value in self.tree.values() if not ismapping(value))
            nsvalues = iterchain(value.values() for value in self.tree.values() if ismapping(value))
            return chain(values, nsvalues)
        elif namespace in self.namespaces():
            return self.tree[namespace].values()
        raise KeyError(f"Unknown namespace: {namespace}")
    
    def flatten(self, cls=None):
        plain_kvs = ((key, value) for key, value in self.tree.items() if not ismapping(value))
        namespaced_kvs = iterchain(((self.pack_ns(nskey, namespace=key), nsvalue) for nskey, nsvalue in value.items()) \
                                                                                  for key, value in self.tree.items() \
                                                                                   if ismapping(value))
        if cls is None:
            cls = Flat
        return cls(dictionary=dict(chain(plain_kvs, namespaced_kvs)))
    
    def namespaces(self):
        return tuple(sorted(frozenset(key \
               for key, value in self.tree.items() \
                if ismapping(value))))
    
    def clone(self):
        return type(self)(tree=copy(self.tree))
    
    def __repr__(self):
        cnm = nameof(type(self))
        dic = repr(self.tree)
        hxa = hex(id(self))
        return f"{cnm}({dic}) @ {hxa}"

export(NAMESPACE_SEP, name='NAMESPACE_SEP')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from pprint import pprint
    
    tree = {
        'yo'        : "dogg",
        'i_heard'   : "you like",
        'nested'    : "dicts",
        'so'        : "we put dicts in your dicts",
        
        'wat'       : { 'yo'        : "dogggggg",
                        'yoyo'      : "dogggggggggg" },
        
        'nodogg'    : { 'yo'        : "dogggggg",
                        'yoyo'      : "dogggggggggg" }
    }
    
    nested = Nested(tree=tree)
    
    print("» (nested) KEYS:")
    pprint(tuple(nested.keys()))
    print()
    
    print("» (nested) VALUES:")
    pprint(tuple(nested.values()))
    print()
    
    print("» (nested) NAMESPACES:")
    pprint(tuple(nested.namespaces()))
    print()
    
    flat = nested.flatten()
    
    print("» (flat) KEYS:")
    pprint(tuple(flat.keys()))
    print()
    
    print("» (flat) VALUES:")
    pprint(tuple(flat.values()))
    print()
    
    print("» (flat) NAMESPACES:")
    pprint(tuple(flat.namespaces()))
    print()
    
    print("» (flat) dictionary:")
    pprint(flat.dictionary)
    print()
    
    print("» (flat) __repr__:")
    pprint(flat)
    print()
    
    renestified = flat.nestify()
    
    print("» (renestified) KEYS:")
    pprint(tuple(renestified.keys()))
    print()
    
    print("» (renestified) VALUES:")
    pprint(tuple(renestified.values()))
    print()
    
    print("» (renestified) NAMESPACES:")
    pprint(tuple(renestified.namespaces()))
    print()
    
    print("» (renestified) __repr__:")
    pprint(renestified)
    print()
    

if __name__ == '__main__':
    test()
