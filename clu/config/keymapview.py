# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import clu.abstract
import collections
import collections.abc

abstract = abc.abstractmethod

from clu.constants.consts import pytuple
from clu.config.ns import (concatenate_ns,
                           prefix_for,
                           startswith_ns,
                           pack_ns)

from clu.predicates import tuplize
from clu.typology import iterlen
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

typename = lambda thing: type(thing).__name__

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
              + tuplize('mapping', 'namespaces', 'prefix')
    
    def __init__(self, mapping, *namespaces):
        """ Initialize a view on a KeyMap instance, for a given namespace """
        self.mapping = mapping
        self.namespaces = namespaces
        self.prefix = prefix_for(*namespaces)
    
    @property
    def _mapping(self):
        """ For compatibility with “collections.abc” stuff """
        return self.mapping
    
    def __len__(self):
        if not self.prefix:
            return len(self.mapping)
        return len([nskey \
                for nskey in self.mapping \
                 if nskey.startswith(self.prefix)])
    
    def __getitem__(self, idx):
        return tuple(self)[idx]
    
    @abstract
    def __contains__(self, nskey):
        ...
    
    @abstract
    def __iter__(self):
        ...
    
    def __repr__(self):
        tn = typename(self)
        nslist = ', '.join(self.namespaces)
        ns = bool(self.prefix) and f"<{nslist}>" or ''
        return f"{tn}{ns}({self.mapping!r})"

@export
@collections.abc.KeysView.register
class KeyMapKeysView(KeyMapViewBase,
                     collections.abc.Set):
    
    """ A KeyMap key view. """
    
    @classmethod
    def _from_iterable(cls, iterable): # pragma: no cover
        # Required by the “collections.abc.Set” API:
        return set(iterable)
    
    def __contains__(self, nskey):
        return nskey in self.mapping.submap(*self.namespaces)
    
    def __iter__(self):
        yield from (nskey \
                for nskey in self.mapping \
                 if nskey.startswith(self.prefix))

@export
@collections.abc.ItemsView.register
class KeyMapItemsView(KeyMapViewBase,
                      collections.abc.Set):
    
    """ A KeyMap items view. """
    
    @classmethod
    def _from_iterable(cls, iterable): # pragma: no cover
        # Required by the “collections.abc.Set” API:
        return set(iterable)
    
    def __contains__(self, item):
        nskey, value = item
        try:
            contained = self.mapping.submap(*self.namespaces)[nskey]
        except KeyError:
            return False
        else:
            return contained is value or contained == value
    
    def __iter__(self):
        yield from ((nskey, self.mapping[nskey]) \
                 for nskey in self.mapping \
                  if nskey.startswith(self.prefix))

@export
@collections.abc.ValuesView.register
class KeyMapValuesView(KeyMapViewBase,
                       collections.abc.Collection):
    
    """ A KeyMap values view. """
    
    def __contains__(self, value):
        submap = self.mapping.submap(*self.namespaces)
        for nskey in submap:
            contained = submap[nskey]
            if contained is value or contained == value:
                return True
        return False
    
    def __iter__(self):
        yield from (self.mapping[nskey] \
                             for nskey in self.mapping \
                              if nskey.startswith(self.prefix))

@export
class NamespaceWalkerViewBase(KeyMapViewBase):
    
    """ A view abstract base class tailored to NamespaceWalker types;
        specifically, it overrides “__len__(…)” to better utilize
        the underlying mapping types’ “walk(…)” method.
    """
    
    def __len__(self):
        if not self.prefix:
            return iterlen(self.mapping.walk())
        return iterlen(concatenate_ns(*namespaces) \
                                  for *namespaces, _, _ in self.mapping.walk() \
                                   if startswith_ns(namespaces,
                                               self.namespaces))

@export
@collections.abc.KeysView.register
class NamespaceWalkerKeysView(NamespaceWalkerViewBase,
                              collections.abc.Set):
    
    """ A keys view specifically tailored to NamespaceWalker types. """
    
    @classmethod
    def _from_iterable(cls, iterable): # pragma: no cover
        # Required by the “collections.abc.Set” API:
        return set(iterable)
    
    def __contains__(self, nskey):
        for *namespaces, key, value in self.mapping.walk():
            if startswith_ns(namespaces, self.namespaces):
                if nskey == pack_ns(key, *namespaces):
                    return True
        return False
    
    def __iter__(self):
        for *namespaces, key, value in self.mapping.walk():
            if startswith_ns(namespaces, self.namespaces):
                yield pack_ns(key, *namespaces)

@export
@collections.abc.ItemsView.register
class NamespaceWalkerItemsView(NamespaceWalkerViewBase,
                               collections.abc.Set):
    
    """ An items view specifically tailored to NamespaceWalker types. """
    
    @classmethod
    def _from_iterable(cls, iterable): # pragma: no cover
        # Required by the “collections.abc.Set” API:
        return set(iterable)
    
    def __contains__(self, item):
        nskey, putative = item
        for *namespaces, key, value in self.mapping.walk():
            if putative is value or putative == value:
                if startswith_ns(namespaces, self.namespaces):
                    if nskey == pack_ns(key, *namespaces):
                        return True
        return False
    
    def __iter__(self):
        for *namespaces, key, value in self.mapping.walk():
            if startswith_ns(namespaces, self.namespaces):
                yield (pack_ns(key, *namespaces), value)

@export
@collections.abc.ValuesView.register
class NamespaceWalkerValuesView(NamespaceWalkerViewBase,
                                collections.abc.Collection):
    
    """ A values view specifically tailored to NamespaceWalker types. """
    
    def __contains__(self, putative):
        for *namespaces, key, value in self.mapping.walk():
            if putative is value or putative == value:
                if startswith_ns(namespaces, self.namespaces):
                    return True
        return False
    
    def __iter__(self):
        for *namespaces, key, value in self.mapping.walk():
            if startswith_ns(namespaces, self.namespaces):
                yield value
