# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import collections
import collections.abc
import copy

abstract = abc.abstractmethod

from clu.constants.consts import DEBUG, NoDefault
from clu.fs.misc import typename_hexid
from clu.predicates import (isiterable, always, uncallable,
                            isexpandable, iscontainer,
                            tuplize)
from clu.exporting import Slotted, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

NAMESPACE_SEP = ':'

@export
class ReprWrapper(abc.ABC):
    
    """ ReprWrapper fills in a default template for __repr__ results,
        based on a standard display including the type name and the
        hex ID of the instance:
        
            TypeName( ••• ) @ 0xDEADBEEF
        
        … The “ ••• ” string gets filled in by a new abstract method,
        “inner_repr()”, which subclasses must provide. This new method
        takes no arguments and should return a string.
        
        Example 1: Return the repr of a relevant sub-instance value:
        
            FlatOrderedSet(('a', 'b', 'c', 'd')) @ 0x115299650
        
        … Note that the parenthesized value is the repr of an internal
        tuple value. The “inner_repr()” method returns something like
        “repr(self.internal_tuple)”.
        
        Example 2: Return some interesting meta-information:
        
            Env([prefix=“CLU_*”, namespaces=4, keys=13]) @ 0x115373690
        
        … Here the return value of “inner_repr()” is composed freely,
        like any other repr-string, instead of delegated wholesale to
        another objects repr value. 
    """
    __slots__ = tuple()
    
    @abstract
    def inner_repr(self):
        """ Return a repr string for instances of this class """
        ...
    
    def __repr__(self):
        """ This classes’ object instances’ unique string representation """
        cnm, hxa = typename_hexid(self)
        rpr = self.inner_repr()
        return f"{cnm}({rpr}) @ {hxa}"

@export
class Cloneable(abc.ABC):
    
    """ An abstract class representing something “clonable.” A cloneable
        subclass need only implement the one method, “clone()” – taking no
        arguments and returning a new instance of said class, populated
        as a cloned copy of the instance upon which the “clone()” method
        was called.
        
        Implementors are at liberty to use shallow- or deep-copy methods,
        or a mixture of the two, in creating these cloned instances.
    """
    __slots__ = tuple()
    
    @abstract
    def clone(self, deep=False, memo=None):
        """ Return a cloned copy of this instance """
        ...
    
    def __copy__(self):
        """ Return a shallow copy of this instance """
        return self.clone()
    
    def __deepcopy__(self, memo):
        """ Return a deep copy of this instance """
        return self.clone(deep=True, memo=memo)

@export
class FlatOrderedSet(collections.abc.Set,
                     collections.abc.Sequence,
                     collections.abc.Reversible,
                     collections.abc.Hashable,
                     Cloneable, ReprWrapper,
                     metaclass=Slotted):
    
    """ FlatOrderedSet is a structure designed to coalesce any nested
        elements with which it is initialized into a flat, ordered sequence
        devoid of None-values. It has both set and sequence properties –
        membership can be tested as with a set; comparisons can be made with
        less-than and greater-than operators, as with a set; recombinant 
        operations are performed with binary-and and binary-or operators, as
        with a set – but like a sequence, iterating a FlatOrderedSet has a
        stable and deterministic order and items may be retrieved from an
        instance using subscript indexes (e.g. flat_ordered_set[3]). 
        
        Here’s an example of the coalescing behavior:
        
            stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
            summary = FlatOrderedSet("a", "b", "c", "d")
            
            assert stuff == summary
        
        One can optionally specify, as a keyword-only argument, a unary boolean
        function “predicate” that will be used to filter out any of the items
        used to initialize the FlatOrderedSet for which the predicate returns
        a Falsey value. 
    """
    
    __slots__ = tuplize('things')
    
    def __init__(self, *things, predicate=always):
        """ Initialize a new FlatOrderedSet instance with zero or more things.
            
            Optionally, a unary boolean function “predicate” may be specified
            to filter the list of things.
        """
        if uncallable(predicate):
            raise ValueError("FlatOrderedSet requires a callable predicate")
        thinglist = []
        if len(things) == 1:
            if isexpandable(things[0]):
                things = things[0]
            elif iscontainer(things[0]):
                things = tuple(things[0])
        for thing in things:
            if thing is not None:
                if isinstance(thing, type(self)):
                    for other in thing.things:
                        if predicate(other):
                            if other not in thinglist:
                                thinglist.append(other)
                elif predicate(thing):
                    if thing not in thinglist:
                        thinglist.append(thing)
        self.things = tuple(thinglist)
    
    def __iter__(self):
        yield from iter(self.things)
    
    def __reversed__(self):
        yield from reversed(self.things)
    
    def __len__(self):
        return len(self.things)
    
    def __contains__(self, thing):
        return thing in self.things
    
    def __getitem__(self, idx):
        return self.things[idx]
    
    def __bool__(self):
        return len(self.things) > 0
    
    def __hash__(self):
        return hash(self.things) & hash(id(self.things))
    
    def clone(self, deep=False, memo=None):
        # Q.v. https://stackoverflow.com/a/48550898/298171
        cls = type(self)
        out = cls.__new__(cls)
        things = list()
        for thing in self.things:
            things.append(copy.copy(thing))
        super(cls, out).__init__(*things)
        return out
    
    def inner_repr(self):
        return repr(self.things)

@export
class NamespacedMutableMapping(collections.abc.MutableMapping,
                               collections.abc.Reversible,
                               ReprWrapper):
    
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
        yield from iter(self.keys())
    
    def __reversed__(self):
        yield from reversed(self.keys())
    
    def __len__(self):
        return len(list(self.keys()))
    
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

export(NAMESPACE_SEP, name='NAMESPACE_SEP')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
