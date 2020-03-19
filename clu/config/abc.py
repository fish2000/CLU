# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import clu.abstract
import collections
import collections.abc
import copy

abstract = abc.abstractmethod

from clu.constants.consts import DEBUG, NAMESPACE_SEP, NoDefault, pytuple
from clu.config.ns import concatenate_ns, prefix_for
from clu.config.ns import unpack_ns, pack_ns, get_ns, compare_ns
from clu.config.keymapview import KeyMapKeysView, KeyMapItemsView, KeyMapValuesView
from clu.config.keymapview import NamespaceWalkerKeysView, NamespaceWalkerItemsView
from clu.config.keymapview import NamespaceWalkerValuesView

from clu.predicates import (isexpandable, iscontainer, isnotnone,
                            always, uncallable, tuplize)

from clu.typology import iterlen
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# SUB-BASE AND ABSTRACT BASE CLASSES:

@export
class FrozenKeyMapBase(collections.abc.Mapping,
                       collections.abc.Reversible,
                       metaclass=clu.abstract.Slotted):
    
    """ Abstract sub-base interface class for immutable namespaced mappings.
        This is the root of the namespaced-mapping (née “KeyMap”) class tower.
        
        Don’t subclass this, it’s just a bunch of abstract dunder methods and
        other stuff to pass the buck properly from the ‘collections.abc’ bases
        on up to our own API. You, for your purposes, should employ “FrozenKeyMap”
        (without the “Base”) – q.v. the class definition below, sub.
    """
    __slots__ = pytuple('weakref')
    
    @abstract
    def namespaces(self):
        """ Iterate over all of the namespaces defined in the mapping. """
        ...
    
    @abstract
    def __iter__(self):
        ...
    
    @abstract
    def __len__(self):
        ...
    
    @abstract
    def __contains__(self, nskey):
        ...
    
    @abstract
    def __getitem__(self, nskey):
        ...
    
    def __reversed__(self):
        yield from reversed(tuple(self))
    
    def __missing__(self, nskey):
        if DEBUG:
            print(f"__missing__(…): {nskey}")
        raise KeyError(nskey)
    
    def __bool__(self):
        return len(self) > 0

@export
class KeyMapBase(FrozenKeyMapBase,
                 collections.abc.MutableMapping):
    
    """ Abstract sub-base interface class for mutable namespaced mappings.
        
        Don’t subclass this anemic vestigial thing. You want “KeyMap” (sans
        the “Base”) as your ancestor; see below.
    """
    
    @abstract
    def freeze(self):
        """ Return a “frozen” – or immutable – version of the KeyMap instance. """
        ...
    
    @abstract
    def __setitem__(self, nskey, value):
        ...
    
    @abstract
    def __delitem__(self, nskey):
        ...

