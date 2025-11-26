# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import signal
if not hasattr(signal, 'SIGHUP'):
    signal.SIGHUP = 1
if not hasattr(signal, 'SIGQUIT'):
    signal.SIGQUIT = 3
if not hasattr(signal, 'SIGSTOP'):
    signal.SIGSTOP = 19
from unittest.mock import MagicMock

# Mock zict if not present
try:
    import zict
except ImportError:
    zict = MagicMock()
    class MockLRU(dict):
        def __init__(self, *args, **kwargs):
            if len(args) > 1:
                self.update(args[1])
    zict.LRU = MockLRU
    sys.modules['zict'] = zict

from clu.config.ns import namespace_matches, startswith_ns
from clu.config.abc import FrozenKeyMap
from clu.config.legacy.base import Flat
from clu.config.keymap import Nested, Flat as KeymapFlat
from clu.constants.consts import NAMESPACE_SEP

class MyMap(FrozenKeyMap):
    __slots__ = ('data',)
    def __init__(self, data):
        self.data = data
    def __iter__(self):
        return iter(self.data)
    def __len__(self):
        return len(self.data)
    def __getitem__(self, key):
        return self.data[key]
    def namespaces(self):
        return [] 
    def to_dict(self):
        return self.data
    def __contains__(self, key):
        return key in self.data
    def __hash__(self):
        return 0

FrozenMyMap = MyMap

def test_namespace_matches_exact():
    sep = NAMESPACE_SEP
    assert namespace_matches("foo", "foo")
    assert namespace_matches(f"foo{sep}bar", f"foo{sep}bar")

def test_namespace_matches_prefix():
    sep = NAMESPACE_SEP
    assert namespace_matches(f"foo{sep}bar", "foo")
    assert namespace_matches(f"foo{sep}bar{sep}baz", "foo")

def test_namespace_matches_negative():
    sep = NAMESPACE_SEP
    assert not namespace_matches("foo", "bar")
    assert not namespace_matches("foobar", "foo")
    assert not namespace_matches(f"foo.bar", "foo") 
    assert not namespace_matches("foo", f"foo{sep}bar")

def test_startswith_ns_wrapper():
    # startswith_ns takes iterables of fragments
    assert startswith_ns(("foo", "bar"), ("foo",))
    assert startswith_ns(("foo", "bar"), ("foo", "bar"))
    assert not startswith_ns(("foo",), ("foo", "bar"))
    assert not startswith_ns(("foobar",), ("foo",))

def test_frozenkeymap_submap_integration():
    sep = NAMESPACE_SEP
    data = {
        "foo": 1,
        f"foo{sep}bar": 2,
        f"foo{sep}bar{sep}baz": 3,
        "foobar": 4,
        "other": 5
    }
    m = MyMap(data)
    
    # Test submap
    sub = m.submap("foo")
    assert "foo" in sub
    assert f"foo{sep}bar" in sub
    assert f"foo{sep}bar{sep}baz" in sub
    assert "foobar" not in sub
    assert "other" not in sub
    
    # Test exact match
    sub2 = m.submap(f"foo{sep}bar")
    assert f"foo{sep}bar" in sub2
    assert f"foo{sep}bar{sep}baz" in sub2
    assert "foo" not in sub2

def test_flat_keys_values_namespace_filtering():
    sep = NAMESPACE_SEP
    
    # Test Legacy Flat
    data = {
        "foo": 1,
        f"foo{sep}bar": 2,
        "other": 3
    }
    flat = Flat(data)
    
    # Test keys
    keys = list(flat.keys("foo"))
    assert f"foo{sep}bar" in keys
    assert "foo" in keys
    assert "other" not in keys
    
    # Test values
    values = list(flat.values("foo"))
    assert 1 in values
    assert 2 in values
    assert 3 not in values

    # Test KeymapFlat
    data2 = {
        "foo": 1,
        f"foo{sep}bar": 2,
        "other": 3
    }
    flat2 = KeymapFlat(data2)
    
    # Test keys
    keys2 = list(flat2.keys("foo"))
    assert f"foo{sep}bar" in keys2
    assert "foo" in keys2
    assert "other" not in keys2
    
    # Test values
    values2 = list(flat2.values("foo"))
    assert 1 in values2
    assert 2 in values2
    assert 3 not in values2

def test_namespacewalker_integration():
    sep = NAMESPACE_SEP
    # Nested expects nested dicts.
    # Nested keys are NOT namespaced strings in the input dict, but structure.
    # But Nested.keys(namespace) returns namespaced keys.
    n = Nested({"foo": {"bar": 1}})
    
    # Test keys view with namespace prefix
    keys_foo = n.keys("foo")
    # "foo" -> {"bar": 1}
    # keys should be "foo:bar" (or "foo;bar")
    assert f"foo{sep}bar" in keys_foo
    
    # Test keys view with exact namespace match (should be empty for this data)
    keys_foobar = n.keys(f"foo{sep}bar")
    assert f"foo{sep}bar" not in keys_foobar
    
    # Test negative
    keys_bar = n.keys("bar")
    assert f"foo{sep}bar" not in keys_bar
