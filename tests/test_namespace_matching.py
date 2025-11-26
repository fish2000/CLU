# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from unittest.mock import MagicMock

# Mock zict if not present
try:
    import zict
except ImportError:
    zict = MagicMock()
    class MockLRU(dict):
        def __init__(self, n, d):
            self.update(d)
    zict.LRU = MockLRU
    sys.modules['zict'] = zict

import unittest
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

class TestNamespaceMatching(unittest.TestCase):
    
    def test_namespace_matches(self):
        sep = NAMESPACE_SEP
        self.assertTrue(namespace_matches("foo", "foo"))
        self.assertTrue(namespace_matches(f"foo{sep}bar", "foo"))
        self.assertTrue(namespace_matches(f"foo{sep}bar{sep}baz", "foo"))
        self.assertTrue(namespace_matches(f"foo{sep}bar", f"foo{sep}bar"))
        
        self.assertFalse(namespace_matches("foo", "bar"))
        self.assertFalse(namespace_matches("foobar", "foo"))
        self.assertFalse(namespace_matches(f"foo.bar", "foo")) 
        self.assertFalse(namespace_matches("foo", f"foo{sep}bar"))

    def test_startswith_ns(self):
        # startswith_ns takes iterables of fragments
        self.assertTrue(startswith_ns(("foo", "bar"), ("foo",)))
        self.assertTrue(startswith_ns(("foo", "bar"), ("foo", "bar")))
        self.assertFalse(startswith_ns(("foo",), ("foo", "bar")))
        self.assertFalse(startswith_ns(("foobar",), ("foo",)))

    def test_frozen_keymap_submap(self):
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
        self.assertIn("foo", sub)
        self.assertIn(f"foo{sep}bar", sub)
        self.assertIn(f"foo{sep}bar{sep}baz", sub)
        self.assertNotIn("foobar", sub)
        self.assertNotIn("other", sub)
        
        # Test exact match
        sub2 = m.submap(f"foo{sep}bar")
        self.assertIn(f"foo{sep}bar", sub2)
        self.assertIn(f"foo{sep}bar{sep}baz", sub2)
        self.assertNotIn("foo", sub2)

    def test_flat_keys_values(self):
        sep = NAMESPACE_SEP
        data = {
            "foo": 1,
            f"foo{sep}bar": 2,
            "other": 3
        }
        flat = Flat(data)
        
        # Test keys
        keys = list(flat.keys("foo"))
        self.assertIn(f"foo{sep}bar", keys)
        self.assertIn("foo", keys)
        self.assertNotIn("other", keys)
        
        # Test values
        values = list(flat.values("foo"))
        self.assertIn(1, values)
        self.assertIn(2, values)
        self.assertNotIn(3, values)

    def test_namespace_walker_views(self):
        sep = NAMESPACE_SEP
        # Nested expects nested dicts.
        # Nested keys are NOT namespaced strings in the input dict, but structure.
        # But Nested.keys(namespace) returns namespaced keys.
        n = Nested({"foo": {"bar": 1}})
        
        # Test keys view with namespace prefix
        keys_foo = n.keys("foo")
        # "foo" -> {"bar": 1}
        # keys should be "foo:bar" (or "foo;bar")
        self.assertIn(f"foo{sep}bar", keys_foo)
        
        # Test keys view with exact namespace match (should be empty for this data)
        keys_foobar = n.keys(f"foo{sep}bar")
        self.assertNotIn(f"foo{sep}bar", keys_foobar)
        
        # Test negative
        keys_bar = n.keys("bar")
        self.assertNotIn(f"foo{sep}bar", keys_bar)

    def test_keymap_flat_keys_values(self):
        sep = NAMESPACE_SEP
        data = {
            "foo": 1,
            f"foo{sep}bar": 2,
            "other": 3
        }
        flat = KeymapFlat(data)
        
        # Test keys
        keys = list(flat.keys("foo"))
        self.assertIn(f"foo{sep}bar", keys)
        self.assertIn("foo", keys)
        self.assertNotIn("other", keys)
        
        # Test values
        values = list(flat.values("foo"))
        self.assertIn(1, values)
        self.assertIn(2, values)
        self.assertNotIn(3, values)

if __name__ == '__main__':
    unittest.main()
