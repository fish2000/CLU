# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain, zip_longest

iterchain = chain.from_iterable

import abc
import clu.abstract
import collections
import collections.abc
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

def startswith_ns(longer, putative):
    """ Boolean predicate to compare a pair of namespace iterables,
        returning True if one starts with the other (regardless of
        which starts with which, despite the argument names).
        
        Do not confuse this with the helper function “compare_ns(…)”,
        defined below, which returns False if the namespace iterables
        in question aren’t exactly alike.
    """
    for one, two in zip(putative, longer):
        if one != two:
            return False
    return True

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
            if nskey.startswith(self.prefix):
                if startswith_ns(namespaces, self.namespaces):
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
                if nskey.startswith(self.prefix):
                    if startswith_ns(namespaces, self.namespaces):
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
    
    def __init__(self, dictionary=None, *args, **updates):
        """ Initialize a flat KeyMap instance from a target dictionary.
            
            The dictionary can contain normal key-value items as long as the
            keys are strings; namespaces can be specified per-key as per the
            output of ‘pack_ns(…)’ (q.v. function definition supra.)
        """
        try:
            super(FrozenFlat, self).__init__(*args, **updates)
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
    
    @abstract
    def walk(self):
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

def DefaultTree():
    return collections.defaultdict(DefaultTree)

def dictify(tree):
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
    
    def __init__(self, tree=None, *args, **updates):
        """ Initialize an articulated (née “nested”) KeyMap instance from a
            target nested dictionary (or a “tree” of dicts).
        """
        try:
            super(FrozenNested, self).__init__(*args, **updates)
        except TypeError:
            super(FrozenNested, self).__init__()
        if hasattr(tree, 'tree'):
            tree = attr(tree, 'tree')
        elif hasattr(tree, 'nestify'):
            tree = attr(tree.nestify(), 'tree')
        self.tree = tree or DefaultTree()
        if updates:
            self.tree.update(**updates)
    
    def walk(self):
        """ Iteratively walk the nested KeyMap’s tree of dicts. """
        yield from mapwalk(self.tree)
    
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
        key, namespaces = unpack_ns(nskey)
        if not namespaces:
            del self.tree[key]
        else:
            d = self.tree
            for namespace in namespaces:
                d = d[namespace]
            del d[key]

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
    appname, *namespaces, key = envkey.lower().split(ENVIRONS_SEP)
    return appname, key, tuple(namespaces)

def nskey_from_env(envkey):
    """ Repack an environment-variable key name as a packed namespace key. """
    appname, *namespaces, key = envkey.lower().split(ENVIRONS_SEP)
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
    for envkey in (ek for ek in mapping if ek.startswith(app_prefix)):
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
    
    def __init__(self, environment=None, appname=None, *args, **updates):
        """ Initialize a FrozenKeyMap instance wrapping an environment-variable
            dictionary from a target dictionary, with a supplied appname.
        """
        try:
            super(FrozenEnviron, self).__init__(*args, **updates)
        except TypeError:
            super(FrozenEnviron, self).__init__()
        self.environment = environment or os.environ.copy()
        self.appname = appname or PROJECT_NAME
        if updates:
            self.environment.update(**updates)
    
    def walk(self):
        """ Iteratively walk the environment access dict. """
        yield from envwalk(self.appname,
                           self.environment)
    
    def __contains__(self, nskey):
        envkey = nskey_to_env(self.appname, nskey)
        return envkey in self.environment
    
    def __getitem__(self, nskey):
        envkey = nskey_to_env(self.appname, nskey)
        return self.environment[envkey]
    
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
class Environ(FrozenEnviron, KeyMap):
    
    def __init__(self, environment=None, appname=None, *args, **updates):
        """ Initialize a KeyMap instance wrapping an environment-variable
            dictionary from a target dictionary, with a supplied appname.
        """
        if environment is None:
            environment = os.environ
        try:
            super(Environ, self).__init__(environment=environment,
                                              appname=appname,
                                             *args, **updates)
        except TypeError:
            super(Environ, self).__init__(environment=environment,
                                              appname=appname)
    
    def freeze(self):
        return FrozenEnviron(environment=self.environment.copy(),
                                 appname=self.appname)
    
    def __setitem__(self, nskey, value):
        envkey = nskey_to_env(self.appname, nskey)
        self.environment[envkey] = value
    
    def __delitem__(self, nskey):
        envkey = nskey_to_env(self.appname, nskey)
        del self.environment[envkey]

