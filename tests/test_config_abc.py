# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

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
    
    def test_FlatOrderedSet_addition(self):
        from clu.config.abc import FlatOrderedSet
        fos0 = FlatOrderedSet('yo', 'dogg')
        fos1 = FlatOrderedSet('iheard', 'youlike')
        fos2 = FlatOrderedSet('yo', 'dogg', 'iheard', 'youlike')
        
        assert fos0 + fos1 == fos2
        assert fos0 + fos2 == fos2
        assert fos0 + ('iheard', 'youlike') == fos2
        assert fos1 + fos2 == FlatOrderedSet('iheard', 'youlike', 'yo', 'dogg')
        assert fos1 + fos0 == FlatOrderedSet('iheard', 'youlike', 'yo', 'dogg')
    
    def test_FlatOrderedSet_sort(self):
        # N.B. could use tests with the “key” argument
        from clu.config.abc import FlatOrderedSet
        stuff = FlatOrderedSet(None, "a", "b", FlatOrderedSet("c", None, "a", "d"))
        summary = FlatOrderedSet("a", "b", "c", "d")
        out_of_order = FlatOrderedSet("b", "d", "a", "c")
        
        assert stuff.sort() == summary.sort()
        assert stuff.sort() == out_of_order.sort()
        assert stuff == out_of_order.sort()
        assert stuff.sort().things == tuple(sorted(out_of_order.things))      
          
        assert stuff.sort(reverse=True) == summary.sort(reverse=True)
        assert stuff.sort(reverse=True) == out_of_order.sort(reverse=True)
        assert stuff.sort(reverse=True).things == tuple(sorted(out_of_order.things, reverse=True))