# -*- coding: utf-8 -*-
from __future__ import print_function

import clu.abstract
import contextlib
import copy
import os
import sys

from clu.constants.consts import APPNAME, NoDefault
from clu.config.abc import KeyMap, NamespaceWalker
from clu.config.ns import pack_ns, prefix_env, unpack_env, nskey_from_env, nskey_to_env
from clu.typology import iterlen
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# CONCRETE SUBCLASSES: FrozenEnviron and Environ

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
        yield namespaces + [key, mapping[envkey]]

@export
class FrozenEnviron(NamespaceWalker, clu.abstract.ReprWrapper,
                                     clu.abstract.Cloneable):
    
    """ A concrete immutable – or frozen – KeyMap class wrapping a
        frozen copy of an environment-variable dictionary.
    """
    
    __slots__ = ('environment', 'appname')
    
    @classmethod
    def from_dict(cls, instance_dict):
        """ Used by `clu.config.codecs` to deserialize keymaps """
        return cls(environment=instance_dict['environment'],
                       appname=instance_dict['appname'])
    
    def __init__(self, environment=None, appname=None, **updates):
        """ Initialize a FrozenKeyMap instance wrapping an environment-variable
            dictionary from a target dictionary, with a supplied appname.
        """
        try:
            super().__init__(**updates)
        except TypeError:
            super().__init__()
        self.appname = appname or APPNAME
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
    
    def inner_repr(self): # pragma: no cover
        """ Return some readable meta-information about this instance """
        prefix = prefix_env(self.appname)
        nscount = iterlen(self.namespaces())
        keycount = len(self.keys())
        return f"[prefix=“{prefix}*”, namespaces={nscount}, keys={keycount}]"
    
    def clone(self, deep=False, memo=None):
        copier = deep and copy.deepcopy or copy.copy
        out = type(self)(appname=self.appname)
        out.environment = copier(self.environment)
        return out
    
    def to_dict(self):
        """ Used by `clu.config.codecs` to serialize the keymap """
        return { 'environment'  : copy.deepcopy(self.environment),
                 'appname'      : self.appname }

@export
class Environ(FrozenEnviron, KeyMap, contextlib.AbstractContextManager):
    
    __slots__ = 'stash'
    
    def __init__(self, environment=None, appname=None, **updates):
        """ Initialize a KeyMap instance wrapping an environment-variable
            dictionary from a target dictionary, with a supplied appname.
        """
        if environment is None:
            environment = os.environ
        try:
            super().__init__(environment=environment,
                                 appname=appname,
                                       **updates)
        except TypeError:
            super().__init__(environment=environment,
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
        try:
            self.environment.clear()
        finally:
            self.environment.update(self.stash or {})
        self.stash = None
        return exc_type is None
    
    def to_dict(self):
        """ Used by `clu.config.codecs` to serialize the keymap """
        return { 'environment'  : None, # reconstitution uses os.environ
                 'appname'      : self.appname }

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline, format_environment
    from clu.config.keymap import nestedmaps
    from pprint import pprint
    
    @inline.precheck
    def show_nestedmaps():
        print("Nested maps fixture output:")
        pprint(nestedmaps())
    
    @inline
    def test_one():
        """ FrozenEnviron and “envwalk(…)” namespaced-key check """
        env = FrozenEnviron()
        
        for *namespaces, key, value in envwalk('clu', os.environ.copy()):
            nskey = pack_ns(key, *namespaces)
            assert nskey in env
    
    @inline
    def test_one_pt_five():
        """ FrozenEnviron and “envwalk(…)” with ‘updates’ kwargs """
        updates = { 'yo' : 'dogg', 'iheard' : 'you like' }
        env = FrozenEnviron(**updates)
        
        for *namespaces, key, value in envwalk('clu', os.environ.copy()):
            nskey = pack_ns(key, *namespaces)
            assert nskey in env
        
        # getenv(…) key check:
        for key in updates.keys():
            assert env.getenv(key) == updates[key]
        
        # bad-key getenv(…) without default -
        # raises a KeyError:
        try:
            env.getenv('wat')
        except KeyError as exc:
            assert 'wat' in str(exc)
        
        # bad-key getenv(…) with default:
        assert env.getenv('WTF', 'HAX') == 'HAX'
    
    @inline
    def test_two():
        """ Environ with “os.environ” and custom-dict backends """
        env = Environ()
        fenv = env.freeze()
        nenv = env.flatten().nestify()
        
        wat = Environ(environment={ nskey_to_env('clu', nskey) : value \
                                    for nskey, value \
                                     in nenv.flatten().items() })
        
        assert env == wat
        assert fenv == wat
        assert env.flatten() == nenv
        
        assert len(env.envkeys()) >= len(env)
        assert len(wat.envkeys()) == len(wat)
        
        env.setenv('wtf', 'hax')
        assert 'wtf' not in wat
        env.unsetenv('wtf')
    
    @inline
    def test_three():
        """ FrozenEnviron low-level API """
        env = FrozenEnviron()
        
        for key in env.clone().envkeys():
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
        finally:
            del os.environ['CLU_CTX_YODOGG']
    
    @inline
    def test_three_pt_five():
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
    
    @inline
    def test_four():
        """ Check “prefix_env(…)” edge-case handling """
        # not appname, not namespaces:
        assert prefix_env(None) == ''
        
        # not appname:
        assert prefix_env(None, 'do', 're', 'mi') == 'DO_RE_MI_'
        
        # not namespaces:
        assert prefix_env('yodogg') == 'YODOGG_'
        
        # yes to both:
        assert prefix_env('yodogg', 'do', 're', 'mi') == 'YODOGG_DO_RE_MI_'
        
        # nskey_from_env(…) checks:
        assert nskey_from_env('YODOGG_DO_RE_MI_KEY') == ('yodogg', 'do:re:mi:key')
        assert nskey_from_env('YODOGG_KEY') == ('yodogg', 'key')
        assert nskey_from_env('YODOGG_') == ('yodogg', '')
    
    @inline.diagnostic
    def show_environment():
        """ Show environment variables """
        for envline in format_environment():
            print(envline)
    
    @inline.diagnostic
    def show_fixture_cache_stats():
        """ Show the per-fixture-function cache stats """
        from clu.config.keymap import inline as keymap_inline
        from clu.dicts import merge_fast_two
        
        fixtures = merge_fast_two(inline.fixtures,
                           keymap_inline.fixtures)
        total = len(fixtures)
        
        for idx, name in enumerate(fixtures.keys()):
            if idx > 0:
                print()
            print(f"FUNCTION CACHE INFO: {name} ({idx+1} of {total})")
            print(fixtures[name].cache_info())
    
    # Run all inline tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())