export(ENVIRONS_SEP,  name='ENVIRONS_SEP')
export(NAMESPACE_SEP, name='NAMESPACE_SEP')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from pprint import pprint
    
    nestedmaps = {'body': {'declare_i': {'id': {'name': 'i', 'type': 'Identifier'},
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
                 'type': 'Program'}
    
    @inline
    def test_one():
        dictderive = tuple(mapwalk(nestedmaps))
        return dictderive
    
    @inline
    def test_two():
        for mappingpath in mapwalk(nestedmaps):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            print("NAMESPACES:", ", ".join(namespaces))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_three():
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            flat_dict[nskey] = value
        
        print(f"FLAT DICTIONARY (length={len(flat_dict)}):")
        pprint(flat_dict, indent=4)
        print()
        
        flat = FrozenFlat(flat_dict)
        
        print(f"FLAT FROZEN INSTANCE (length={len(flat)}):")
        pprint(flat)
        print()
        
        keys = tuple(flat.keys())
        print(f"FLAT KEYS (length={len(keys)}):")
        pprint(keys)
        print()
        
        values = tuple(flat.values())
        print(f"FLAT VALUES (length={len(values)}):")
        pprint(values)
        print()
        
        namespaces = tuple(flat.namespaces())
        print(f"FLAT NAMESPACES (length={len(namespaces)}):")
        pprint(namespaces)
        print()
        
        nested = Nested(flat)
        assert nested.flatten() == flat
        assert nested == flat
    
    @inline
    def test_three_pt_five():
        flat_dict = {}
        
        for mappingpath in mapwalk(nestedmaps):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            flat_dict[nskey] = value
        
        print(f"FLAT DICTIONARY (length={len(flat_dict)}):")
        pprint(flat_dict, indent=4)
        print()
        
        flat = Flat(flat_dict)
        
        print(f"FLAT MUTABLE INSTANCE (length={len(flat)}):")
        pprint(flat)
        print()
        
        keys = tuple(flat.keys())
        print(f"FLAT KEYS (length={len(keys)}):")
        pprint(keys)
        print()
        
        values = tuple(flat.values())
        print(f"FLAT VALUES (length={len(values)}):")
        pprint(values)
        print()
        
        namespaces = tuple(flat.namespaces())
        print(f"FLAT NAMESPACES (length={len(namespaces)}):")
        pprint(namespaces)
        print()
        
        frozen_flat = flat.freeze()
        assert frozen_flat == flat
        
        nested = flat.nestify()
        flattened = nested.flatten()
        assert flattened == flat
    
    @inline
    def test_four():
        nested = FrozenNested(tree=nestedmaps)
        
        for mappingpath in mapwalk(nested.tree):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            print("NAMESPACES:", ", ".join(namespaces))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_four_pt_five():
        nested = Nested(tree=nestedmaps)
        
        for mappingpath in mapwalk(nested.tree):
            *namespaces, key, value = mappingpath
            nskey = pack_ns(key, *namespaces)
            print("NAMESPACES:", ", ".join(namespaces))
            print("KEY:", key)
            print("NSKEY:", nskey)
            print("VALUE:", value)
            print()
    
    @inline
    def test_four_pt_seven():
        nested = FrozenNested(tree=nestedmaps)
        
        print(f"NESTED FROZEN INSTANCE (length={len(nested)}):")
        pprint(nested)
        print()
        
        keys = tuple(nested.keys())
        print(f"NESTED KEYS (length={len(keys)}):")
        pprint(keys)
        print()
        
        values = tuple(nested.values())
        print(f"NESTED VALUES (length={len(values)}):")
        pprint(values)
        print()
        
        namespaces = tuple(nested.namespaces())
        print(f"NESTED NAMESPACES (length={len(namespaces)}):")
        pprint(namespaces)
        print()
        
        flat = Flat(nested)
        assert flat.nestify() == nested
        assert flat == nested
    
    @inline
    def test_five():
        nested = Nested(tree=nestedmaps)
        
        print(f"NESTED MUTABLE INSTANCE (length={len(nested)}):")
        pprint(nested)
        print()
        
        keys = tuple(nested.keys())
        print(f"NESTED KEYS (length={len(keys)}):")
        pprint(keys)
        print()
        
        values = tuple(nested.values())
        print(f"NESTED VALUES (length={len(values)}):")
        pprint(values)
        print()
        
        namespaces = tuple(nested.namespaces())
        print(f"NESTED NAMESPACES (length={len(namespaces)}):")
        pprint(namespaces)
        print()
        
        frozen_nested = nested.freeze()
        assert frozen_nested == nested
        
        flat = nested.flatten()
        renested = flat.nestify()
        assert renested == nested
    
    @inline
    def test_six():
        for *namespaces, key, value in envwalk('clu', os.environ.copy()):
            print("NAMESPACES:", namespaces)
            print("KEY:", f"«{key}»")
            print("VALUE:", f"“{value}”")
            print()
    
    print()
    pprint(nestedmaps)
    
    # Run all inline tests:
    inline.test(100)
    # inline.test()
    # test_five()
    # test_six()

if __name__ == '__main__':
    test()
