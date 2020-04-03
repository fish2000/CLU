# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

import clu.abstract
import contextlib
import weakref
import sys

from clu.config.abc import FrozenKeyMap, KeyMap
from clu.naming import qualified_name
from clu.predicates import typeof, none_function
from clu.typespace import types
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def selfcheck(function):
    """ Decorator abstracting a boolean self-check for weakref methods """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if not bool(self):
            typename = type(self).__name__
            raise ValueError(f"{typename} referent is dead")
        return function(self, *args, **kwargs)
    return wrapper

@export
class KeyMapView(FrozenKeyMap, clu.abstract.ReprWrapper,
                               clu.abstract.Cloneable,
                               contextlib.AbstractContextManager):
    
    __slots__ = 'referent'
    
    @classmethod
    def get_basetype(cls):
        return getattr(cls, 'basetype', FrozenKeyMap)
    
    @classmethod
    def check_basetype(cls, instance):
        return isinstance(instance, cls.get_basetype())
    
    def __new__(cls, keymap):
        instance = super().__new__(cls)
        instance.referent = none_function
        return instance
    
    def __init__(self, operand):
        """ Initialize a new KeyMapView, with one required argument – that is:
            
                1) an instance of “BaseType” or a descendant thereof;
                2) a weakref pointing to such an instance; or
                3) an instance of KeyMapView or KeyMapProxy, or a descendant
                   thereof – any instance holding “referent” weakref member
                   pointing to a “BaseType” or descendant instance will do
            
            … TypeError will raise if the provided operand isn’t any kind
              of anything, w/r/t these criteria.
        
        """
        
        if not operand:
            raise ValueError("A valid keymap instance is required")
        
        cls = type(self)
        BaseType = cls.get_basetype()
        
        # Does the operand contain a “referent” weakref (á la another KeyMapView)?
        if isinstance(getattr(operand, 'referent', None), types.Reference):
            self.referent = weakref.ref(operand.referent())
        
        # Is the operand itself a weakref?
        elif isinstance(operand, types.Reference) and cls.check_basetype(operand()):
            self.referent = weakref.ref(operand())
        
        # Is the operand an instance of the BaseType (or a descendant of same)?
        elif cls.check_basetype(operand):
            self.referent = weakref.ref(operand)
        
        # It isn’t any kind of anything:
        else:
            qualname = qualified_name(BaseType)
            raise TypeError(f"An operand descending from “{qualname}” is required")
    
    @selfcheck
    def get_reftype(self):
        return typeof(self.referent())
    
    @selfcheck
    def namespaces(self):
        yield from self.referent().namespaces()
    
    @selfcheck
    def __iter__(self):
        yield from self.referent()
    
    @selfcheck
    def __len__(self):
        return self.referent().__len__()
    
    @selfcheck
    def __contains__(self, nskey):
        return self.referent().__contains__(nskey)
    
    @selfcheck
    def __getitem__(self, nskey):
        return self.referent().__getitem__(nskey)
    
    @selfcheck
    def keys(self, *namespaces, unprefixed=False):
        return self.referent().keys(*namespaces, unprefixed=unprefixed)
    
    @selfcheck
    def items(self, *namespaces, unprefixed=False):
        return self.referent().items(*namespaces, unprefixed=unprefixed)
    
    @selfcheck
    def values(self, *namespaces, unprefixed=False):
        return self.referent().values(*namespaces, unprefixed=unprefixed)
    
    @selfcheck
    def __enter__(self):
        return self.referent()
    
    def __exit__(self, exc_type=None,
                       exc_val=None,
                       exc_tb=None):
        return exc_type is None
    
    def __bool__(self):
        return self.referent() is not None
    
    def inner_repr(self):
        return repr(self.referent())
    
    def clone(self, deep=False, memo=None):
        return type(self)(self.referent())

