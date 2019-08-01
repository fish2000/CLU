# -*- coding: utf-8 -*-
from __future__ import print_function

import re

from clu.constants.consts import SEPARATOR_WIDTH, pytuple, NoDefault
from clu.constants.polyfills import MutableMapping, HashableABC
from clu.dicts import merge_two, asdict
from clu.naming import nameof
from clu.predicates import ismergeable
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# NAMESPACES: SimpleNamespace and Namespace

@export
class SimpleNamespace(HashableABC):
    
    """ Implementation courtesy this SO answer:
        • https://stackoverflow.com/a/37161391/298171
    """
    __slots__ = pytuple('dict', 'weakref')
    
    def __init__(self, *args, **kwargs):
        for arg in args:
            self.__dict__.update(asdict(arg))
        self.__dict__.update(kwargs)
    
    def __iter__(self):
        return iter(self.__dict__.keys())
    
    def __repr__(self):
        items = ("{}={!r}".format(key, self.__dict__[key]) for key in sorted(self))
        return "{}({}) @ {}".format(nameof(type(self)),
                         ",\n".join(items),  id(self))
    
    def __eq__(self, other):
        return self.__dict__ == asdict(other)
    
    def __ne__(self, other):
        return self.__dict__ != asdict(other)
    
    def __hash__(self):
        return hash(tuple(self.__dict__.keys()) +
                    tuple(self.__dict__.values()))

@export
class Namespace(SimpleNamespace, MutableMapping):
    
    """ Namespace adds the `get(…)`, `__len__()`, `__contains__(…)`, `__getitem__(…)`,
        `__setitem__(…)`, `__add__(…)`, and `__bool__()` methods to its ancestor class
        implementation SimpleNamespace.
        
        Since it implements a `get(…)` method, Namespace instances can be passed
        to `merge(…)` – q.v. `merge(…)` function definition supra.
        
        Additionally, Namespace furnishes an `__all__` property implementation.
    """
    __slots__ = tuple()
    
    winnower = re.compile(r"\{(?:\s+)(?P<stuff>.+)")
    
    def get(self, key, default=NoDefault):
        """ Return the value for key if key is in the namespace, else default. """
        if default is NoDefault:
            return self.__dict__.get(key)
        return self.__dict__.get(key, default)
    
    def pop(self, key, default=NoDefault):
        """ Return the value for key if key is in the namespace, else default,
            removing the key/value pairing if the key was found.
        """
        if default is NoDefault:
            return self.__dict__.pop(key)
        return self.__dict__.pop(key, default)
    
    def update(self, dictish=None, **updates):
        """ Update the namespace with key/value pairs and/or an iterator;
            q.v. `dict.update(…)` docstring supra.
        """
        self.__dict__.update(dictish, **updates)
    
    @property
    def __all__(self):
        """ Get a tuple with all the stringified keys in the namespace. """
        return tuple(str(key) for key in sorted(self))
    
    def __repr__(self):
        from pprint import pformat
        return "{}({}) @ {}".format(nameof(type(self)),
                                    self.winnower.sub(r'{\g<stuff>',
                                              pformat(self.__dict__,
                                                      width=SEPARATOR_WIDTH)),
                                                      id(self))
    
    def __len__(self):
        return len(self.__dict__)
    
    def __contains__(self, key):
        return key in self.__dict__
    
    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)
    
    def __setitem__(self, key, value):
        self.__dict__.__setitem__(key, value)
    
    def __delitem__(self, key):
        self.__dict__.__delitem__(key)
    
    def __add__(self, operand):
        # On add, old values are not overwritten
        if not ismergeable(operand):
            return NotImplemented
        return merge_two(self, operand, cls=type(self))
    
    def __radd__(self, operand):
        # On reverse-add, old values are overwritten
        if not ismergeable(operand):
            return NotImplemented
        return merge_two(operand, self, cls=type(self))
    
    def __iadd__(self, operand):
        # On in-place add, old values are updated and replaced
        if not ismergeable(operand):
            return NotImplemented
        self.__dict__.update(asdict(operand))
        return self
    
    def __or__(self, operand):
        return self.__add__(operand)
    
    def __ror__(self, operand):
        return self.__radd__(operand)
    
    def __ior__(self, operand):
        return self.__iadd__(operand)
    
    def __bool__(self):
        return bool(self.__dict__)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
