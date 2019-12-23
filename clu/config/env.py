# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from clu.abstract import Slotted, AppName, Cloneable, ReprWrapper
from clu.constants.consts import PROJECT_NAME, NoDefault
from clu.config.abc import NAMESPACE_SEP, NamespacedMutableMapping
from clu.predicates import tuplize
from clu.typology import iterlen
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

PREFIX_SEP = '_'

@export
class EnvBase(NamespacedMutableMapping, AppName,
                                        Cloneable,
                                        ReprWrapper,
                                        metaclass=Slotted):
    
    """ The base class for “clu.config.env.Env”. Override this class in
        your own project for access to an interface to the environment
        variable table as a NamespacedMutableMapping in your Schema
        pipelines – q.v. the docstring for “clu.config.env.Env” sub.
        
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
            return cls.appname.upper() + PREFIX_SEP
        if not str(namespace).isidentifier():
            raise KeyError(f"Invalid namespace: {namespace!s}")
        return cls.appname.upper() + PREFIX_SEP + \
            str(namespace).upper() + PREFIX_SEP
    
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
        string = key.lstrip(cls.appname.upper() + PREFIX_SEP)
        if PREFIX_SEP not in string:
            return string.casefold()
        return NAMESPACE_SEP.join(string.casefold().split(PREFIX_SEP, 1))
    
    def __init__(self, *args, **kwargs):
        """ Initialize the environment-variable mapping interface.
            
            An optional “environment” keyword argument allows the
            dict-style environment access point to be specified –
            this defaults to “os.environ”.
        """
        self.environment = kwargs.get('environment', os.environ)
        try:
            super(EnvBase, self).__init__(*args, **kwargs)
        except TypeError:
            super(EnvBase, self).__init__()
    
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
        prefixes = frozenset(key.casefold().split(PREFIX_SEP, 1)[0] for key in envkeys if PREFIX_SEP in key)
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
