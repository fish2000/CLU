# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import copy
import clu.abstract
import collections
import collections.abc

abstract = abc.abstractmethod

from clu.constants.consts import NAMESPACE_SEP, pytuple
from clu.config.ns import (concatenate_ns, pack_ns)

from clu.predicates import isnormative, tuplize
from clu.typology import isnumber, iterlen
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

typename = lambda thing: type(thing).__name__
set_returner = lambda self, iterable: set(iterable)

@export
class KeyMapViewBase(collections.abc.Sequence,
                     collections.abc.Sized,
                     metaclass=clu.abstract.Slotted):
    
    """ The base class for KeyMap view classes.
        
        These view classes correspond to, but do not inherit directly from,
        the descendants of “collections.abc.MappingView”. They have been
        specially kitted out to deal with KeyMap namespaces: each instance
        has a ‘mapping’ attribute referring to the parent KeyMap instance,
        a ‘namespaces’ iterable attribute with the unconcatenated namespace
        parts for which the instance was allocated, and a ‘prefix’ shortcut
        attribute containing the concatenated namespace parts as a string
        prefix.
        
        Each concrete subclass of KeyMapViewBase registers itself as a
        “virtual subclass” of its corresponding ‘collections.abc’ view
        class, like for good measure.
    """
    
    __slots__ = pytuple('weakref') \
              + tuplize('mapping', 'namespaces', 'submap')
    
    def __init__(self, mapping, *namespaces):
        """ Initialize a view on a KeyMap instance, for a given namespace """
        self.mapping = mapping
        self.namespaces = tuplize(namespaces)
        self.submap = self.mapping.submap(*self.namespaces)
    
    @property
    def _mapping(self): # pragma: no cover
        """ For compatibility with “collections.abc” stuff """
        return self.mapping
    
    def __len__(self):
        return len(self.submap)
    
    def __getitem__(self, idx):
        if isnumber(idx):
            return tuple(self.submap)[idx]
        if isnormative(idx):
            return self.submap[idx]
        tn = typename(idx)
        raise KeyError(f"bad index type: {tn}")
    
    @abstract
    def __contains__(self, nskey):
        ...
    
    @abstract
    def __iter__(self):
        ...
    
    def __repr__(self):
        tn = typename(self)
        nslist = ', '.join(self.namespaces)
        ns = bool(self.namespaces) and f"«{nslist}»" or ''
        return f"{tn}{ns}({self.mapping!r})"

@export
@collections.abc.KeysView.register
class KeyMapKeysView(KeyMapViewBase,
                     collections.abc.Set):
    
    """ A KeyMap key view. """
    
    _from_iterable = classmethod(set_returner)
    
    def __contains__(self, nskey):
        return nskey in self.submap
    
    def __iter__(self):
        if self.namespaces:
            for nskey in self.mapping:
                if nskey.startswith(self.namespaces):
                    yield nskey
        else:
            yield from self.mapping

@export
@collections.abc.ItemsView.register
class KeyMapItemsView(KeyMapViewBase,
                      collections.abc.Set):
    
    """ A KeyMap items view. """
    
    _from_iterable = classmethod(set_returner)
    
    def __contains__(self, item):
        nskey, value = item
        try:
            contained = self.submap[nskey]
        except KeyError:
            return False
        else:
            return contained is value or contained == value
    
    def __iter__(self):
        if self.namespaces:
            for nskey in self.mapping:
                if nskey.startswith(self.namespaces):
                    yield (nskey, self.mapping[nskey])
        else:
            yield from ((key, self.mapping[key]) for key in self.mapping)

@export
@collections.abc.ValuesView.register
class KeyMapValuesView(KeyMapViewBase,
                       collections.abc.Collection):
    
    """ A KeyMap values view. """
    
    def __contains__(self, value):
        for nskey in self.submap:
            contained = self.submap[nskey]
            if contained is value or contained == value:
                return True
        return False
    
    def __iter__(self):
        if self.namespaces:
            for nskey in self.mapping:
                if nskey.startswith(self.namespaces):
                    yield self.mapping[nskey]
        else:
            yield from (self.mapping[key] for key in self.mapping)

@export
class NamespaceWalkerViewBase(KeyMapViewBase):
    
    """ A view abstract base class tailored to NamespaceWalker types;
        specifically, it overrides “__len__(…)” to better utilize
        the underlying mapping types’ “walk(…)” method.
    """
    
    def __len__(self):
        if not self.namespaces:
            return iterlen(self.mapping.walk())
        return len(self.submap)

@export
@collections.abc.KeysView.register
class NamespaceWalkerKeysView(NamespaceWalkerViewBase,
                              collections.abc.Set):
    
    """ A keys view specifically tailored to NamespaceWalker types. """
    
    _from_iterable = classmethod(set_returner)
    
    def __contains__(self, nskey):
        for *fragments, key, value in self.mapping.walk():
            if not self.namespaces:
                return nskey == key
            if concatenate_ns(*fragments) in self.namespaces:
                return nskey == pack_ns(key, *fragments)
        return False
    
    def __iter__(self):
        if not self.namespaces:
            yield from (pack_ns(key, *frags) for *frags, key, _ in self.mapping.walk())
        else:
            for *fragments, key, value in self.mapping.walk():
                if concatenate_ns(*fragments) in self.namespaces:
                    yield pack_ns(key, *fragments)

@export
@collections.abc.ItemsView.register
class NamespaceWalkerItemsView(NamespaceWalkerViewBase,
                               collections.abc.Set):
    
    """ An items view specifically tailored to NamespaceWalker types. """
    
    _from_iterable = classmethod(set_returner)
    
    def __contains__(self, item):
        nskey, putative = item
        for *fragments, key, value in self.mapping.walk():
            if putative is value or putative == value:
                if not self.namespaces:
                    return nskey == key
                if concatenate_ns(*fragments) in self.namespaces:
                    return nskey == pack_ns(key, *fragments)
        return False
    
    def __iter__(self):
        if not self.namespaces:
            yield from ((pack_ns(key, *frags), val) for *frags, key, val in self.mapping.walk())
        else:
            for *fragments, key, value in self.mapping.walk():
                if concatenate_ns(*fragments) in self.namespaces:
                    yield (pack_ns(key, *fragments), value)

@export
@collections.abc.ValuesView.register
class NamespaceWalkerValuesView(NamespaceWalkerViewBase,
                                collections.abc.Collection):
    
    """ A values view specifically tailored to NamespaceWalker types. """
    
    def __contains__(self, putative):
        for *fragments, key, value in self.mapping.walk():
            if putative is value or putative == value:
                if concatenate_ns(*fragments) in self.namespaces:
                    return True
                if not self.namespaces:
                    return True
        return False
    
    def __iter__(self):
        if not self.namespaces:
            yield from (value for *_, _, value in self.mapping.walk())
        else:
            for *fragments, key, value in self.mapping.walk():
                if concatenate_ns(*fragments) in self.namespaces:
                    yield value