@export
class FrozenKeyMap(FrozenKeyMapBase):
    
    """ The abstract base class for frozen – immutable once created – namespaced mappings,
        also known as “FrozenKeyMaps”.
        
        Subclasses must implement a bunch of typical Python dunder methods like e.g.
        ‘__iter__’, ‘__len__’ &c, plus a “namespaces()” method which takes no arguments
        and then iterates in order over all the THATS RIGHT YOU GUESSED IT namespaces
        contained in the KeyMap’s keys.
        
        Optionally one may override ‘__missing__’, which can be kind of interesting,
        and ‘__bool__’ which generally is less so. Q.v. the “FrozenKeyMapBase” source
        supra. for further deets, my doggie
    """
    
    def get(self, key, *namespaces, default=NoDefault):
        """ Retrieve a (possibly namespaced) value for a given key.
            
            An optional default value may be specified, to be returned
            if the key in question is not found in the mapping.
        """
        nskey = pack_ns(key, *namespaces)
        if default is NoDefault:
            return self[nskey]
        if nskey in self:
            return self[nskey]
        return default
    
    def submap(self, *namespaces, unprefixed=False):
        """ Return a standard dict containing only the namespaced items. """
        if unprefixed:
            return { nskey : self[nskey] for nskey in self if NAMESPACE_SEP not in nskey }
        if not namespaces:
            return dict(self)
        prefix = prefix_for(*namespaces)
        return { nskey : self[nskey] for nskey in self if nskey.startswith(prefix) }
    
    def keys(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all keys in the mapping,
            or over only those keys in the mapping matching the specified
            namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).keys()
        return KeyMapKeysView(self, *namespaces)
    
    def items(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all key/value pairs in the
            mapping, or over only those key/value pairs in the mapping whose
            keys match the specified namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).items()
        return KeyMapItemsView(self, *namespaces)
    
    def values(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all values in the mapping,
            or over only those values in the mapping whose keys match the
            specified namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).values()
        return KeyMapValuesView(self, *namespaces)
    
    def namespaces(self):
        """ Iterate over all of the namespaces defined in the mapping.
            
            This is the generic implementation. It depends on “__iter__(…)”,
            as implemented by the concrete descendant.
        """
        nss = { get_ns(nskey) for nskey in self if NAMESPACE_SEP in nskey }
        yield from sorted(nss)

@export
class KeyMap(KeyMapBase, FrozenKeyMap):
    
    """ The abstract base class for mutable namespaced mappings (née “KeyMaps”).
        
        Subclasses must implement all the requisite Python dunder methods required by
        the ancestor “FrozenKeyMap”, like e.g. ‘__iter__’, ‘__len__’ &c, plus also a
        “namespaces()” method which takes no arguments and iterates in order over all
        namespaces contained in the KeyMap’s keys.
        
        OK AND FURTHERMORE for mutability, you also need to do your own ‘__setattr__’
        and ‘__delattr__’ (which maybe we’ll make that last one optional as delete
        methods in Python are totally gauche and a sign of a sort of naïve vulgar
        un-Pythonicism, I feel like).
        
        Optionally one may override ‘__missing__’, which can be kind of interesting,
        and ‘__bool__’ which generally is less so. Q.v. the “FrozenKeyMapBase” source
        supra. for further deets, my doggie
    """
    
    def set(self, key, value, *namespaces):
        """ Set a (possibly namespaced) value for a given key. """
        nskey = pack_ns(key, *namespaces)
        self[nskey] = value
    
    def delete(self, key, *namespaces):
        """ Delete a (possibly namespaced) value from the mapping. """
        nskey = pack_ns(key, *namespaces)
        del self[nskey]
    
    def pop(self, key, *namespaces, default=NoDefault):
        """ Pop a (possibly namespaced) value off the mapping
            and eitehr return it or a default if it doesn’t
            exist – raising a KeyError if no default is given.
        """
        value = self.get(key, *namespaces, default=default)
        if value == default or value is default:
            return value
        self.delete(key, *namespaces)
        return value
    
    def clear(self, *namespaces, unprefixed=False):
        """ Remove all items from the mapping – either in totality,
            or only those matching a specific namespace.
        """
        if unprefixed:
            for key in self.submap(unprefixed=unprefixed).keys():
                del self[key]
            return None
        if not namespaces:
            return super().clear()
        prefix = prefix_for(*namespaces)
        for nskey in self:
            if nskey.startswith(prefix):
                del self[nskey]
        return None
    
    def update(self, dictish=NoDefault, **updates):
        """ KeyMap.update([E, ]**F) -> None.
            
            Update D from dict/iterable E and/or F.
        """
        if dictish is not NoDefault:
            if hasattr(dictish, 'items'):
                dictish = dictish.items()
            for key, value in dictish:
                self[key] = value
        if updates:
            self.update(dictish=updates)

# INTERIM ABSTRACT BASE: NamespaceWalker

