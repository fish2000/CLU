# -*- coding: utf-8 -*-
from __future__ import print_function
from reprlib import Repr

import clu.abstract
import collections.abc
import contextlib
import sys

from clu.constants.consts import SINGLETON_TYPES, STRINGPAIR, WHITESPACE, ENCODING, pytuple, NoDefault
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# NAMESPACES: bespoke “reprlib” recursion-friendly repr-helper:

@export
class NamespaceRepr(Repr):
    
    """ Custom Repr-izer for SimpleNamespace, Namespace and
        Typespace mappings, which can recursively self-contain.
        
        q.v. cpython docs, http://bit.ly/2r1GQ4l supra.
    """
    
    def __init__(self, *args, maxlevel=10,
                              maxstring=120,
                              maxother=120,
                            **kwargs):
        """ Initialize a NamespaceRepr, with default params
            for ‘maxlevel’, ‘maxstring’, and ‘maxother’.
        """
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()
        self.maxlevel = maxlevel
        self.maxstring = maxstring
        self.maxother = maxother
    
    def subrepr(self, thing, level):
        """ An internal “core” repr helper method. """
        if isnamespace(thing):
            return self.repr1(thing, level - 1)
        return repr(thing)
    
    def primerepr(self, thing, level):
        """ The internal method for “core” repr production
            of all BaseNamespace descendant types.
        """
        if len(thing.__dict__) == 0:
            return "{}"
        elif len(thing.__dict__) == 1:
            key = tuple(thing.__dict__.keys())[0]
            item = STRINGPAIR.format(key, self.subrepr(thing.__dict__[key], level))
            return f"{{ {item} }}"
        items = (STRINGPAIR.format(key, self.subrepr(thing.__dict__[key], level)) \
                                          for key in thing.__dict__.keys())
        ts = "    " * (int(self.maxlevel - level) + 1)
        ls = "    " * (int(self.maxlevel - level) + 0)
        total = (f",\n{ts}").join(items)
        return f"{{ \n{ts}{total}\n{ls}}}"
    
    def repr_BaseNamespace(self, thing, level):
        """ Return the “core” repr for a specific instance of
            “clu.typespace.namespace.BaseNamespace” – just the
            stringification of the key-value pairs, without
            the typename or instance-id adornment.
        """
        return self.primerepr(thing, level)
    
    def repr_SimpleNamespace(self, thing, level):
        """ Return the “core” repr for a specific instance of
            “clu.typespace.namespace.SimpleNamespace” – just
            the stringification of the key-value pairs, without
            the typename or instance-id adornment.
        """
        return self.primerepr(thing, level)
    
    def repr_Namespace(self, thing, level):
        """ Return the “core” repr for a specific instance of
            “clu.typespace.namespace.Namespace” – just the
            stringification of the key-value pairs, without
            the typename or instance-id adornment.
        """
        return self.primerepr(thing, level)
    
    def repr_Typespace(self, thing, level):
        """ Return the “core” repr for a specific instance of
            “clu.typespace.namespace.Typespace” – just the
            stringification of the key-value pairs, without
            the typename or instance-id adornment.
        """
        return self.primerepr(thing, level)
    
    def shortrepr(self, thing):
        """ Return the “short” repr of a namespace instance –
            all whitespace will be condensed to single spaces
            without newlines.
        """
        return WHITESPACE.sub(' ', self.repr(thing))
    
    def fullrepr(self, thing, short=False):
        """ Return the “full” repr of a namespace instance. """
        from clu.repr import fullrepr as fullstringrepr
        if short:
            return fullstringrepr(thing, self.shortrepr(thing))
        return fullstringrepr(thing, self.repr(thing))

reprizer = NamespaceRepr()
nsrepr = reprizer.repr
nsshortrepr = reprizer.shortrepr

# NAMESPACES: SimpleNamespace and Namespace

