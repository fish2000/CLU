# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain, zip_longest

iterchain = chain.from_iterable

import abc
import clu.abstract
import collections
import collections.abc
import contextlib
import copy
import os

abstract = abc.abstractmethod

from clu.constants.consts import DEBUG, PROJECT_NAME, NoDefault
from clu.predicates import attr, tuplize, listify
from clu.typology import iterlen, ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

ENVIRONS_SEP = '_'
NAMESPACE_SEP = ':'

typename = lambda thing: type(thing).__name__

def concatenate_ns(*namespaces):
    """ Return the given namespace(s), concatenated with the
        namespace separator.
    """
    return NAMESPACE_SEP.join(namespaces)

def prefix_for(*namespaces):
    """ Return the prefix string for the given namespace(s) """
    ns = concatenate_ns(*namespaces)
    return ns and f"{ns}{NAMESPACE_SEP}" or ns

def strip_ns(nskey):
    """ Strip all namespace-related prefixing from a namespaced key """
    return nskey.rpartition(NAMESPACE_SEP)[-1]

def startswith_ns(putative, prefix):
    """ Boolean predicate to compare a pair of namespace iterables,
        returning True if the first starts with the second.
        
        Do not confuse this with the helper function “compare_ns(…)”,
        defined below, which returns False if the namespace iterables
        in question aren’t exactly alike.
    """
    putative_ns = concatenate_ns(*putative)
    prefix_ns = concatenate_ns(*prefix)
    return putative_ns.startswith(prefix_ns)

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
    
    __slots__ = ('mapping', 'namespaces', 'prefix')
    
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
    def _from_iterable(cls, iterable):
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
    def _from_iterable(cls, iterable):
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
    def _from_iterable(cls, iterable):
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
    def _from_iterable(cls, iterable):
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

# NAMESPACE-MANIPULATION FUNCTION API:

def validate_ns(*namespaces):
    """ Raise a ValueError if any of the given namespaces are invalid. """
    for namespace in namespaces:
        if not namespace.isidentifier():
            raise ValueError(f"Invalid namespace: “{namespace}”")
        if NAMESPACE_SEP in namespace:
            raise ValueError(f"Namespace contains separator: “{namespace}”")

def unpack_ns(nskey):
    """ Unpack a namespaced key into a set of namespaces and a key name.
        
        To wit: if the namespaced key is “yo:dogg:i-heard”, calling “unpack_ns(…)”
        on it will return the tuple ('i-heard', ('yo', 'dogg'));
        
        If the key is not namespaced (like e.g. “wat”) the “unpack_ns(…)”
        call will return the tuple ('wat', tuple()).
    """
    *namespaces, key = nskey.split(NAMESPACE_SEP)
    return key, tuple(namespaces)

def pack_ns(key, *namespaces):
    """ Pack a key and a set of (optional) namespaces into a namespaced key.
        
        To wit: if called as “pack_ns('i-heard, 'yo', 'dogg')” the return
        value will be the string "yo:dogg:i-heard".
        
        If no namespaces are provided (like e.g. “pack_ns('wat')”)
        the return value will be the string "wat".
    """
    return NAMESPACE_SEP.join(chain(namespaces, tuplize(key, expand=False)))

def get_ns(nskey):
    """ Get the namespace portion of a namespaced key as a packed string. """
    return nskey.rpartition(NAMESPACE_SEP)[0]

def compare_ns(iterone, itertwo):
    """ Boolean predicate to compare a pair of namespace iterables, value-by-value """
    for one, two in zip_longest(iterone,
                                itertwo,
                                fillvalue=NoDefault):
        if one != two:
            return False
    return True

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
        """ NamespacedMutableMapping.update([E, ]**F) -> None.
            
            Update D from dict/iterable E and/or F.
        """
        if dictish is not NoDefault:
            if hasattr(dictish, 'items'):
                dictish = dictish.items()
            for key, value in dictish:
                self[key] = value
        if updates:
            self.update(dictish=updates)

# CONCRETE SUBCLASSES: FrozenFlat and Flat

