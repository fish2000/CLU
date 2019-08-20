# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from clu.constants.consts import PROJECT_NAME, NoDefault
from clu.config.base import AppName, NamespacedMutableMapping, NAMESPACE_SEP
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

PREFIX_SEP = '_'

@export
class EnvBase(NamespacedMutableMapping, AppName):
    
    @classmethod
    def prefix(cls, namespace=None):
        if not namespace:
            return cls.appname.upper() + PREFIX_SEP
        if not str(namespace).isidentifier():
            raise KeyError(f"Invalid namespace: {namespace!s}")
        return cls.appname.upper() + PREFIX_SEP + \
            str(namespace).upper() + PREFIX_SEP
    
    @classmethod
    def envkey(cls, key, namespace=None):
        return cls.prefix(namespace=namespace) + str(key).upper()
    
    @classmethod
    def deprefix(cls, key):
        string = key.lstrip(cls.appname.upper() + PREFIX_SEP)
        if PREFIX_SEP not in string:
            return string.lower()
        return NAMESPACE_SEP.join(string.lower().split(PREFIX_SEP, 1))
    
    def __init__(self, *args, **kwargs):
        self.environment = kwargs.get('environment', os.environ)
        try:
            super(EnvBase, self).__init__(*args, **kwargs)
        except TypeError:
            super(EnvBase, self).__init__()
    
    def get(self, key, namespace=None, default=NoDefault):
        if default is NoDefault:
            return self.environment[type(self).envkey(key, namespace)]
        try:
            return self.environment[type(self).envkey(key, namespace)]
        except KeyError:
            return default
    
    def set(self, key, value, namespace=None):
        if not key.isidentifier():
            raise KeyError(f"Invalid key: {key}")
        self.environment[type(self).envkey(key, namespace)] = value
    
    def delete(self, key, namespace=None):
        del self.environment[type(self).envkey(key, namespace)]
    
    def keys(self, namespace=None):
        cls = type(self)
        prefix = cls.prefix(namespace=namespace)
        return (cls.deprefix(key) for key in self.environment.keys() if key.startswith(prefix))
    
    def values(self, namespace=None):
        prefix = type(self).prefix(namespace=namespace)
        return (value for key, value in self.environment.items() if key.startswith(prefix))
    
    def namespaces(self):
        prefix = type(self).prefix(namespace=None)
        envkeys = (key.lstrip(prefix) for key in self.environment.keys() if key.startswith(prefix))
        prefixes = frozenset(key.lower().split(PREFIX_SEP, 1)[0] for key in envkeys if PREFIX_SEP in key)
        return tuple(prefixes)
    
    def clone(self):
        return type(self)(environment=self.environment)

@export
class Env(EnvBase, appname=PROJECT_NAME):
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from pprint import pprint
    env = Env()
    
    print("» KEYS:")
    pprint(tuple(env.keys()))
    print()
    
    print("» VALUES:")
    pprint(tuple(env.values()))
    print()
    
    print("» NAMESPACES:")
    pprint(tuple(env.namespaces()))
    print()

if __name__ == '__main__':
    test()
