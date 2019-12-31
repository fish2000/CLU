# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain

iterchain = chain.from_iterable

import abc
import clu.abstract
import collections
import collections.abc
import copy
import os

abstract = abc.abstractmethod

from clu.constants.consts import DEBUG, PROJECT_NAME, NoDefault
from clu.constants.consts import ENVIRONS_SEP, NAMESPACE_SEP
from clu.predicates import isiterable, tuplize
from clu.typology import iterlen, ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class NamespacedMutableMapping(collections.abc.MutableMapping,
                               collections.abc.Reversible):
    
    __slots__ = tuple()
    
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
        yield from self.keys()
    
    def __reversed__(self):
        yield from reversed(self.keys())
    
    def __len__(self):
        return iterlen(self.keys())
    
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
    
    def __missing__(self, key):
        if DEBUG:
            print(f"__missing__(…): {key}")
        raise KeyError(key)
    
    def __bool__(self):
        return len(self.keys()) > 0

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
class Nested(NamespacedMutableMapping,
             clu.abstract.ReprWrapper,
             clu.abstract.Cloneable):
    
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

@export
class EnvBase(NamespacedMutableMapping,
              clu.abstract.AppName,
              clu.abstract.Cloneable,
              clu.abstract.ReprWrapper,
              metaclass=clu.abstract.Slotted):
    
    """ The base class for “clu.config.base.Env”. Override this class in
        your own project for access to an interface to the environment
        variable table as a NamespacedMutableMapping in your Schema
        pipelines – q.v. the docstring for “clu.config.base.Env” sub.
        
        This class uses the “clu.config.base.AppName” mixin as part of
        its inheritance chain. The “AppName” mixin acts on the “appname”
        class keyword and furnishes a read-only descriptor based on that
        keywords’ value.
    """
    __slots__ = tuplize('environment')
    
    @classmethod
    def prefix(cls, namespace=None):
        """ Determine the environment-variable prefix based on a given
            namespace string and the classes’ “appname” value. Like e.g.,
            for an appname of “YoDogg” and a namespace value of “iheard”,
            the environment variable prefix would work out such that
            a variable with a key value of “youlike” would look like this:
                
                YODOGG_IHEARD_YOULIKE
                                     
                ^^^^^^ ^^^^^^ ^^^^^^^
                   |      |      |
                   |      |      +––––– mapping key (uppercased)
                   |      +–––––––––––– namespace value (uppercased)
                   +––––––––––––––––––– app name (uppercased)
        """
        if not namespace:
            return cls.appname.upper() + ENVIRONS_SEP
        if not str(namespace).isidentifier():
            raise KeyError(f"Invalid namespace: {namespace!s}")
        return cls.appname.upper() + ENVIRONS_SEP + \
            str(namespace).upper() + ENVIRONS_SEP
    
    @classmethod
    def envkey(cls, key, namespace=None):
        """ Transform a mapping key, along with an optional namespace
            value and the classes’ “appname” value, into an environment-
            variable name. Like e.g., for an appname of “YoDogg” and
            a namespace value of “iheard”, the environment variable
            prefix would work out such that a variable with a key value
            of “youlike” would look like this:
                
                YODOGG_IHEARD_YOULIKE
                                     
                ^^^^^^ ^^^^^^ ^^^^^^^
                   |      |      |
                   |      |      +––––– mapping key (uppercased)
                   |      +–––––––––––– namespace value (uppercased)
                   +––––––––––––––––––– app name (uppercased)
        """
        return cls.prefix(namespace=namespace) + str(key).upper()
    
    @classmethod
    def deprefix(cls, key):
        """ Transform an environment-variable name into a (possibly
            namespaced) NamespacedMutableMapping key.
        """
        string = key.lstrip(cls.appname.upper() + ENVIRONS_SEP)
        if ENVIRONS_SEP not in string:
            return string.casefold()
        return NAMESPACE_SEP.join(string.casefold().split(ENVIRONS_SEP, 1))
    
    def __init__(self, *args, **kwargs):
        """ Initialize the environment-variable mapping interface.
            
            An optional “environment” keyword argument allows the
            dict-style environment access point to be specified –
            this defaults to “os.environ”.
        """
        self.environment = kwargs.get('environment', os.environ)
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()
    
    def get(self, key, namespace=None, default=NoDefault):
        """ Retrieve a (possibly namespaced) environment variable for
            a key.
            
            An optional default value may be specified, to be returned
            if the key in question is not found in the environment.
        """
        if default is NoDefault:
            return self.environment[type(self).envkey(key, namespace)]
        try:
            return self.environment[type(self).envkey(key, namespace)]
        except KeyError:
            return default
    
    def set(self, key, value, namespace=None):
        """ Set a (possibly namespaced) environment variable for
            a key.
        """
        if not key.isidentifier():
            raise KeyError(f"Invalid key: {key}")
        if value is None:
            if type(self).envkey(key, namespace) in self.environment:
                self.delete(key, namespace=namespace)
        else:
            self.environment[type(self).envkey(key, namespace)] = str(value)
    
    def delete(self, key, namespace=None):
        """ Delete a (possibly namespaced) variable from the environment. """
        del self.environment[type(self).envkey(key, namespace)]
    
    def keys(self, namespace=None):
        """ Return an iterable generator over all keys matching either the
            classes’ appname, or the classes’ appname and a specified
            namespace value.
        """
        cls = type(self)
        prefix = cls.prefix(namespace=namespace)
        return (cls.deprefix(key) for key in self.environment.keys() if key.startswith(prefix))
    
    def values(self, namespace=None):
        """ Return an iterable generator over all values matching either the
            classes’ appname, or the classes’ appname and a specified
            namespace value.
        """
        prefix = type(self).prefix(namespace=namespace)
        return (value for key, value in self.environment.items() if key.startswith(prefix))
    
    def namespaces(self):
        """ Return a sorted tuple listing all of the namespaces defined in
            the current environment.
        """
        prefix = type(self).prefix(namespace=None)
        envkeys = (key.lstrip(prefix) for key in self.environment.keys() if key.startswith(prefix))
        prefixes = frozenset(key.casefold().split(ENVIRONS_SEP, 1)[0] for key in envkeys if ENVIRONS_SEP in key)
        return tuple(sorted(prefixes))
    
    def inner_repr(self):
        """ Return some readable meta-information about this instance """
        prefix = type(self).prefix(namespace=None)
        namespaces = len(self.namespaces())
        keys = iterlen(self.keys())
        return f"[prefix=“{prefix}*”, namespaces={namespaces}, keys={keys}]"
    
    def clone(self, *args, **kwargs):
        """ Return a cloned copy of this NamespacedMutableMapping environment
            interface.
        """
        return type(self)(environment=self.environment)

@export
class Env(EnvBase, appname=PROJECT_NAME):
    """ An interface to the environment variable table of the running
        process as a NamespacedMutableMapping.
        
        This class is specifically germane to the CLU project – note
        that the “appname” class keyword is used to assign a CLU-specific
        constant value.
        
        CLU users who want access to the environment variable table of
        their running processes as a NamespacedMutableMapping in their
        own projects should create a subclass of EnvBase of their own.
        Like this one, it needs to assign the “appname” class keyword;
        it is unnecessary (but OK!) for you to define further methods,
        properties, class constants, and whatnot.
    """
    pass

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
    
    def test_env():
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
    
    test_env()

if __name__ == '__main__':
    test()