@export
class BaseNamespace(collections.abc.Set,
                    collections.abc.Mapping,
                    clu.abstract.Cloneable,
                    metaclass=clu.abstract.Slotted):
    
    """ The abstract base for SimpleNamespace, Namespace and Typespace. """
    
    __slots__ = pytuple('dict', 'weakref')
    
    def __init__(self, *args, **kwargs):
        """ Initialize a new namespace instance.
            
            One may optionally pass in any number of instances
            of mapping-ish types, to be merged with the namespace.
            
            Any loose keyword arguments will also be merged in.
        
            The BaseNamespace class also furnishes a `__missing__(…)`
            method, which can be overridden by subclasses to provide
            “collections.defaultdict”–like behaviors.
        """
        for mapping in (dict(arg) for arg in args):
            for key, value in mapping.items():
                self.__dict__[key] = value
        for key, value in kwargs.items():
            self.__dict__[key] = value
    
    def __len__(self):
        return len(self.__dict__)
    
    def __iter__(self):
        yield from self.__dict__
    
    def __contains__(self, key):
        return key in self.__dict__
    
    def __getitem__(self, key):
        try:
            return self.__dict__.__getitem__(key)
        except KeyError:
            return self.__missing__(key)
    
    def __missing__(self, key):
        raise KeyError(key)
    
    def __eq__(self, other):
        if type(other) in SINGLETON_TYPES:
            return False
        from clu.dicts import asdict
        return self.__dict__ == asdict(other)
    
    def __ne__(self, other):
        if type(other) in SINGLETON_TYPES:
            return True
        from clu.dicts import asdict
        return self.__dict__ != asdict(other)
    
    def __dir__(self):
        """ Get a list with all the stringified keys in the namespace. """
        return [str(key) for key in self if key not in ('get', 'pop', 'update')]
    
    def __repr__(self):
        return reprizer.fullrepr(self)
    
    def __str__(self):
        return reprizer.fullrepr(self, short=True)
    
    def __bytes__(self):
        return bytes(str(self), encoding=ENCODING)
    
    def __bool__(self):
        return bool(self.__dict__)
    
    def clone(self, deep=False, memo=None):
        # Only shallow clone for the moment:
        return type(self)(self.__dict__.copy())

@export
class SimpleNamespace(BaseNamespace,
                      collections.abc.Hashable):
    
    """ Implementation courtesy this SO answer:
        • https://stackoverflow.com/a/37161391/298171
        
        Additionally, SimpleNamespace furnishes an `__hash__(…)` method.
    """
    
    def __hash__(self):
        return hash(tuple(self.__dict__.keys()) +
                    tuple(self.__dict__.values()))