@export
class NamespaceWalker(FrozenKeyMap):
    
    """ A NamespaceWalker type implements a “walk(…)” method for iterating
        over namespaced key-value items.
        
        In return for furnishing this one method, NamespaceWalkers receive
        implementations for “__iter__()”, “__len__()”, “__contains__(…)”,
        and “__getitem__(…)”, plus optimized view-types returned from their
        “keys(…)”, “items(…)” and “values(…)” calls, a “flatten(…)” method,
        and an optimized version of the “namespaces()” method, ALL FREE!!
        
        For KeyMap types whose backend mechanics are well-suited to being
        “walked” (as it were) this is a remarkably good deal, would you not
        agree??
        
        See the docstring for “NamespaceWalker.walk(…)” for details. The
        original “walk(…)” output format and model implementation were 
        derived from this StackOverflow answer:
        
            • https://stackoverflow.com/a/12507546/298171
    """
    
    @abstract
    def walk(self):
        """ The “walk(…)” method backs all other “NamespaceWalker” methods.
            
            Concrete subclasses must implement “walk(…)” such that it iterates
            over all items in a given instance, yielding them in a form like:
            
                for *namespaces, key, value in self.walk():
                    # …
            
            … So an item with no namespaces would yield “['key', 'value']”,
            but one with three would yield “['do', 're', 'me', 'key', 'value']”.
            
            See the “mapwalk(…)” and “envwalk(…)” function implementations,
            for practical examples of how this can work. “mapwalk(…)” iterates
            over nested dictionaries-of-dictionaries, and “envwalk(…)” transforms
            the values in an environment dictionary (like ‘os.environ’) into the
            above namespaced-key-value format, as noted.
            
            N.B. Implementors may wish to write their own less-näive versions of
            “__contains__(…)” and “__getitem__(…)” in their subclasses, depending
            on how such subclasses work internally – in many cases, implementing
            these methods using domain-specific logic will be faster and/or less
            pathological than doing so using only “walk(…)”.
        """
        ...
    
    def flatten(self, cls=None):
        """ Dearticulate an articulated KeyMap instance into one that is flat. """
        if cls is None:
            from clu.config.keymap import Flat
            cls = Flat
        out = cls()
        for *namespaces, key, value in self.walk():
            out.set(key, value, *namespaces)
        return out
    
    def namespaces(self):
        """ Iterate over all of the namespaces defined in the mapping. """
        nss = set()
        for *namespaces, key, value in self.walk():
            if namespaces:
                nss.add(concatenate_ns(*namespaces))
        yield from sorted(nss)
    
    def keys(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all keys in the mapping,
            or over only those keys in the mapping matching the specified
            namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).keys()
        return NamespaceWalkerKeysView(self, *namespaces)
    
    def items(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all key/value pairs in the
            mapping, or over only those key/value pairs in the mapping whose
            keys match the specified namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).items()
        return NamespaceWalkerItemsView(self, *namespaces)
    
    def values(self, *namespaces, unprefixed=False):
        """ Return a namespaced view over either all values in the mapping,
            or over only those values in the mapping whose keys match the
            specified namespace values.
        """
        if unprefixed:
            return self.submap(unprefixed=unprefixed).values()
        return NamespaceWalkerValuesView(self, *namespaces)
    
    def __iter__(self):
        for *namespaces, key, value in self.walk():
            yield pack_ns(key, *namespaces)
    
    def __len__(self):
        return iterlen(self.walk())
    
    def __contains__(self, nskey):
        key, namespaces = unpack_ns(nskey)
        for *ns, k, value in self.walk():
            if k == key:
                if compare_ns(ns, namespaces):
                    return True
        return False
    
    def __getitem__(self, nskey):
        key, namespaces = unpack_ns(nskey)
        for *ns, k, value in self.walk():
            if k == key:
                if compare_ns(ns, namespaces):
                    return value
        raise KeyError(nskey)

# NON-KEYMAP ABC STRUCTURES: FlatOrderedSet

