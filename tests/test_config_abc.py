# -*- coding: utf-8 -*-
from __future__ import print_function

class TestConfigABC(object):
    
    def test_FlatOrderedSet_equality_operator(self):
        from clu.config.abc import FlatOrderedSet
        
        stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
        summary = FlatOrderedSet("a", "b", "c", "d")
        
        assert stuff.things == summary.things
        assert stuff == summary
        assert not stuff.isdisjoint(summary)
    
    def test_FlatOrderedSet_fancy_indexing(self):
        from clu.config.abc import FlatOrderedSet
        
        stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
        summary = FlatOrderedSet("a", "b", "c", "d")
        
        assert stuff == summary
        assert stuff[1:] == summary[1:]
        assert type(stuff[1:]) is FlatOrderedSet
        assert type(summary[1:]) is FlatOrderedSet