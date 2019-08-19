# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain

iterchain = chain.from_iterable

import abc

abstract = abc.abstractmethod

from clu.constants.consts import PROJECT_NAME, NoDefault
from clu.typology import ismapping
from clu.exporting import ValueDescriptor, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

NAMESPACE_SEP = ':'

@export
class Base(abc.ABC):
    
    @classmethod
    def __init_subclass__(cls, appname=None, **kwargs):
        super(Base, cls).__init_subclass__(**kwargs)
        cls.appname = ValueDescriptor(appname)
    
    @staticmethod
    def unpack_ns(string):
        if NAMESPACE_SEP not in string:
            return None, string
        return string.split(NAMESPACE_SEP, 1)
    
    @staticmethod
    def pack_ns(string, namespace=None):
        if namespace is None:
            return string
        return NAMESPACE_SEP.join((namespace, string))
    
    def __init__(self, *args, **kwargs):
        if type(self).appname is None:
            raise LookupError("Cannot instantiate a base config class")
    
    @abstract
    def get(self, key, namespace=None, default=NoDefault):
        ...
    
    @abstract
    def set(self, key, value, namespace=None):
        ...
    
    def delete(self, key, namespace=None):
        pass
    
    @abstract
    def keys(self, namespace=None):
        ...
    
    @abstract
    def values(self, namespace=None):
        ...
    
    def items(self, namespace=None):
        return zip(self.keys(namespace),
                   self.values(namespace))
    
    @abstract
    def namespaces(self):
        ...
    
    def update(self, dictish=NoDefault, **updates):
        if dictish is not NoDefault:
            for key, value in dictish.items():
                self[key] = value
        for key, value in updates.items():
            self[key] = value
    
    def __len__(self):
        return len(self.keys())
    
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
class NestedBase(Base):
    
    def __init__(self, tree=None, *args, **kwargs):
        try:
            super(NestedBase, self).__init__(*args, **kwargs)
        except TypeError:
            super(NestedBase, self).__init__()
        self.tree = tree or {}
    
    def get(self, key, namespace=None, default=NoDefault):
        if namespace is None:
            if default is NoDefault:
                return self.tree.get(key)
            return self.tree.get(key, default)
        if namespace in self.namespaces():
            if default is NoDefault:
                return self.tree[namespace].get(key)
            return self.tree[namespace].get(key, default)
        raise KeyError(f"Unknown namespace: {namespace}")
    
    def set(self, key, value, namespace=None):
        if namespace is None:
            self.tree[key] = value
        if namespace not in self.namespaces():
            self.tree[namespace] = {}
        self.tree[namespace][key] = value
    
    def delete(self, key, namespace=None):
        if namespace is None:
            del self.tree[key]
        if namespace in self.namespaces():
            del self.tree[namespace][key]
        raise KeyError(f"Unknown namespace: {namespace}")
    
    def keys(self, namespace=None):
        if namespace is None:
            keys = (key for key, value in self.tree.items() if not ismapping(value))
            nskeys = iterchain((self.pack_ns(nskey, namespace=key) for nskey in value.keys()) \
                                                                   for key, value in self.tree.items() \
                                                                    if ismapping(value))
            return chain(keys, nskeys)
        if namespace in self.namespaces():
            return self.tree[namespace].keys()
        raise KeyError(f"Unknown namespace: {namespace}")
    
    def values(self, namespace=None):
        if namespace is None:
            values = (value for value in self.tree.values() if not ismapping(value))
            nsvalues = iterchain(value.values() for value in self.tree.values() if ismapping(value))
            return chain(values, nsvalues)
        if namespace in self.namespaces():
            return self.tree[namespace].values()
        raise KeyError(f"Unknown namespace: {namespace}")
    
    def namespaces(self):
        return tuple(frozenset(key for key, value in self.tree.items() if ismapping(value)))

@export
class Nested(NestedBase, appname=PROJECT_NAME):
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from pprint import pprint
    
    tree = {
        'yo'        : "dogg",
        'i_heard'   : "you like",
        'nested'    : "dicts",
        
        'wat'       : { 'yo'        : "dogggggg",
                        'yoyo'      : "dogggggggggg" },
        
        'nodogg'    : { 'yo'        : "dogggggg",
                        'yoyo'      : "dogggggggggg" }
    }
    
    nested = Nested(tree=tree)
    
    print("» KEYS:")
    pprint(tuple(nested.keys()))
    print()
    
    print("» VALUES:")
    pprint(tuple(nested.values()))
    print()
    
    print("» NAMESPACES:")
    pprint(tuple(nested.namespaces()))
    print()
    

if __name__ == '__main__':
    test()
