# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

# @pytest.fixture(scope='module')
# def fosets():

class TestConfigABC(object):
    
    def test_FlatOrderedSet_equality_operator(self):
        from clu.config.abc import FlatOrderedSet
        
        stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
        summary = FlatOrderedSet("a", "b", "c", "d")
        
        assert stuff.things == summary.things
        assert stuff == summary
        assert not stuff.isdisjoint(summary)
        
        assert stuff == ("a", "b", "c", "d")
        assert summary == ("a", "b", "c", "d")
    
    def test_FlatOrderedSet_fancy_indexing(self):
        from clu.config.abc import FlatOrderedSet
        
        stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
        summary = FlatOrderedSet("a", "b", "c", "d")
        
        assert stuff == summary
        assert stuff[1:] == summary[1:]
        
        assert type(stuff[1:]) is FlatOrderedSet
        assert type(summary[1:]) is FlatOrderedSet
    
    def test_FlatOrderedSet_repr(self):
        from clu.config.abc import FlatOrderedSet
        from clu.repr import chop_instance_repr
        
        stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
        summary = FlatOrderedSet("a", "b", "c", "d")
        
        assert stuff == summary
        assert chop_instance_repr(stuff) == chop_instance_repr(summary)
        assert chop_instance_repr(stuff) == "FlatOrderedSet('a', 'b', 'c', 'd')"
        assert chop_instance_repr(summary) == "FlatOrderedSet('a', 'b', 'c', 'd')"