# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain

iterchain = chain.from_iterable

import abc
import clu.abstract
import collections
import collections.abc
import contextlib
import copy
import os
import sys

abstract = abc.abstractmethod

from clu.constants.consts import PROJECT_NAME
from clu.constants.consts import NoDefault
from clu.config.abc import FrozenKeyMap, KeyMap, NamespaceWalker
from clu.config.ns import unpack_ns, pack_ns
from clu.config.ns import prefix_env, unpack_env, nskey_to_env
from clu.predicates import attr, tuplize, listify
from clu.typology import iterlen, ismapping
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

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

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

from clu.testing.utils import inline, format_environment

@inline.fixture
def nestedmaps():
    """ Nested-dictionary fixture function """
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
    """ Flat-dictionary fixture function """
    out = {}
    for mappingpath in mapwalk(nestedmaps()):
        *namespaces, key, value = mappingpath
        nskey = pack_ns(key, *namespaces)
        out[nskey] = value
    return out

def test():
    
    from pprint import pprint
    
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
    
    @inline.diagnostic
    def show_fixture_cache_stats():
        """ Show the per-fixture-function cache stats """
        total = len(inline.fixtures)
        for idx, name in enumerate(inline.fixtures.keys()):
            if idx > 0:
                print()
            print(f"FUNCTION CACHE INFO: {name} ({idx+1} of {total})")
            print(inline.fixtures[name].cache_info())
    
    # Run all inline tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