@export
class Namespace(BaseNamespace,
                collections.abc.MutableMapping,
                contextlib.AbstractContextManager):
    
    """ Namespace adds the `get(…)`, `__len__()`, `__contains__(…)`, `__getitem__(…)`,
        `__setitem__(…)`, and `__add__(…)` methods to its ancestor class
        implementation BaseNamespace.
        
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
    
    def popitem(self):
        """ Remove and return a single key-value pair from the namespace,
            raising a KeyError if the namespace is empty.
        """
        return self.__dict__.popitem()
    
    def update(self, dictish=None, **updates):
        """ Update the namespace with key/value pairs and/or an iterator;
            q.v. `dict.update(…)` docstring supra.
        """
        self.__dict__.update(dictish, **updates)
    
    def __getattr__(self, key):
        # Called when “key” is missing from ‘self.__dict__’ –
        # provided “key” isn’t dunderized!…
        from clu.predicates import ispyname
        if not ispyname(key):
            # subnamespace = type(self)()
            subnamespace = Namespace()
            self.__dict__[key] = subnamespace
            return subnamespace
        raise AttributeError(key)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        return exc_type is None
    
    def __setitem__(self, key, value):
        self.__dict__.__setitem__(key, value)
    
    def __delitem__(self, key):
        self.__dict__.__delitem__(key)
    
    def __add__(self, operand):
        # On add, old values are not overwritten
        from clu.predicates import ismergeable
        from clu.dicts import merge_fast_two
        if not ismergeable(operand):
            return NotImplemented
        return type(self)(merge_fast_two(self, operand))
    
    def __radd__(self, operand):
        # On reverse-add, old values are overwritten
        from clu.predicates import ismergeable
        from clu.dicts import merge_fast_two
        if not ismergeable(operand):
            return NotImplemented
        return type(self)(merge_fast_two(operand, self))
    
    def __iadd__(self, operand):
        # On in-place add, old values are updated and replaced
        from clu.predicates import ismergeable
        from clu.dicts import asdict
        if not ismergeable(operand):
            return NotImplemented
        self.__dict__.update(asdict(operand))
        return self

@export
class Typespace(Namespace):
    
    """ The Typespace class is instantiated to form the `clu.typespace.types` instance. """
    
    def __missing__(self, key):
        """ Ensure compatibility with Python’s `types` module. """
        if not key.endswith('Type'):
            return super().__missing__(key)
        return self[key.removesuffix('Type')]
    
    def __getattr__(self, key):
        """ Ensure compatibility with Python’s `types` module. """
        if not key.endswith('Type'):
            return super().__getattr__(key)
        return getattr(self, key.removesuffix('Type'))

@export
def isnamespace(thing):
    """ isnamespace(thing) → boolean predicate,
        True if the name of the type of “thing”
        is amongst those of the quote-unquote
        “Namespace tower”, as defined in the
        module “clu.typespace.namespace”
    """
    from clu.typology import subclasscheck
    return subclasscheck(thing, (BaseNamespace,
                               SimpleNamespace,
                                     Namespace,
                                     Typespace))

with exporter as export:
    
    export(reprizer,    name='reprizer')
    export(nsshortrepr, name='nsshortrepr')
    export(nsrepr,      name='nsrepr',          doc="Return the “core” repr for any descendant namespace type.")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline.fixture
    def flat_dict():
        return {
            'yo'        : "dogg",
            'i_heard'   : "you like",
            'nested'    : "dicts",
            'so'        : "we put dicts in your dicts"
        }
    
    @inline.fixture
    def shorty_repr():
        return "SimpleNamespace({ yo : 'dogg', i_heard : 'you like', " \
               "nested : 'dicts', so : 'we put dicts in your dicts' })"
    
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
        
        assert ROOT.other.additional        == "«additional»"
        assert ROOT.other.considerations    == "…"
        assert ROOT.yo.dogg                 == "yo dogg"
        assert ROOT.yo.wat                  == "¡WAT!"
        
        with ROOT.other as ns:
            assert ns.additional            == "«additional»"
            assert ns.considerations        == "…"
        
        return ROOT
    
    @inline
    def test_two():
        """ SimpleNamespace sanity checks """
        from clu.repr import chop_instance_repr
        
        sn = SimpleNamespace(flat_dict())
        assert dir(sn) == ['i_heard', 'nested', 'so', 'yo']
        assert chop_instance_repr(reprizer.fullrepr(sn, short=True)) == shorty_repr()
    
    class NamespaceKeyError(KeyError):
        pass
    
    @inline
    def test_three():
        """ Namespace subclass “__missing__(…)” check """
        
        class MissingNamespace(Namespace):
            
            def __missing__(self, key):
                """ Raise a bespoke exception on missing key access """
                raise NamespaceKeyError(key)
        
        try:
            MissingNamespace()['wat']
        except NamespaceKeyError as exc:
            assert bool(exc)
    
    @inline
    def test_four():
        """ Compatibility with standard-library “types.SimpleNamespace” """
        import types
        
        stdn = types.SimpleNamespace(**flat_dict())
        sn = SimpleNamespace(flat_dict())
        
        assert stdn.__dict__ == sn.__dict__
        assert nsrepr(stdn) == nsrepr(sn)
        assert nsshortrepr(stdn) == nsshortrepr(sn)
        
        print(repr(stdn))
        print()
        print(repr(sn))
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