@export
class FrozenFlat(FrozenKeyMap, clu.abstract.ReprWrapper,
                               clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class with a flat internal topology. """
    
    __slots__ = tuplize('dictionary')
    
    def __init__(self, dictionary=None, **updates):
        """ Initialize a flat KeyMap instance from a target dictionary.
            
            The dictionary can contain normal key-value items as long as the
            keys are strings; namespaces can be specified per-key as per the
            output of ‘pack_ns(…)’ (q.v. function definition supra.)
        """
        try:
            super(FrozenFlat, self).__init__(**updates)
        except TypeError:
            super(FrozenFlat, self).__init__()
        if hasattr(dictionary, 'dictionary'):
            dictionary = attr(dictionary, 'dictionary')
        elif hasattr(dictionary, 'flatten'):
            dictionary = attr(dictionary.flatten(), 'dictionary')
        self.dictionary = dict(dictionary or {})
        if updates:
            self.dictionary.update(**updates)
    
    def nestify(self, cls=None):
        """ Articulate a flattened KeyMap instance out into one that is nested. """
        if cls is None:
            cls = Nested
        out = cls()
        out.update(self.dictionary)
        return out
    
    def __iter__(self):
        yield from self.dictionary
    
    def __reversed__(self):
        yield from reversed(self.dictionary.keys())
    
    def __len__(self):
        return len(self.dictionary)
    
    def __contains__(self, nskey):
        return nskey in self.dictionary
    
    def __getitem__(self, nskey):
        return self.dictionary[nskey]
    
    def inner_repr(self):
        return repr(self.dictionary)
    
    def clone(self, deep=False, memo=None):
        copier = deep and copy.deepcopy or copy.copy
        return type(self)(dictionary=copier(self.dictionary))

@export
class Flat(FrozenFlat, KeyMap):
    
    """ A concrete mutable KeyMap class with a flat internal topology. """
    
    def freeze(self):
        return FrozenFlat(dictionary=copy.deepcopy(self.dictionary))
    
    def __setitem__(self, nskey, value):
        self.dictionary[nskey] = value
    
    def __delitem__(self, nskey):
        del self.dictionary[nskey]

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

def DefaultTree(*args, **kwargs):
    """ Initialize a recursive DefaultDict pseudo-tree. """
    return collections.defaultdict(DefaultTree, *args, **kwargs)

def dictify(tree):
    """ Recursively convert a nested mapping to standard dicts. """
    if ismapping(tree):
        return { key : dictify(tree[key]) for key in tree }
    return tree

@export
def mapwalk(mapping, pre=None):
    """ Iteratively walk a nested mapping.
        Based on https://stackoverflow.com/a/12507546/298171
    """
    pre = pre and pre[:] or []
    if ismapping(mapping):
        for key, value in mapping.items():
            if ismapping(value):
                yield from mapwalk(value, pre + [key])
            else:
                yield pre + [key, value]
    else:
        yield mapping

# CONCRETE SUBCLASSES: FrozenNested and Nested

@export
class FrozenNested(NamespaceWalker, clu.abstract.ReprWrapper,
                                    clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class with an articulated –
        or, if you will, a nested – internal topology.
    """
    
    __slots__ = tuplize('tree')
    
    def __init__(self, tree=None, **updates):
        """ Initialize an articulated (née “nested”) KeyMap instance from a
            target nested dictionary (or a “tree” of dicts).
        """
        try:
            super(FrozenNested, self).__init__(**updates)
        except TypeError:
            super(FrozenNested, self).__init__()
        if hasattr(tree, 'tree'):
            tree = attr(tree, 'tree')
        elif hasattr(tree, 'nestify'):
            tree = attr(tree.nestify(), 'tree')
        self.tree = DefaultTree(tree or {})
        if updates:
            self.tree.update(**updates)
    
    def walk(self):
        """ Iteratively walk the nested KeyMap’s tree of dicts. """
        yield from mapwalk(self.tree)
    
    def submap(self, *namespaces, unprefixed=False):
        """ Return a standard dict containing only the namespaced items. """
        # The “unprefixed” codepath is optimized here, the rest
        # delegates up to the ancestor implementation:
        if unprefixed:
            return { key : value for key, value in self.tree.items() \
                                  if not ismapping(value) }
        if not namespaces:
            return dict(self)
        return super().submap(*namespaces)
    
    def inner_repr(self):
        return repr(self.tree)
    
    def clone(self, deep=False, memo=None):
        copier = deep and copy.deepcopy or copy.copy
        return type(self)(tree=copier(self.tree))

@export
class Nested(FrozenNested, KeyMap):
    
    """ A concrete mutable KeyMap class with an articulated (or nested)
        internal topology.
    """
    
    def freeze(self):
        return FrozenNested(tree=copy.deepcopy(self.tree))
    
    def __setitem__(self, nskey, value):
        key, namespaces = unpack_ns(nskey)
        if not namespaces:
            self.tree[key] = value
        else:
            d = self.tree
            for namespace in namespaces:
                try:
                    d = d[namespace]
                except KeyError:
                    d = d[namespace] = type(d)()
            d[key] = value
    
    def __delitem__(self, nskey):
        if nskey in self:
            key, namespaces = unpack_ns(nskey)
            if not namespaces:
                del self.tree[key]
            else:
                d = self.tree
                for namespace in namespaces:
                    d = d[namespace]
                del d[key]
        else:
            raise KeyError(nskey)

# ENVIRONMENT-VARIABLE MANIPULATION API:

def concatenate_env(*namespaces):
    """ Concatenate and UPPERCASE namespaces, per environment variables. """
    return ENVIRONS_SEP.join(namespace.upper() for namespace in namespaces)

def prefix_env(appname, *namespaces):
    """ Determine the environment-variable prefix based on a given
        set of namespaces and the provided “appname” value. Like e.g.,
        for an appname of “YoDogg” and a namespace value of “iheard”,
        the environment variable prefix would work out such that
        a variable with a key value of “youlike” would look like this:
            
            YODOGG_IHEARD_YOULIKE
                                 
            ^^^^^^ ^^^^^^ ^^^^^^^
               |      |      |
               |      |      +––––– mapping key (uppercased)
               |      +–––––––––––– namespaces (uppercased, one value)
               +––––––––––––––––––– app name (uppercased)
    """
    if not appname and not namespaces:
        return ''
    if not appname:
        return concatenate_env(*namespaces) + ENVIRONS_SEP
    if not namespaces:
        return appname.upper() + ENVIRONS_SEP
    return appname.upper() + ENVIRONS_SEP + concatenate_env(*namespaces) + ENVIRONS_SEP

def pack_env(appname, key, *namespaces):
    """ Transform a mapping key, along with optional “namespaces”
        values and the provided “appname” value, into an environment-
        variable name. Like e.g., for an appname of “YoDogg” and
        a namespace value of “iheard”, the environment variable
        prefix would work out such that a variable with a key value
        of “youlike” would look like this:
            
            YODOGG_IHEARD_YOULIKE
                                 
            ^^^^^^ ^^^^^^ ^^^^^^^
               |      |      |
               |      |      +––––– mapping key (uppercased)
               |      +–––––––––––– namespaces (uppercased, one value)
               +––––––––––––––––––– app name (uppercased)
    """
    prefix = prefix_env(appname, *namespaces)
    return f"{prefix}{key.upper()}"

def unpack_env(envkey):
    """ Unpack the appname, possible namespaces, and the key from an environment
        variable key name.
    """
    appname, *namespaces, key = envkey.casefold().split(ENVIRONS_SEP)
    return appname, key, tuple(namespaces)

def nskey_from_env(envkey):
    """ Repack an environment-variable key name as a packed namespace key. """
    appname, *namespaces, key = envkey.casefold().split(ENVIRONS_SEP)
    return appname, pack_ns(key, *namespaces)

def nskey_to_env(appname, nskey):
    """ Repack a packed namespace key, with a given appname, as an environment
        variable key name.
    """
    key, namespaces = unpack_ns(nskey)
    return pack_env(appname, key, *namespaces)

@export
def envwalk(appname, mapping):
    """ Iteratively walk an environment-variable mapping, selecting
        only the variables prefixed for the given appname, and convert
        environment-variable-packed namespaced key-value pairs into
        the format expected for a “walk(…)” function.
    """
    app_prefix = prefix_env(appname)
    for envkey in (ek for ek in mapping.keys() if ek.startswith(app_prefix)):
        an, key, namespaces = unpack_env(envkey)
        assert an == appname
        yield listify(namespaces) + listify(key, mapping[envkey])

# CONCRETE SUBCLASSES: FrozenEnviron and Environ

@export
class FrozenEnviron(NamespaceWalker, clu.abstract.ReprWrapper,
                                     clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class wrapping a
        frozen copy of an environment-variable dictionary.
    """
    
    __slots__ = ('environment', 'appname')
    
    def __init__(self, environment=None, appname=None, **updates):
        """ Initialize a FrozenKeyMap instance wrapping an environment-variable
            dictionary from a target dictionary, with a supplied appname.
        """
        try:
            super(FrozenEnviron, self).__init__(**updates)
        except TypeError:
            super(FrozenEnviron, self).__init__()
        self.appname = appname or PROJECT_NAME
        self.environment = environment is None \
                       and os.environ.copy() \
                        or environment
        if updates:
            self.environment.update(**updates)
    
    def walk(self):
        """ Iteratively walk the backend environment access dictionary. """
        yield from envwalk(self.appname,
                           self.environment)
    
    def __contains__(self, nskey):
        envkey = nskey_to_env(self.appname, nskey)
        return envkey in self.environment
    
    def __getitem__(self, nskey):
        envkey = nskey_to_env(self.appname, nskey)
        return self.environment[envkey]
    
    def hasenv(self, envkey):
        """ Query the backend environment dictionary for a key. """
        return envkey in self.environment
    
    def getenv(self, envkey, default=NoDefault):
        """ Retrieve a key directly from the backend environment. """
        if default is NoDefault:
            return self.environment[envkey]
        try:
            return self.environment[envkey]
        except KeyError:
            return default
    
    def envkeys(self):
        """ Get a view on the dictionary keys from the backend environment. """
        return self.environment.keys()
    
    def inner_repr(self):
        """ Return some readable meta-information about this instance """
        prefix = prefix_env(self.appname)
        nscount = iterlen(self.namespaces())
        keycount = len(self.keys())
        return f"[prefix=“{prefix}*”, namespaces={nscount}, keys={keycount}]"
    
    def clone(self, deep=False, memo=None):
        copier = deep and copy.deepcopy or copy.copy
        return type(self)(tree=copier(self.tree))

@export
class Environ(FrozenEnviron, KeyMap, contextlib.AbstractContextManager):
    
    __slots__ = tuplize('stash')
    
    def __init__(self, environment=None, appname=None, **updates):
        """ Initialize a KeyMap instance wrapping an environment-variable
            dictionary from a target dictionary, with a supplied appname.
        """
        if environment is None:
            environment = os.environ
        try:
            super(Environ, self).__init__(environment=environment,
                                              appname=appname,
                                                    **updates)
        except TypeError:
            super(Environ, self).__init__(environment=environment,
                                              appname=appname)
        self.stash = None
    
    def freeze(self):
        return FrozenEnviron(environment=self.environment.copy(),
                                 appname=self.appname)
    
    def __setitem__(self, nskey, value):
        envkey = nskey_to_env(self.appname, nskey)
        self.environment[envkey] = value
    
    def __delitem__(self, nskey):
        envkey = nskey_to_env(self.appname, nskey)
        del self.environment[envkey]
    
    def setenv(self, envkey, value):
        """ Set the value for a key directly in the backend environment. """
        self.environment[envkey] = value
    
    def unsetenv(self, envkey):
        """ Delete a key directly from the backend environment """
        del self.environment[envkey]
    
    def __enter__(self):
        self.stash = self.environment.copy()
        return self
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        if self.stash:
            try:
                self.environment.clear()
            finally:
                self.environment.update(self.stash)
        self.stash = None
        return exc_type is None

export(ENVIRONS_SEP,  name='ENVIRONS_SEP')
export(NAMESPACE_SEP, name='NAMESPACE_SEP')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline, format_environment
    from pprint import pprint
    
    @inline.fixture
    def nestedmaps():
        """ Private nested-dictionary pseudo-fixture """
        return {'body':   {'declare_i': {'id': {'name': 'i', 'type': 'Identifier'},
                                                'init': {'type': 'Literal', 'value': 2},
                                                'type': 'VariableDeclarator'},
                               'kind': 'var',
                               'type': 'VariableDeclaration',
                               'declare_j': {'id': {'name': 'j', 'type': 'Identifier'},
                                                'init': {'type': 'Literal', 'value': 4},
                                                'type': 'VariableDeclarator'},
                               'kind': 'var',
                               'type': 'VariableDeclaration',
                               'declare_answer': {'id': {'name': 'answer', 'type': 'Identifier'},
                                                'init': {'left': {'name': 'i',
                                                                  'type': 'Identifier'},
                                                         'operator': '*',
                                                         'right': {'name': 'j',
                                                                   'type': 'Identifier'},
                                                         'type': 'BinaryExpression'},
                                                'type': 'VariableDeclarator'},
                               'kind': 'var',
                               'type': 'VariableDeclaration'},
                'type':     'Program'}
    
    @inline.fixture
    def flatdict():
        """ Private flat-dictionary pseudo-fixture """
        out = {}
        for mappingpath in mapwalk(nestedmaps()):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            out[nskey] = value
        return out
    
    @inline.precheck
    def show_nestedmaps():
        print("Nested maps fixture output:")
        pprint(nestedmaps())
    
    @inline
    def test_one():
        """ Simple “mapwalk(…)” content """
        dictderive = tuple(mapwalk(nestedmaps()))
        return dictderive
    
    @inline
    def test_two():
        """ Verbose “mapwalk(…)” content check """
        for mappingpath in mapwalk(nestedmaps()):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            print("NAMESPACES:", ", ".join(namespaces))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_three():
        """ FrozenFlat and Nested equivalence """
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps()):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            flat_dict[nskey] = value
        
        assert flat_dict == flatdict()
        
        flat = FrozenFlat(flat_dict)
        nested = Nested(flat)
        assert nested.flatten() == flat
        assert nested.flatten().dictionary == flatdict()
        assert nested == flat
    
    @inline
    def test_three_pt_five():
        """ Flat, FrozenFlat and Nested equivalence """
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps()):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            flat_dict[nskey] = value
        
        assert flat_dict == flatdict()
        
        flat = Flat(flat_dict)
        frozen_flat = flat.freeze()
        assert frozen_flat == flat
        assert frozen_flat.dictionary == flatdict()
        
        nested = flat.nestify()
        flattened = nested.flatten()
        assert flattened == flat
        assert flattened.dictionary == flatdict()
    
    @inline
    def test_four():
        """ FrozenNested contains namespaced key """
        nested = FrozenNested(tree=nestedmaps())
        
        for mappingpath in mapwalk(nested.tree):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            assert nskey in nested
    
    @inline
    def test_four_pt_five():
        """ Nested (mutable) contains namespaced key """
        nested = Nested(tree=nestedmaps())
        
        for mappingpath in mapwalk(nested.tree):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            assert nskey in nested
    
    @inline
    def test_five():
        """ FrozenNested and Flat roundtrip commutativity """
        nested = FrozenNested(tree=nestedmaps())
        flat = Flat(nested)
        assert flat.nestify() == nested
        assert flat == nested
    
    @inline
    def test_five_pt_five():
        """ Nested (mutable) and FrozenNested commutativity """
        nested = Nested(tree=nestedmaps())
        frozen_nested = nested.freeze()
        assert frozen_nested == nested
        
        flat = nested.flatten()
        renested = flat.nestify()
        assert renested == nested
    
    @inline
    def test_six():
        """ FrozenEnviron and “envwalk(…)” namespaced-key check """
        env = FrozenEnviron()
        
        for *namespaces, key, value in envwalk('clu', os.environ.copy()):
            nskey = pack_ns(key, *namespaces)
            assert nskey in env
    
    @inline
    def test_seven():
        """ Environ with “os.environ” and custom-dict backends """
        env = Environ()
        nenv = env.flatten().nestify()
        wat = Environ(environment={ nskey_to_env('clu', nskey) : value \
                                    for nskey, value \
                                     in nenv.flatten().items() })
        assert env == wat
        assert env.flatten() == nenv
        assert len(env.envkeys()) >= len(env)
        assert len(wat.envkeys()) == len(wat)
    
    @inline
    def test_eight():
        """ FrozenEnviron low-level API """
        env = FrozenEnviron()
        
        for key in env.envkeys():
            assert env.hasenv(key)
            assert env.getenv(key) == os.getenv(key)
        
        # N.B. It looks like the “os.{get,put,unset}env(…)” functions
        # don’t really fucking work the way they should:
        try:
            before = len(env)
            os.environ['CLU_CTX_YODOGG'] = 'I heard you are frozen'
            assert len(env) == before
            assert not env.hasenv('CLU_CTX_YODOGG')
            assert os.getenv('CLU_CTX_YODOGG') == 'I heard you are frozen'
            # print("CLU_CTX_YODOGG:", os.getenv('CLU_CTX_YODOGG'))
        finally:
            # os.unsetenv('CLU_CTX_YODOGG')
            del os.environ['CLU_CTX_YODOGG']
    
    @inline
    def test_eight_pt_five():
        """ Environ (mutable) context-manager API """
        before = len(os.environ)
        assert os.getenv('CLU_CTX_YODOGG') is None
        
        with Environ() as env:
            env.set('yodogg', 'I heard you like managed context', 'ctx')
            assert env.getenv('CLU_CTX_YODOGG') == 'I heard you like managed context'
            assert os.getenv('CLU_CTX_YODOGG') == 'I heard you like managed context'
            assert len(os.environ) == before + 1
        
        # Why can we still access the thing in unmanaged scope???
        assert env.stash is None
        
        assert os.getenv('CLU_CTX_YODOGG') is None
        assert len(os.environ) == before
    
    @inline.diagnostic
    def show_environment():
        """ Show environment variables """
        for envline in format_environment():
            print(envline)
    
    # Run all inline tests:
    inline.test(100)

if __name__ == '__main__':
    test()
