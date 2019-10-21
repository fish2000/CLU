# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain
import copy

iterchain = chain.from_iterable

from clu.abstract import Cloneable, ReprWrapper
from clu.constants.consts import NoDefault
from clu.config.abc import (NAMESPACE_SEP, NamespacedMutableMapping)
from clu.typology import ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class Flat(NamespacedMutableMapping, ReprWrapper, Cloneable):
    
    def __init__(self, dictionary=None, *args, **kwargs):
        try:
            super(Flat, self).__init__(*args, **kwargs)
        except TypeError:
            super(Flat, self).__init__()
        self.dictionary = dict(dictionary or {})
    
    def get(self, key, namespace=None, default=NoDefault):
        nskey = self.pack_ns(key, namespace=namespace)
        if default is NoDefault:
            return self.dictionary[nskey]
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
    
    def __getstate__(self):
        return self.dictionary
    
    def __setstate__(self, state):
        self.dictionary = state
    
    def inner_repr(self):
        return repr(self.dictionary)
    
    def clone(self, deep=False, memo=None):
        return type(self)(dictionary=copy.copy(self.dictionary))

@export
class Nested(NamespacedMutableMapping, ReprWrapper, Cloneable):
    
    def __init__(self, tree=None, *args, **kwargs):
        try:
            super(Nested, self).__init__(*args, **kwargs)
        except TypeError:
            super(Nested, self).__init__()
        self.tree = dict(tree or {})
    
    def get(self, key, namespace=None, default=NoDefault):
        if namespace is None:
            if default is NoDefault:
                return self.tree[key]
            return self.tree.get(key, default)
        elif namespace in self.namespaces():
            if default is NoDefault:
                return self.tree[namespace][key]
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
    
    def __getstate__(self):
        return self.tree
    
    def __setstate__(self, state):
        self.tree = state
    
    def inner_repr(self):
        return repr(self.tree)
    
    def clone(self, deep=False, memo=None):
        return type(self)(tree=copy.copy(self.tree))

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