@export
class FlatOrderedSet(collections.abc.Set,
                     collections.abc.Sequence,
                     collections.abc.Reversible,
                     collections.abc.Hashable, clu.abstract.Cloneable,
                                               clu.abstract.ReprWrapper,
                                               metaclass=clu.abstract.Slotted):
    
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
    
    @classmethod
    def is_a(cls, instance):
        return isinstance(instance, (cls, FlatOrderedSet)) or \
               isinstance(getattr(instance, 'things', None),
                                  collections.abc.Iterable)
    
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
                if type(self).is_a(thing):
                    for other in thing.things:
                        if predicate(other):
                            if other not in thinglist:
                                thinglist.append(other)
                elif predicate(thing):
                    if thing not in thinglist:
                        thinglist.append(thing)
        self.things = tuple(thinglist)
    
    def __iter__(self):
        yield from self.things
    
    def __reversed__(self):
        yield from reversed(self.things)
    
    def __len__(self):
        return len(self.things)
    
    def __contains__(self, thing):
        return thing in self.things
    
    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.things[idx]
        return type(self)(*self.things[idx])
    
    def __bool__(self):
        return len(self.things) > 0
    
    def __hash__(self):
        return hash(self.things) & hash(id(self.things))
    
    def __eq__(self, other):
        if not type(self).is_a(other):
            return NotImplemented
        return self.things == other.things
    
    def __ne__(self, other):
        if not type(self).is_a(other):
            return NotImplemented
        return self.things != other.things
    
    def clone(self, deep=False, memo=None):
        # Q.v. https://stackoverflow.com/a/48550898/298171
        cls = type(self)
        out = cls.__new__(cls)
        things = list()
        copier = getattr(copy, deep and 'deepcopy' or 'copy')
        for thing in self.things:
            things.append(copier(thing))
        super(cls, out).__init__(*things)
        return out
    
    def inner_repr(self):
        # N.B. string-indexing strips off the parens,
        # which are superfluous as “inner_repr(…)” will
        # add its own parens by default
        return repr(self.things)[1:-1]

# CONCRETE CALLABLE SUBTYPES: functional_and, functional_set

@export
class functional_and(FlatOrderedSet,
                     collections.abc.Callable):
    
    """ The “functional_and” FlatOrderedSet subclass is designed to hold
        a sequence of functions. Instances of “functional_and” are callable –
        calling “functional_and_instance(thing)” will apply each item held
        by the instance to “thing”, returning True only if the instances’
        functions all return a Truthy value. 
    """
    
    def __init__(self, *functions):
        """ Initialize a “functional_and” callable FlatOrderedSet with a list
            of unary boolean functions.
        """
        super(functional_and, self).__init__(predicate=callable, *functions)
    
    def __call__(self, *args):
        """ Apply each of the functions held by this “functional_and” instance;
            True is returned if all of the functions return a Truthy value –
            otherwise, False is returned.
        """
        return all(function(*args) \
               for function in self \
                if function is not None)

@export
class functional_set(FlatOrderedSet,
                     collections.abc.Callable):
    
    """ The “functional_set” FlatOrderedSet subclass is designed to hold
        a sequence of functions. Instances of “functional_set” are callable –
        calling “functional_set_instance(thing)” will successively apply
        each function to either “thing” or the return value of the previous
        function – finally returning the last return value when the sequence
        of functions has been exhausted.
    """
    
    def __init__(self, *functions):
        """ Initialize a “functional_and” callable FlatOrderedSet with a list
            of functions accepting a “thing” and returning something like it.
        """
        super(functional_set, self).__init__(predicate=callable, *functions)
    
    def __call__(self, thing):
        """ Apply each of the functions held by this “functional_and” instance
            successively to “thing”, replacing “thing” with the return value of
            each function in turn, and finally returning the last return value
            once the sequence of functions has been exhausted.
        """
        for function in reversed(tuple(filter(isnotnone, self))):
            if function is not None:
                thing = function(thing)
        return thing

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