@export
class KeyMapProxy(KeyMapView, KeyMap):
    
    basetype = KeyMap
    
    @selfcheck
    def freeze(self):
        return KeyMapView(self.referent())
    
    @selfcheck
    def __setitem__(self, nskey, value):
        self.referent().__setitem__(nskey, value)
    
    @selfcheck
    def __delitem__(self, nskey):
        self.referent().__delitem__(nskey)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from clu.config.ns import unpack_ns
    from clu.config.keymap import FrozenFlat, Flat
    from clu.config.keymap import nestedmaps, flatdict
    from pprint import pprint
    
    @inline.precheck
    def show_nestedmaps_fixture():
        """ Pretty-print the “nestedmaps()” fixture """
        pprint(nestedmaps(), indent=4)
    
    def test_one_fn(keymap_type, proxy_type, fixture_fn):
        """ Metafunction test generator for KeyMap proxy types:
            • generate tests for proxy/view type basic functionality
        """
        def test_fn():
            kmap = keymap_type(fixture_fn())
            prox = proxy_type(kmap)
            
            # A keymap is equal to a view/proxy on that keymap:
            assert kmap == prox
            assert len(kmap) == len(prox)
            
            # Ensure the “clone(…)” method works as advertised:
            assert kmap == prox.clone()
            assert kmap.clone() == prox
            
            # Check each namespace across the keymap and proxy:
            for ns0, ns1 in zip(kmap.namespaces(), prox.namespaces()):
                assert ns0 == ns1
            
            # Check the iterable output across the keymap and proxy:
            for iter0, iter1 in zip(kmap, prox):
                assert iter0 == iter1
                assert iter0 in kmap
                assert iter0 in prox
                assert iter1 in kmap
                assert iter1 in prox
            
            # Check the keys of both the keymap and the proxy:
            for keys0, keys1 in zip(kmap.keys(), prox.keys()):
                assert keys0 == keys1
                key0, ns0 = unpack_ns(keys0)
                key1, ns1 = unpack_ns(keys1)
                assert kmap.get(key0, *ns0) == prox.get(key1, *ns1)
                assert kmap.get(key1, *ns1) == prox.get(key0, *ns0)
            
            # Check each of the item tuples of the keymap and the proxy:
            for items0, items1 in zip(kmap.items(), prox.items()):
                key0, val0 = items0
                key1, val1 = items1
                assert key0 == key1
                assert val0 == val1
            
            # Check the values across the keymap and the proxy:
            for val0, val1 in zip(kmap.values(), prox.values()):
                assert val0 == val1
        
        test_fn.__doc__ = """ %s vs. %s """ % (proxy_type.__name__,
                                              keymap_type.__name__)
        
        return test_fn
    
    def test_two_fn(keymap_type, proxy_type0, fixture_fn,
                                              proxy_type1=None,
                                              proxy_type2=None):
        """ Metafunction test generator for KeyMap proxy types:
            • generate tests for views-of-views and weakref integrity
        """
        if not proxy_type1:
            proxy_type1 = proxy_type0
        
        def test_fn():
            nonlocal proxy_type2
            
            # Instantiate:
            #
            #   • a keymap populated from the fixture function,
            #   • a view/proxy instance on that keymap, and
            #   • a second view/proxy instance constructed from
            #       the first.
            #
            # … these view/proxy types might be the same, or they
            #   might be totally different.
            kmap = keymap_type(fixture_fn())
            prox0 = proxy_type0(kmap)
            prox1 = proxy_type1(prox0)
            
            if not proxy_type2:
                if hasattr(kmap, 'freeze'):
                    proxy_type2 = kmap.freeze
                else:
                    proxy_type2 = lambda: proxy_type0(kmap)
            
            # Check that commutative equality holds, across
            # the two view/proxy instances and their referent
            # KeyMap referent instances – KeyMap ABC ancestors
            # don’t specify equality, so these operators will
            # be calling default implementations:
            assert kmap == prox0
            assert kmap == prox1
            assert prox0 == prox1
            
            # Check that the referent instances and the
            # weakrefs themselves are equivalent across
            # both instances:
            assert prox0.referent() == prox1.referent()
            assert prox0.referent == prox1.referent
            
            # Ensure both are Truthy – the weakrefs are valid:
            assert bool(prox0)
            assert bool(prox1)
            
            # Entering the view/proxy context provides
            # a dereferenced handle on the instances’ referent:
            with prox0 as dereferenced:
                assert dereferenced
                assert dereferenced == prox1.referent()
                assert prox1.check_basetype(dereferenced)
                assert isinstance(dereferenced, prox1.get_basetype())
            
            # Entering the view/proxy context provides
            # a dereferenced handle on the instances’ referent:
            with prox1 as dereferenced:
                assert dereferenced
                assert dereferenced == prox0.referent()
                assert prox0.check_basetype(dereferenced)
                assert isinstance(dereferenced, prox0.get_basetype())
            
            # Check the weakref count – N.B. according to its docs,
            # this function is “only for testing” and not
            # actual use, and you can see why:
            assert weakref.getweakrefcount(kmap) > 0 # this isn’t 2 somehow
            
            # Go through the equality checks with a new instance
            # of “proxy_type2()” – which actually is a factory function,
            # q.v. abnove and not a type:
            prox2 = proxy_type2()
            assert kmap == prox2
            assert prox0 == prox2
            assert prox1 == prox2
            assert bool(prox2)
            
            assert weakref.getweakrefcount(kmap) > 0 # this isn’t 2 somehow
        
        test_fn.__doc__ = """ %s of %s (&c.) """ % (proxy_type0.__name__,
                                                    proxy_type1.__name__)
        
        return test_fn
    
    # Add inline test functions using the metafunction test generators:
    inline.add_function(test_one_fn(FrozenFlat, KeyMapView,  flatdict),   'test_one')
    inline.add_function(test_two_fn(FrozenFlat, KeyMapView,  flatdict),   'test_two')
    inline.add_function(test_one_fn(Flat,       KeyMapView,  flatdict),   'test_three')
    inline.add_function(test_one_fn(Flat,       KeyMapProxy, flatdict),   'test_three_point_five')
    inline.add_function(test_two_fn(Flat,       KeyMapProxy, flatdict,
                                                KeyMapView),              'test_four')
    
    # N.B. These two take FUCKING FOREVER to run:
    # inline.add_function(test_one_fn(Nested,     KeyMapView,  nestedmaps), 'test_five')
    # inline.add_function(test_one_fn(Nested,     KeyMapProxy, nestedmaps), 'test_five_point_five')
    
    @inline
    def test_six():
        """ View/Proxy error conditions """
        try:
            KeyMapView(None)
        except ValueError as exc:
            assert "valid keymap instance" in str(exc)
        
        try:
            KeyMapProxy(None)
        except ValueError as exc:
            assert "valid keymap instance" in str(exc)
        
        from clu.config.abc import FlatOrderedSet
        
        try:
            # Passing an empty FlatOrderedSet raises ValueError,
            # as above – the empty FlatOrderedSet is Falsey,
            # soooooooooo:
            KeyMapView(FlatOrderedSet('a', 'b'))
        except TypeError as exc:
            assert "operand descending from" in str(exc)
            assert "clu.config.abc.FrozenKeyMap" in str(exc)
        
        try:
            # Passing an empty FlatOrderedSet raises ValueError,
            # as above – the empty FlatOrderedSet is Falsey,
            # soooooooooo:
            KeyMapProxy(FlatOrderedSet('a', 'b'))
        except TypeError as exc:
            assert "operand descending from" in str(exc)
            assert "clu.config.abc.KeyMap" in str(exc)
    
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
    
    # Run all test functions:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
