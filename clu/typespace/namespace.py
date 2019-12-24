# -*- coding: utf-8 -*-
from __future__ import print_function
from reprlib import Repr

import clu.abstract
import collections.abc
import contextlib
import re

from clu.constants.consts import pytuple, NoDefault
from clu.constants.polyfills import ispyname
from clu.dicts import merge_two, asdict
from clu.predicates import ismergeable
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# NAMESPACES: bespoke “reprlib” recursion-friendly repr-helper:

WHITESPACE = re.compile(r'\s+')
STRINGPAIR = "{!s} : {!s}"

@export
class NamespaceRepr(Repr):
    
    """ Custom Repr-izer for SimpleNamespace and Namespace mappings,
        which can recursively self-contain.
        
        q.v. cpython docs, http://bit.ly/2r1GQ4l supra.
    """
    
    def __init__(self, *args, maxlevel=10,
                              maxstring=120,
                              maxother=120,
                            **kwargs):
        """ Initialize a NamespaceRepr, with default params for ‘maxlevel’,
            ‘maxstring’, and ‘maxother’.
        """
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()
        self.maxlevel = maxlevel
        self.maxstring = maxstring
        self.maxother = maxother
    
    def subrepr(self, thing, level):
        if isnamespace(thing):
            return self.repr1(thing, level - 1)
        return repr(thing)
    
    def primerepr(self, thing, level):
        if len(thing) == 0:
            return "{}"
        elif len(thing) == 1:
            key = tuple(thing.keys())[0]
            item = STRINGPAIR.format(key, self.subrepr(thing.__dict__[key], level))
            return f"{{ {item} }}"
        items = (STRINGPAIR.format(key, self.subrepr(thing.__dict__[key], level)) for key in sorted(thing))
        ts = "    " * (int(self.maxlevel - level) + 1)
        ls = "    " * (int(self.maxlevel - level) + 0)
        total = (f",\n{ts}").join(items)
        return f"{{ \n{ts}{total}\n{ls}}}"
    
    def repr_SimpleNamespace(self, thing, level):
        return self.primerepr(thing, level)
    
    def repr_Namespace(self, thing, level):
        return self.primerepr(thing, level)
    
    def shortrepr(self, thing):
        return WHITESPACE.sub(' ', self.repr(thing))
    
    def fullrepr(self, thing, short=False):
        from clu.repr import fullrepr as fullstringrepr
        if short:
            return fullstringrepr(thing, self.shortrepr(thing))
        return fullstringrepr(thing, self.repr(thing))

reprizer = NamespaceRepr()
nsrepr = reprizer.repr
nsshortrepr = reprizer.shortrepr

# NAMESPACES: SimpleNamespace and Namespace

@export
class SimpleNamespace(collections.abc.Hashable,
                      collections.abc.Iterable,
                      clu.abstract.ReprWrapper,
                      metaclass=clu.abstract.Slotted):
    
    """ Implementation courtesy this SO answer:
        • https://stackoverflow.com/a/37161391/298171
        
        Additionally, SimpleNamespace furnishes an `__dir__(…)` method.
    """
    
    __slots__ = pytuple('dict', 'weakref')
    
    def __init__(self, *args, **kwargs):
        for arg in args:
            self.__dict__.update(asdict(arg))
        self.__dict__.update(kwargs)
    
    def __iter__(self):
        yield from self.__dict__
    
    def inner_repr(self):
        return nsrepr(self)
    
    def __eq__(self, other):
        return self.__dict__ == asdict(other)
    
    def __ne__(self, other):
        return self.__dict__ != asdict(other)
    
    def __hash__(self):
        return hash(tuple(self.__dict__.keys()) +
                    tuple(self.__dict__.values()))
    
    def __dir__(self):
        """ Get a list with all the stringified keys in the namespace. """
        return [str(key) for key in sorted(self) if key not in ('inner_repr', 'get', 'pop', 'update')]

@export
class Namespace(SimpleNamespace,
                collections.abc.MutableMapping,
                contextlib.AbstractContextManager):
    
    """ Namespace adds the `get(…)`, `__len__()`, `__contains__(…)`, `__getitem__(…)`,
        `__setitem__(…)`, `__add__(…)`, and `__bool__()` methods to its ancestor class
        implementation SimpleNamespace.
        
        Since it implements a `get(…)` method, Namespace instances can be passed
        to `merge(…)` – q.v. `merge(…)` function definition supra.
    """
    
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
    
    def __getattr__(self, key):
        # Called when “key” is missing from ‘self.__dict__’ –
        # provided “key” isn’t dunderized!…
        if not ispyname(key):
            subnamespace = type(self)()
            self.__dict__[key] = subnamespace
            return subnamespace
        raise AttributeError(key)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        return exc_type is None
    
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

@export
def isnamespace(thing):
    from clu.typology import subclasscheck
    return subclasscheck(thing, (SimpleNamespace, Namespace))

with exporter as export:
    
    export(reprizer,    name='reprizer')
    export(nsrepr,      name='nsrepr')
    export(nsshortrepr, name='nsshortrepr')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_one():
        """ Implicit recursive namespaces """
        ROOT = Namespace()
        
        ROOT.title = "«title»"
        ROOT.count = 666
        ROOT.idx = 0
        
        with ROOT.other as ns:
            ns.additional = "«additional»"
            ns.considerations = "…"
        
        ROOT.yo.dogg = "yo dogg"
        ROOT.yo.wat = "¡WAT!"
        
        # print("ROOT NAMESPACE:")
        # print(ROOT)
        
        assert ROOT.other.additional        == "«additional»"
        assert ROOT.other.considerations    == "…"
        assert ROOT.yo.dogg                 == "yo dogg"
        assert ROOT.yo.wat                  == "¡WAT!"
        
        with ROOT.other as ns:
            assert ns.additional            == "«additional»"
            assert ns.considerations        == "…"
        
        return ROOT
    
    inline.test(100)

if __name__ == '__main__':
    test()
