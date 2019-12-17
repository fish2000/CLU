# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestPredicates(object):
    
    """ Run the tests for the clu.predicates module. """
    
    def test_try_items_and_item_search(self):
        from clu.predicates import try_items, item_search
        from collections import defaultdict as DefaultDict
        
        dict_one = {
            'yo'    : "dogg",
            'i'     : "heard",
            'you'   : "liked",
            'dict'  : "chains" }
        
        dict_two = {
            'so'    : "SOOOOO",
            'yeah'  : "YEAH",
            'what'  : "WHAAAAT",
            'is'    : "ISSSSS",
            'up'    : "UP?" }
        
        assert item_search('yo', dict_one, dict_two) == "dogg"
        assert item_search('so', dict_one, dict_two) == "SOOOOO"
        assert try_items('yo', dict_one, dict_two) == "dogg"
        assert try_items('so', dict_one, dict_two) == "SOOOOO"
        
        dict_default = DefaultDict(lambda: "WTF")
        
        assert item_search('yo', dict_one, dict_default) == "dogg"
        assert item_search('so', dict_one, dict_default) is None # “item_search(…)” default value
        assert try_items('yo', dict_one, dict_default) == "dogg"
        assert try_items('so', dict_one, dict_default) == "WTF" # DefaultDict factory value
    
    def test_ancestral_and_ancestral_union(self):
        from clu.predicates import ancestral_union
        from clu.fs.filesystem import Directory, TemporaryDirectory
        
        fields = ('name', 'old', 'new', 'exists',
                  'will_change', 'did_change', 'will_change_back', 'did_change_back')
        
        morefields = ('name', 'old', 'new', 'exists',
                      'will_change', 'did_change', 'will_change_back', 'did_change_back',
                      'destroy', 'prefix', 'suffix', 'parent')
        
        assert ancestral_union('fields', Directory) == fields
        assert ancestral_union('fields', TemporaryDirectory) == morefields
    
    def test_union(self):
        from clu.predicates import listify, union
        
        l0 = listify("yo", "dogg", "I", "heard", "you", "like", "dogg", "yo", "don't")
        l1 = listify("yo", "dogg", "I", "heard", "you", "like", "repetitive", "sets")
        lU = union(*l0, *l1)
        lS = union(l0 + l1)
        
        assert lU == { "yo", "dogg", "I", "heard", "you", "don't", "like", "repetitive", "sets" }
        assert lS == { "yo", "dogg", "I", "heard", "you", "don't", "like", "repetitive", "sets" }
    
    def test_negate(self):
        from clu.predicates import negate
        
        def is_even(integer):
            return integer % 2 == 0
        
        assert is_even(2)
        assert is_even(66)
        assert is_even(222)
        assert is_even(6666)
        assert not is_even(3)
        assert not is_even(67)
        assert not is_even(223)
        assert not is_even(6667)
        
        is_odd = negate(is_even)
        
        assert not is_odd(2)
        assert not is_odd(66)
        assert not is_odd(222)
        assert not is_odd(6666)
        assert is_odd(3)
        assert is_odd(67)
        assert is_odd(223)
        assert is_odd(6667)
    
    def test_reverse(self):
        from clu.predicates import reverse, listify
        
        # Sample lists:
        l0 = listify("yo", "dogg", "I", "heard", "you", "like", "ordered", "lists")
        r0 = listify("lists", "ordered", "like", "you", "heard", "I", "dogg", "yo")
        
        # Reverse “listify(…)”:
        backwards = reverse(listify)
        # Ensure the reversed function returns a list:
        backwardsify = lambda *items: list(backwards(item for item in items if item is not None))
        
        # Sample reversed lists:
        l1 = backwardsify("yo", "dogg", "I", "heard", "you", "like", "ordered", "lists")
        r1 = backwardsify("lists", "ordered", "like", "you", "heard", "I", "dogg", "yo")
        
        # Compare:
        assert r0 == l1
        assert l0 == r1
    
    def test_itervariadic_decorator(self):
        from clu.predicates import reverse, itervariadic, listify
        
        l0 = listify("yo", "dogg", "I", "heard", "you", "like", "ordered", "lists")
        r0 = listify("lists", "ordered", "like", "you", "heard", "I", "dogg", "yo")
        
        # Reverse “listify(…)”:
        backwards = reverse(listify)
        # Ensure the reversed function returns a list:
        backwardslist = lambda *items: list(backwards(item for item in items if item is not None))
        # Imbue the wrapped revered function with “itervariadic(¬)” powers:
        backwardsify = itervariadic(backwardslist)
        
        # Sample reversed lists:
        l1 = backwardsify("yo", "dogg", "I", "heard", "you", "like", "ordered", "lists")
        r1 = backwardsify("lists", "ordered", "like", "you", "heard", "I", "dogg", "yo")
        
        # Sample reversed lists from iterables:
        l2 = backwardsify(l0)
        r2 = backwardsify(r0)
        
        # Compare reversed lists from lists:
        assert r0 == l1
        assert l0 == r1
        
        # Compare reversed lists from iterables:
        assert l1 == l2
        assert r1 == r2
    
    def test_mro_and_rmro(self):
        from clu.predicates import mro, rmro
        from clu.predicates import newtype
        
        A = newtype('A')
        B = newtype('B', A)
        C = newtype('C', B)
        D = newtype('D', C)
        
        assert mro(D)           == (D, C, B, A, object)
        assert tuple(rmro(D))   == (object, A, B, C, D)
    
    def test_unwrap(self):
        from clu.predicates import unwrap
        from clu.extending import doubledutch
        
        @doubledutch
        def yodogg(x, y):
            return None
        
        @yodogg.domain(int, int)
        def yodogg(x, y):
            return f"INTS: {x}, {y}"
        
        @yodogg.domain(str, str)
        def yodogg(x, y):
            return f"STRS: {x}, {y}"
        
        @yodogg.annotated
        def yodogg(x: float, y: float):
            return f"FLTS: {x}, {y}"
        
        assert yodogg(None, None) is None
        assert yodogg(22, 333).startswith('INTS')
        assert yodogg(22.22, 333.33).startswith('FLTS')
        assert yodogg('one', 'two').startswith('STRS')
        
        assert unwrap(yodogg)(22, 33) is None
        assert unwrap(yodogg)(22.22, 333.33) is None
        assert unwrap(yodogg)('one', 'two') is None
        
        def not_wrapped():
            return "NOT WRAPPED"
        
        assert not_wrapped() == unwrap(not_wrapped)()
    
    @pytest.mark.TODO
    def test_origin(self):
        # TODO: expand both this test, and what
        # this predicate does – e.g. special-case for
        # “typing._SpecialForm” or whatever the fuck
        from clu.predicates import origin
        import typing as tx
        
        assert origin(tx.Dict) is dict
        assert origin(tx.Dict[str, tx.Any]) is dict
        assert origin(dict) is dict
        assert origin({}) is dict
    
    @pytest.mark.TODO
    def test_isancestor_and_isorigin(self):
        from clu.predicates import isancestor
        from clu.predicates import newtype
        
        A = newtype('A')
        B = newtype('B', A)
        C = newtype('C', B)
        D = newtype('D', C)
        
        assert isancestor(A) # defaults to “object”
        assert isancestor(B) # defaults to “object”
        assert isancestor(C) # defaults to “object”
        assert isancestor(D) # defaults to “object”
        
        assert isancestor(B, A)
        assert isancestor(C, B)
        assert isancestor(D, C)
        
        assert isancestor(B, ancestor=A)
        assert isancestor(C, ancestor=B)
        assert isancestor(D, ancestor=C)
        
        # THIS DOES NOT QUITE WORK.
        # TODO: make it work
        # from clu.predicates import isorigin
        # import typing as tx
        # assert isorigin(tx.Dict,            original=dict)
        # assert isorigin(dict,                 original=tx.Dict)
        # assert isorigin(tx.Dict[str, str],  original=dict)
        # assert isorigin(dict,               original=dict)
        # assert isorigin({},                 original=dict)
    
    def test_newtype(self):
        from clu.predicates import isclass, ismetaclass
        from clu.predicates import newtype
        import abc
        
        # equivalient to class Thingy(object): pass
        Thingy = newtype('Thingy')
        assert isclass(Thingy)
        assert not ismetaclass(Thingy)
        assert Thingy.__name__ == 'Thingy'
        assert Thingy.__qualname__.endswith('Thingy')
        
        # equivalent to class MetaThingy(type): pass
        MetaThingy = newtype('MetaThingy', type)
        assert not isclass(MetaThingy)
        assert ismetaclass(MetaThingy)
        assert MetaThingy.__name__ == 'MetaThingy'
        assert MetaThingy.__qualname__.endswith('MetaThingy')
        
        # equivalent to class DerivedThingy(Thingy): pass
        DerivedThingy = newtype('DerivedThingy', Thingy)
        assert isclass(DerivedThingy)
        assert not ismetaclass(DerivedThingy)
        assert DerivedThingy.__name__ == 'DerivedThingy'
        assert DerivedThingy.__qualname__.endswith('DerivedThingy')
        assert DerivedThingy.__mro__ == (DerivedThingy, Thingy, object)
        
        # equivalent to class AbstractThingy(Thingy, abc.ABC): pass
        AbstractThingy = newtype('AbstractThingy', Thingy, abc.ABC)
        assert isclass(AbstractThingy)
        assert not ismetaclass(AbstractThingy)
        assert AbstractThingy.__name__ == 'AbstractThingy'
        assert AbstractThingy.__qualname__.endswith('AbstractThingy')
        assert AbstractThingy.__mro__ == (AbstractThingy, Thingy, abc.ABC, object)
        
        # equivalent to:
        # class ThingyWithAttrs(Thingy):
        #     yo = 'dogg',
        #     iheard = 'you like attributes'
        ThingyWithAttrs = newtype('ThingyWithAttrs', Thingy, yo='dogg', iheard='you like attributes')
        assert isclass(ThingyWithAttrs)
        assert not ismetaclass(ThingyWithAttrs)
        assert ThingyWithAttrs.__name__ == 'ThingyWithAttrs'
        assert ThingyWithAttrs.__qualname__.endswith('ThingyWithAttrs')
        assert ThingyWithAttrs.__mro__ == (ThingyWithAttrs, Thingy, object)
        assert ThingyWithAttrs.yo == 'dogg'
        assert ThingyWithAttrs.iheard == 'you like attributes'
    
    @pytest.mark.TODO
    def test_static_accessors(self, environment, consts):
        from clu.fs.misc import gethomedir
        from clu.predicates import isclasstype, pyattr
        from clu.predicates import attr, attrs, stattr, stattrs
        # TODO: test *_search and *_across static accessors:
        # from clu.predicates import (attr_search, attr_across,
        #                           stattr_search, stattr_across)
        
        # Non-data descriptor wrapping a R/O value:
        from clu.abstract import ValueDescriptor
        
        # We have to use these irritating default environment values everywhere,
        # in case the testing environment is kertwanged:
        home = environment.get('HOME', gethomedir())
        user = environment.get('USER', consts.USER)
        
        # Non-data descriptor wrapping R/O access to a named environment variable,
        # a default value for that variable, and the variables’ name:
        class EnvironmentName(object):
            
            __slots__ = ('name', 'default')
            
            def __init__(self, name=None, default=None):
                self.default = default
                if name is not None:
                    self.name = name
            
            def __set_name__(self, cls, name):
                if name is not None:
                    self.name = name
            
            def __get__(self, instance=None, cls=None):
                if instance is not None:
                    return environment.get(self.name,
                                           self.default)
                if isclasstype(cls):
                    return self.name
            
            def __repr__(self):
                clsname = pyattr(type(self), 'name', 'qualname')
                selfname =  attr(     self,  'name', 'default')
                return f"{clsname}<[{selfname}]>"
        
        # Slotted type with non-data descriptors,
        # wrapping values and environment variables:
        class Slotted(object):
            __slots__ = ('yo', 'dogg', 'wtf')
            
            hax = ValueDescriptor('HAXXX')
            HOME = EnvironmentName(default=gethomedir())
            USER = EnvironmentName(default=consts.USER)
            
            def __init__(self):
                self.yo: str = "YO"
                self.dogg: str = "DOGG"
                self.wtf: str = "WTFFF"
        
        # Non-slotted (“dictish”) type with non-data descriptors,
        # wrapping values and environment variables:
        class Dictish(object):
            yo: str = "YO"
            dogg: str = "DOGG"
            
            wtf = ValueDescriptor('WTFFF')
            HOME = EnvironmentName(default=gethomedir())
            USER = EnvironmentName(default=consts.USER)
            
            def __init__(self):
                self.hax: str = "HAXXX"
        
        # The basics – Slotted type and instance attributes:
        assert attr(Slotted,    'hax', 'HOME', 'USER') ==  'HAXXX'
        assert attr(Slotted(),  'hax', 'HOME', 'USER') ==  'HAXXX'
        assert attrs(Slotted,   'hax', 'HOME', 'USER') == ('HAXXX', 'HOME', 'USER')
        assert attrs(Slotted(), 'hax', 'HOME', 'USER') == ('HAXXX',  home,   user)
        
        # More basics – Dictish type and instance attributes:
        assert attr(Dictish,    'wtf', 'HOME', 'USER') ==  'WTFFF'
        assert attr(Dictish(),  'wtf', 'HOME', 'USER') ==  'WTFFF'
        assert attrs(Dictish,   'wtf', 'HOME', 'USER') == ('WTFFF', 'HOME', 'USER')
        assert attrs(Dictish(), 'wtf', 'HOME', 'USER') == ('WTFFF',  home,   user)
        
        # Check statically obtained ValueDescriptor instances,
        # from Slotted types and instances:
        assert repr(stattr(Slotted,    'hax', 'HOME', 'USER')) ==                       'HAXXX'
        assert repr(stattr(Slotted(),  'hax', 'HOME', 'USER')) ==                       'HAXXX'
        assert repr(stattr(Slotted,    'hax', 'HOME', 'USER')) ==  repr(ValueDescriptor('HAXXX'))
        assert repr(stattr(Slotted(),  'hax', 'HOME', 'USER')) ==  repr(ValueDescriptor('HAXXX'))
        assert type(stattr(Slotted,    'hax', 'HOME', 'USER')) is       ValueDescriptor
        assert type(stattr(Slotted(),  'hax', 'HOME', 'USER')) is       ValueDescriptor
        # These don’t work (they need ValueDescriptor.__eq__() which might make things weird):
        # assert      stattr(Slotted,    'hax', 'HOME', 'USER')  ==  ValueDescriptor('HAXXX')
        # assert      stattr(Slotted(),  'hax', 'HOME', 'USER')  ==  ValueDescriptor('HAXXX')
        
        # Check statically obtained ValueDescriptor instances,
        # from Dictish types and instances:
        assert repr(stattr(Dictish,    'wtf', 'HOME', 'USER')) ==                       'WTFFF'
        assert repr(stattr(Dictish(),  'wtf', 'HOME', 'USER')) ==                       'WTFFF'
        assert repr(stattr(Dictish,    'wtf', 'HOME', 'USER')) ==  repr(ValueDescriptor('WTFFF'))
        assert repr(stattr(Dictish(),  'wtf', 'HOME', 'USER')) ==  repr(ValueDescriptor('WTFFF'))
        assert type(stattr(Dictish,    'wtf', 'HOME', 'USER')) is       ValueDescriptor
        assert type(stattr(Dictish(),  'wtf', 'HOME', 'USER')) is       ValueDescriptor
        # These don’t work (they need ValueDescriptor.__eq__() which might make things weird):
        # assert      stattr(Dictish,    'wtf', 'HOME', 'USER')  ==  ValueDescriptor('WTFFF')
        # assert      stattr(Dictish(),  'wtf', 'HOME', 'USER')  ==  ValueDescriptor('WTFFF')
        
        # Check statically obtained EnvironmentName instances,
        # from both Slotted and Dictish types and instances:
        assert repr(stattr(Slotted,   'HOME')) == repr(EnvironmentName('HOME', default=gethomedir()))
        assert repr(stattr(Slotted(), 'HOME')) == repr(EnvironmentName('HOME', default=gethomedir()))
        assert repr(stattr(Slotted,   'USER')) == repr(EnvironmentName('USER', default=consts.USER))
        assert repr(stattr(Slotted(), 'USER')) == repr(EnvironmentName('USER', default=consts.USER))
        assert repr(stattr(Slotted,   'HOME')) ==     "EnvironmentName<[HOME]>"
        assert repr(stattr(Slotted(), 'HOME')) ==     "EnvironmentName<[HOME]>"
        assert repr(stattr(Slotted,   'USER')) ==     "EnvironmentName<[USER]>"
        assert repr(stattr(Slotted(), 'USER')) ==     "EnvironmentName<[USER]>"
        assert repr(stattr(Dictish,   'HOME')) == repr(EnvironmentName('HOME', default=gethomedir()))
        assert repr(stattr(Dictish(), 'HOME')) == repr(EnvironmentName('HOME', default=gethomedir()))
        assert repr(stattr(Dictish,   'USER')) == repr(EnvironmentName('USER', default=consts.USER))
        assert repr(stattr(Dictish(), 'USER')) == repr(EnvironmentName('USER', default=consts.USER))
        assert repr(stattr(Dictish,   'HOME')) ==     "EnvironmentName<[HOME]>"
        assert repr(stattr(Dictish(), 'HOME')) ==     "EnvironmentName<[HOME]>"
        assert repr(stattr(Dictish,   'USER')) ==     "EnvironmentName<[USER]>"
        assert repr(stattr(Dictish(), 'USER')) ==     "EnvironmentName<[USER]>"
        
        # Slotted attributes are named descriptors that can compare with __eq__():
        assert stattr(Slotted, 'yo')   == stattr(Slotted(), 'yo')   == attr(Slotted, 'yo')
        assert stattr(Slotted, 'dogg') == stattr(Slotted(), 'dogg') == attr(Slotted, 'dogg')
        assert stattr(Slotted, 'wtf')  == stattr(Slotted(), 'wtf')  == attr(Slotted, 'wtf')
        
        # Dictish attributes are just attributes -- statically obtained attributes come from
        # the class __dict__, while “normally” obtained attributes are probably coming out of
        # the instance __dict__:
        atts = ('yo', 'dogg', 'wtf')
        assert stattrs(Dictish, *atts) == stattrs(Dictish(), *atts) != attrs(Dictish(), *atts)
        
        # N.B. Dictish.hax is a ValueDescriptor instance:
        atts = ('yo', 'dogg', 'hax')
        assert stattrs(Dictish, *atts) != stattrs(Dictish(), *atts) == attrs(Dictish(), *atts)
    
    def test_resolve_accessor(self):
        from clu.predicates import resolve
        from clu.typespace.namespace import SimpleNamespace
        
        ns = SimpleNamespace(yo=SimpleNamespace(
                           dogg=SimpleNamespace(
                         iheard=SimpleNamespace(
                        youlike="namespaces"))))
        
        assert type(ns) is SimpleNamespace
        assert type(ns.yo) is SimpleNamespace
        assert type(ns.yo.dogg) is SimpleNamespace
        assert type(ns.yo.dogg.iheard) is SimpleNamespace
        assert type(ns.yo.dogg.iheard.youlike) is str
        
        assert type(resolve(ns, 'yo')) is SimpleNamespace
        assert type(resolve(ns, 'yo.dogg')) is SimpleNamespace
        assert type(resolve(ns, 'yo.dogg.iheard')) is SimpleNamespace
        assert type(resolve(ns, 'yo.dogg.iheard.youlike')) is str
        
        assert resolve(ns, 'yo.dogg.iheard.youlike') == "namespaces"
        assert resolve(ns, 'yo.dogg.iheard.youlike') == ns.yo.dogg.iheard.youlike
    
    def test_collator_based_accessors(self):
        from clu.predicates import attr_across, pyattr_across, item_across
        from clu.typespace.namespace import Namespace
        
        ns0 = Namespace(yo="Yo Dogg,",
                        dogg="I heard you like",
                        iheard="multidimentional accessors",
                        youlike=None)
        
        ns1 = Namespace(yo="Yo Dogg,",
                        dogg="I heard you like",
                        iheard="polymorpic descriptors",
                        youlike=None)
        
        ns2 = Namespace(yo="Yo Dogg,",
                        dogg="I heard you like",
                        iheard="attribute hypergetters",
                        youlike=None)
        
        ns3 = Namespace(yo="Yo Dogg,",
                        dogg="I heard you like",
                        iheard="object-instance query functors",
                        youlike=None)
        
        # Check “attr_across(…)”:
        assert attr_across('yo', ns0, ns1, ns2, ns3) == ("Yo Dogg,",) * 4
        assert attr_across('dogg', ns0, ns1, ns2, ns3) == ("I heard you like",) * 4
        assert attr_across('iheard', ns0, ns1, ns2, ns3) == ("multidimentional accessors",
                                                             "polymorpic descriptors",
                                                             "attribute hypergetters",
                                                             "object-instance query functors")
        # “youlike” will be None, which won’t get collated:
        assert attr_across('youlike', ns0, ns1, ns2, ns3) == tuple()
        
        # Check “item_across(…)”:
        assert item_across('yo', ns0, ns1, ns2, ns3) == ("Yo Dogg,",) * 4
        assert item_across('dogg', ns0, ns1, ns2, ns3) == ("I heard you like",) * 4
        assert item_across('iheard', ns0, ns1, ns2, ns3) == ("multidimentional accessors",
                                                             "polymorpic descriptors",
                                                             "attribute hypergetters",
                                                             "object-instance query functors")
        # “youlike” will be None, which won’t get collated:
        assert item_across('youlike', ns0, ns1, ns2, ns3) == tuple()
        
        # Check “pyattr_across(…)”:
        assert pyattr_across('abstractmethods', ns0, ns1, ns2, ns3) == (frozenset(),) * 4
        assert pyattr_across('class', ns0, ns1, ns2, ns3) == (Namespace,) * 4
        assert pyattr_across('slots', ns0, ns1, ns2, ns3) == (tuple(),) * 4
        # “__weakref__” will be None, which won’t get collated:
        assert pyattr_across('weakref', ns0, ns1, ns2, ns3) == tuple()
    
    def test_acquirer_based_accessors(self):
        from clu.predicates import attrs, pyattrs, items
        from clu.typespace.namespace import Namespace
        
        ns = Namespace(yo="Yo Dogg,",
                       dogg="I heard you like",
                       iheard="irritating recursion",
                       youlike=None)
        
        # Check “attrs(…)”:
        assert attrs(ns, 'yo', 'dogg', 'iheard') == ("Yo Dogg,",
                                                     "I heard you like",
                                                     "irritating recursion")
        
        assert attrs(ns, 'iheard', 'dogg', 'yo') == ("irritating recursion",
                                                     "I heard you like",
                                                     "Yo Dogg,")
        
        # “youlike” will be None, which won’t get acquired:
        assert attrs(ns, 'yo', 'dogg', 'iheard', 'youlike') == ("Yo Dogg,",
                                                     "I heard you like",
                                                     "irritating recursion")
        
        # Check “items(…)”:
        assert items(ns, 'yo', 'dogg', 'iheard') == ("Yo Dogg,",
                                                     "I heard you like",
                                                     "irritating recursion")
        
        assert items(ns, 'iheard', 'dogg', 'yo') == ("irritating recursion",
                                                     "I heard you like",
                                                     "Yo Dogg,")
        
        # “youlike” will be None, which won’t get acquired:
        assert items(ns, 'yo', 'dogg', 'iheard', 'youlike') == ("Yo Dogg,",
                                                     "I heard you like",
                                                     "irritating recursion")
        
        # Check “pyattrs(…)”:
        assert pyattrs(ns, 'abstractmethods', 'class', 'module', 'slots') == (frozenset(), Namespace,
                                                                             'clu.typespace.namespace',
                                                                              tuple())
        
        # “__weakref__” will be None, which won’t get acquired:
        assert pyattrs(ns, 'abstractmethods', 'class', 'module', 'slots', 'weakref') == (frozenset(), Namespace,
                                                                             'clu.typespace.namespace',
                                                                              tuple())
    
    def test_utility_helpers_for_builtin_predicates(self):
        from clu.predicates import allof, anyof, noneof
        
        all_OK = (True, True, True, True, True)
        any_OK = (False, False, True, False, True)
        non_OK = (False, False, False, False, False)
        
        # What we expect:
        assert all(all_OK)
        assert any(all_OK)
        assert any(any_OK)
        assert not any(non_OK)
        assert not all(any_OK) # … but WHO CARES really;
                               # notice, we don’t have a
                               # “someof(…)” function or
                               # anything like that dogg
        
        # The “real” tests:
        assert allof(*all_OK)
        assert anyof(*all_OK)
        assert anyof(*any_OK)
        assert noneof(*non_OK)
        
        assert allof(True, True, True, True, True)
        assert anyof(True, True, True, True, True)
        assert anyof(False, False, True, False, True)
        assert noneof(False, False, False, False, False)
        
        assert allof(1, 2, 3, 4, 5)
        assert allof([1], [2], [3], [4], [5])
        assert anyof([], {}, tuple(), '', b'b')
        assert anyof(0, 1, 2, 3, 4, 5)
        
        class Falsified(object):
            
            def __bool__(self):
                return False
        
        assert not noneof(0, 1, 2, 3, 4, 5)
        assert not noneof(1, 2, 3, 4, 5)
        assert noneof([], {}, tuple(), '', b'')
        assert noneof(0, None, False, Falsified())
    
    def test_utility_helpers_for_builtin_containers(self):
        """ » Checking “tuplize/uniquify/listify” functions from clu.predicates … """
        from clu.predicates import tuplize, uniquify, listify
        
        t = tuplize("yo", "dogg", "I", "heard", "you", "like", "tuples")
        assert type(t) is tuple
        assert len(t) == 7
        
        u = uniquify("yo", "dogg", "I", "heard", "you", "like", "dogg", "yo")
        assert type(u) is tuple
        assert len(u) == 6
        
        l = listify("yo", "dogg", "I", "heard", "you", "like", "mutable", "lists")
        assert type(l) is list
        assert len(l) == 8
        
        et = tuplize()
        assert type(et) is tuple
        assert len(et) == 0
        
        eu = uniquify()
        assert type(eu) is tuple
        assert len(eu) == 0
        
        el = listify()
        assert type(el) is list
        assert len(el) == 0
    
    def test_slot_aware_attribute_checkers(self):
        """ » Checking “thing/class/slotted/dictish” lambdas from clu.predicates … """
        from clu.predicates import (thing_has, class_has,
                                    isslotted, isdictish, isslotdicty,
                                    slots_for)
        
        class Slotted(object):
            __slots__ = ('yo', 'dogg', 'wtf')
            
            def __init__(self):
                self.yo: str = "YO"
                self.dogg: str = "DOGG"
                self.wtf: str = "WTFFFF"
        
        class Dictish(object):
            yo: str = "YO"
            dogg: str = "DOGG"
            
            def __init__(self):
                self.hax: str = "HAXXX"
        
        assert isslotted(Slotted())
        assert isdictish(Dictish())
        assert not isslotted(Dictish())
        assert not isdictish(Slotted())
        assert not isslotdicty(Slotted())
        assert not isslotdicty(Dictish())
        
        assert thing_has(Slotted, 'yo')
        assert thing_has(Slotted(), 'yo')
        assert thing_has(Slotted, 'dogg')
        assert thing_has(Slotted(), 'dogg')
        assert thing_has(Slotted, 'wtf')
        assert thing_has(Slotted(), 'wtf')
        assert not thing_has(Slotted, 'hax')
        assert not thing_has(Slotted(), 'hax')
        
        assert thing_has(Dictish, 'yo')
        assert thing_has(Dictish(), 'yo')
        assert thing_has(Dictish, 'dogg')
        assert thing_has(Dictish(), 'dogg')
        assert not thing_has(Dictish, 'wtf')
        assert not thing_has(Dictish(), 'wtf')
        # Only installed via __init__ on instance:
        assert not thing_has(Dictish, 'hax')
        assert thing_has(Dictish(), 'hax')
        
        assert class_has(Slotted, 'yo')
        assert class_has(Slotted, 'dogg')
        assert class_has(Slotted, 'wtf')
        assert not class_has(Slotted, 'hax')
        
        assert class_has(Dictish, 'yo')
        assert class_has(Dictish, 'dogg')
        assert not class_has(Dictish, 'wtf')
        assert not class_has(Dictish, 'hax')
        
        class DerivedSlottedNoSlots(Slotted):
            __slots__ = tuple()
        
        class DerivedPlusSomeSlots(DerivedSlottedNoSlots):
            __slots__ = ('i', 'heard', 'you', 'like')
            
            def __init__(self):
                super(DerivedPlusSomeSlots, self).__init__()
                self.i: str = "I"
                self.heard: str = "HEARD"
                self.you: str = "YOU"
                self.like: str = "LIKE SLOTS"
        
        assert slots_for(Slotted)   == ('yo', 'dogg', 'wtf')
        assert slots_for(Slotted()) == ('yo', 'dogg', 'wtf')
        
        assert slots_for(DerivedSlottedNoSlots)   == ('yo', 'dogg', 'wtf')
        assert slots_for(DerivedSlottedNoSlots()) == ('yo', 'dogg', 'wtf')
        
        # Slots returned by “slots_for(…)” start with the lowest base class,
        # and move up through the heirarchy, keeping the slot names in order,
        # as they appear in the iterable specified in the slotted class:
        assert slots_for(DerivedPlusSomeSlots)   == ('yo', 'dogg', 'wtf',
                                                     'i', 'heard', 'you', 'like')
        assert slots_for(DerivedPlusSomeSlots()) == ('yo', 'dogg', 'wtf',
                                                     'i', 'heard', 'you', 'like')
        
        # Non-slotted types passed to “slots_for(…)” yield an empty tuple:
        assert slots_for(Dictish)   == tuple()
        assert slots_for(Dictish()) == tuple()
    
    def test_applyto(self, consts):
        """ » Checking “apply_to(…)” core function from clu.predicates … """
        from string import capwords
        from clu.predicates import apply_to, isclasstype, typeof, uniquify
        from clu.typology import (numeric_types, string_types, bytes_types,
                                  callable_types, array_types, path_types)
        
        # First, test apply_to(…) with invalid arguments (to raise a ValueError):
        with pytest.raises(ValueError) as exc:
            apply_to(isclasstype, "all")
        assert "Noncallable passed to apply_to" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            apply_to("isclasstype", all)
        assert "Noncallable passed to apply_to" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            apply_to("isclasstype", "all")
        assert "Noncallable passed to apply_to" in str(exc.value)
        
        # Test apply_to(…) returning a partial --
        # N.B. this is the exact implementation of actual functions
        # in use in clu.typology:
        istypelist = apply_to(isclasstype, all)
        maketypelist = apply_to(typeof, uniquify)
        
        assert istypelist(consts.SINGLETON_TYPES)
        assert istypelist(numeric_types)
        assert istypelist(string_types)
        assert istypelist(bytes_types)
        assert istypelist(callable_types)
        assert istypelist(array_types)
        assert istypelist(path_types)
        
        one = maketypelist(str, bytes, type, object(), { 'yo' : "dogg" })
        two = maketypelist("yo", "dogg", b"I heard", b"you like", 1337)
        
        assert istypelist(one)
        assert istypelist(two)
        
        # Test apply_to evaluating the application of
        # its function and predicate:
        assert apply_to(lambda thing: type(thing) is str,
                        lambda total: all(total),
                        "yo", "dogg", "I", "heard", "you", "love", "apply_to")
        
        s = lambda by: str(by, encoding=consts.ENCODING)
        r = "Yo Dogg I Heard You Love Apply_to"
        assert apply_to(lambda thing: isinstance(thing, string_types) and thing or s(thing),
                        lambda total: capwords(" ".join(total)),
                        "yo", "dogg", b"I", b"heard", "you", b"love", "apply_to") == r
    
    def test_applyto_predicate_logicals(self):
        """ » Checking “apply_to(…)” derived predicate logicals from clu.predicates … """
        from clu.predicates import (haslength, uncallable, isiterable, isslotted)
        from clu.predicates import (predicate_all, predicate_any, predicate_none,
                                    predicate_and, predicate_or,
                                    predicate_xor)
        
        class Slotted(object):
            __slots__ = ('yo', 'dogg', 'wtf')
            
            def __init__(self):
                self.yo: str = "YO"
                self.dogg: str = "DOGG"
                self.wtf: str = "WTFFFF"
        
        slot = Slotted()
        ttup = ('yo', 'dogg')
        mseq = list(ttup)
        rstr = "yo dogg"
        byts = b"YO DOGG!"
        call = lambda: rstr
        
        # Variadics:
        assert predicate_all(isiterable, ttup, mseq, rstr, byts)
        assert predicate_all(uncallable, slot, ttup, mseq, rstr, byts)
        assert predicate_any(isslotted, slot, ttup, mseq, rstr, byts)
        assert predicate_none(isslotted, ttup, mseq, rstr, byts)
        assert predicate_all(isiterable, rstr, byts, slot.yo, slot.dogg, slot.wtf)
        assert predicate_all(lambda thing: not uncallable(thing), Slotted, call, type)
        assert predicate_any(lambda thing: not uncallable(thing), Slotted, call, type, slot)
        assert predicate_none(uncallable, Slotted, call, type)
        
        # Booleans:
        assert predicate_and(lambda thing: type(thing) is str, slot.yo, slot.dogg)
        assert predicate_and(lambda thing: type(thing) is str, slot.yo, rstr)
        assert predicate_and(lambda thing: type(thing) is str, call(), rstr)
        assert predicate_and(lambda thing: type(thing) is str, call(), ttup[0])
        
        assert not predicate_and(lambda thing: type(thing) is str, call, ttup[0])
        assert not predicate_and(lambda thing: type(thing) is str, slot, ttup[0])
        assert not predicate_and(lambda thing: type(thing) is str, slot, Slotted)
        assert not predicate_and(lambda thing: type(thing) is str, ttup, mseq)
        
        assert predicate_or(haslength, slot, ttup)
        assert predicate_or(haslength, byts, call)
        assert predicate_or(haslength, byts, rstr)
        assert predicate_or(haslength, rstr, rstr)
        assert predicate_or(haslength, rstr, Slotted.__slots__)
        assert predicate_or(haslength, rstr, call())
        
        assert not predicate_or(haslength, slot, Slotted)
        assert not predicate_or(haslength, call, call)
        assert not predicate_or(haslength, call, (s for s in ttup))
        assert not predicate_or(haslength, type, Slotted.__class__)
        assert not predicate_or(haslength, type, type(str))
        
        assert predicate_xor(isiterable, slot, ttup)
        assert predicate_xor(isiterable, ttup, call)
        assert predicate_xor(isiterable, call, Slotted.__slots__)
        assert predicate_xor(isiterable, type, Slotted.__slots__)
        assert predicate_xor(isiterable, type, Slotted.__mro__)
        
        assert not predicate_xor(isiterable, mseq, ttup)
        assert not predicate_xor(isiterable, ttup, call())
        assert not predicate_xor(isiterable, call(), Slotted.__slots__)
        assert not predicate_xor(isiterable, rstr, Slotted.__slots__)
        assert not predicate_xor(isiterable, byts, Slotted.__mro__)
    
    def test_applyto_internal_lambdas(self):
        """ » Checking lambda internals for “apply_to(…)” from clu.predicates … """
        from clu.predicates import (uncallable, isexpandable,
                                                isnormative,
                                                iscontainer)
        
        # Test subjects: in descending order, from
        # the most predicate-satisfying to the least:
        ttup = ('yo', 'dogg')
        mseq = list(ttup)
        genx = (s for s in ttup)
        lcmp = [s for s in ttup]
        rstr = "yo dogg"
        byts = b"YO DOGG!"
        robj = object()
        tobj = object
        
        # Tuples aren’t normative:
        assert uncallable(ttup)
        assert isexpandable(ttup)
        assert not isnormative(ttup)
        assert iscontainer(ttup)
        
        # Mutable sequences (aka lists) aren’t normative:
        assert uncallable(mseq)
        assert isexpandable(mseq)
        assert not isnormative(mseq)
        assert iscontainer(mseq)
        
        # Generator expressions are neither expandable not normative:
        assert uncallable(genx)
        assert not isexpandable(genx)
        assert not isnormative(genx)
        assert iscontainer(genx)
        
        # List comprehensions aren’t normative (they are basically lists):
        assert uncallable(lcmp)
        assert isexpandable(lcmp)
        assert not isnormative(lcmp)
        assert iscontainer(lcmp)
        
        # Strings aren’t expandable, and as they are normative,
        # they’re not containers:
        assert uncallable(rstr)
        assert not isexpandable(rstr)
        assert isnormative(rstr)
        assert not iscontainer(rstr)
        
        # Like strings, bytes aren’t expandable, and since they’re
        # normative, they’re not containers:
        assert uncallable(byts)
        assert not isexpandable(byts)
        assert isnormative(byts)
        assert not iscontainer(byts)
        
        # Instances of object (or derived classes) aren’t going
        # to be expandable, normative, or containers by default:
        assert uncallable(robj)
        assert not isexpandable(robj)
        assert not isnormative(robj)
        assert not iscontainer(robj)
        
        # Classes aren’t uncallable – they are callable! – and
        # like instances, by default they won’t wind up being
        # expandable, normative or containers, without intervention:
        assert not uncallable(tobj)
        assert not isexpandable(tobj)
        assert not isnormative(tobj)
        assert not iscontainer(tobj)
    
    def test_enum_predicates(self):
        """ » Checking “isenum” and “enumchoices” functions from clu.predicates … """
        from clu.predicates import isenum, enumchoices
        from clu.constants.enums import Enum, System, CSIDL
        
        class NotAnEnum(object):
            pass
        
        class TechnicallyAnEnum(Enum):
            pass
        
        assert isenum(System)
        assert isenum(CSIDL)
        assert not isenum(NotAnEnum)
        assert isenum(TechnicallyAnEnum)
        
        assert not isenum(System.DARWIN)
        assert not isenum(System.LINUX)
        assert not isenum(CSIDL.APPDATA)
        assert not isenum(CSIDL.LOCAL_APPDATA)
        
        assert enumchoices(System) == ('DARWIN', 'WIN32', 'LINUX', 'LINUX2')
        assert enumchoices(CSIDL) == ('APPDATA', 'COMMON_APPDATA', 'LOCAL_APPDATA')
        assert enumchoices(NotAnEnum) == tuple()
        assert enumchoices(TechnicallyAnEnum) == tuple()
    
    def test_getattr_shortcuts(self):
        """ » Checking “getattr/getpyattr/getitem” shortcuts from clu.predicates … """
        from random import shuffle
        from clu.constants.consts import NoDefault
        from clu.predicates import (or_none, getpyattr, getitem,
                                    attr, pyattr, item,
                                    attr_search, pyattr_search, item_search)
        
        dict0 = {  'yo' : "dogg"  }
        dict1 = {   'i' : "heard" }
        dict2 = { 'you' : "like"  }
        
        dicts = (dict0, dict1, dict2)
        list_of_dicts = list(dicts)
        
        for d in dicts:
            assert or_none(d, 'get') is not None
            assert or_none(d, 'set') is None
            assert attr(d, 'set', 'delete', 'get') == or_none(d, 'get')
            assert attr(d, 'set', 'delete', default=NoDefault) is NoDefault
            assert pyattr(d, 'bool', 'enter', 'exit', 'class') is dict
            assert pyattr(d, 'bool', 'enter', 'exit', default=NoDefault) is NoDefault
            assert type(item(d, 'yo', 'i', 'you')) is str
            assert item(d, 'yo', 'i', 'you') in ("dogg", "heard", "like")
            assert item(d, 'foo', 'bar', 'baz', default="DOGG") == "DOGG"
        
        assert getitem(dict0, 'yo') == "dogg"
        assert getitem(dict1, 'i') == "heard"
        assert getitem(dict2, 'you') == "like"
        
        shuffle(list_of_dicts)
        assert attr_search('__doc__', *dicts) \
            == attr_search('__doc__', *reversed(dicts)) \
            == attr_search('__doc__', *list_of_dicts)
        
        assert item_search('yo', *dicts) == "dogg"
        assert item_search('i', *dicts) == "heard"
        assert item_search('you', *dicts) == "like"
        
        assert getpyattr(dict0, 'class') \
            is getpyattr(dict1, 'class') \
            is getpyattr(dict2, 'class') \
            is pyattr_search('class', *dicts)
    
    @pytest.mark.TODO
    def test_nops(self):
        """ » Checking “always/never/nuhuh/no_op” lambdas from clu.predicates … """
        # TODO: get rid of most of these “nop” functions – many are unused
        from clu.predicates import (negate, 
                                    always, never, nuhuh,
                                    no_op, predicate_nop,
                                            function_nop)
        
        singles = (True, False, None)
        
        for single in singles:
            assert always(single) is True
            assert never(single) is False
            assert nuhuh(single) is None
            assert negate(always)(single) is False
            assert negate(never)(single) is True
            assert negate(nuhuh)(single) is True # not not None is True
            assert no_op(single, 'get') is single
            assert predicate_nop(*singles) is None
            assert function_nop(single) is None
    
    def test_ismergeable(self):
        """ » Checking “ismergeable” lambda from clu.predicates … """
        from clu.predicates import ismergeable
        from clu.typespace import Namespace, SimpleNamespace
        from collections import OrderedDict, defaultdict
        
        dic = { 'yo' : "dogg" }
        odc = OrderedDict({ 'i_heard' : "you liked" })
        ddc = defaultdict(lambda: "wat", { "mergeable" : "instances" })
        nsi = Namespace(dogg="yo")
        sns = SimpleNamespace(dogg="yo")
        
        assert ismergeable(dic)
        assert ismergeable(odc)
        assert ismergeable(ddc)
        assert ismergeable(nsi)
        assert not ismergeable(sns)
        
        class TechnicallyMergeable(object):
            """ This is to show the limitations of the predicate """
            __getitem__ = "wtf"
            __contains__ = "hax"
        
        assert ismergeable(TechnicallyMergeable)
        assert ismergeable(TechnicallyMergeable())
    
    def test_isiterable(self):
        """ » Checking “isiterable” lambda from clu.predicates … """
        from clu.predicates import isiterable
        
        ttup = ('yo', 'dogg')
        mseq = list(ttup)
        genx = (s for s in ttup)
        rstr = "yo dogg"
        robj = object()
        
        assert isiterable(ttup)
        assert isiterable(mseq)
        assert isiterable(genx)
        assert isiterable(rstr)
        assert not isiterable(robj)
        assert not isiterable(isiterable)
        assert not isiterable(self)
        
        class TechnicallyIterable(object):
            """ This is to show the limitations of the predicate """
            __iter__ = "wtf"
            __getitem__ = "hax"
        
        assert isiterable(TechnicallyIterable)
        assert isiterable(TechnicallyIterable())
    
    def test_haslength(self):
        """ » Checking “haslength” lambda from clu.predicates … """
        from clu.predicates import haslength
        
        ttup = ('yo', 'dogg')
        mseq = list(ttup)
        genx = (s for s in ttup)
        lcmp = [s for s in ttup]
        rstr = "yo dogg"
        robj = object()
        
        assert haslength(ttup)
        assert haslength(mseq)
        assert not haslength(genx) # hahaaa
        assert haslength(lcmp)
        assert haslength(rstr)
        assert not haslength(robj)
        assert not haslength(haslength)
        assert not haslength(self)
        
        class TechnicallyLengthy(object):
            """ This is to show the limitations of the predicate """
            __len__ = "YO DOGG"
        
        assert haslength(TechnicallyLengthy)
        assert haslength(TechnicallyLengthy())
    
    def test_hasattr_shortcuts(self):
        """ » Checking “hasattr/haspyattr” shortcuts from clu.predicates … """
        from clu.predicates import (noattr, haspyattr, nopyattr,
                                    anyattrs, allattrs, noattrs,
                                    anypyattrs, allpyattrs, nopyattrs)
        
        assert noattr(object, 'base')
        assert noattr(object, 'class')
        assert not noattr(object, 'mro')
        
        assert not hasattr(object, 'base')
        assert not hasattr(object, 'class')
        assert hasattr(object, 'mro')
        
        assert haspyattr(object, 'base')
        assert haspyattr(object, 'class')
        assert haspyattr(object, 'mro')
        assert not haspyattr(object, 'yo')
        assert not haspyattr(object, 'dogg')
        assert not haspyattr(object, 'wtf')
        
        assert not nopyattr(object, 'base')
        assert not nopyattr(object, 'class')
        assert not nopyattr(object, 'mro')
        assert nopyattr(object, 'yo')
        assert nopyattr(object, 'dogg')
        assert nopyattr(object, 'wtf')
        
        assert anyattrs(object, 'base', 'class', 'mro')
        assert not allattrs(object, 'base', 'class', 'mro')
        assert not anyattrs(object, 'yo', 'dogg', 'i', 'have', 'not', 'heard')
        assert allattrs(object, '__base__', '__class__', '__mro__')
        assert noattrs(object, 'yo', 'dogg', 'i', 'have', 'not', 'heard')
        assert not noattrs(object, 'base', 'class', 'mro')
        
        assert anypyattrs(object, 'yo', 'dogg', 'mro')
        assert not allpyattrs(object, 'yo', 'dogg', 'mro')
        assert not anypyattrs(object, 'yo', 'dogg', 'wtf')
        assert nopyattrs(object, 'yo', 'dogg', 'wtf')
        assert not nopyattrs(object, 'yo', 'dogg', 'mro')
        
        assert allpyattrs(object, 'base', 'class', 'mro',
                                  'call', 'dict', 'doc',
                                  'name', 'hash', 'dir')
    
    def test_class_predicates(self):
        """ » Checking “ismetaclass/isclass/isclasstype/metaclass/typeof” from clu.predicates … """
        from clu.predicates import (ismetaclass,
                                    isclass,
                                    isclasstype,
                                    metaclass, typeof)
        
        class Class(object):
            pass
        
        class MetaClass(type):
            pass
        
        class ClassWithMeta(Class, metaclass=MetaClass):
            pass
        
        assert isclass(Class)
        assert isclasstype(Class)
        assert not ismetaclass(Class)
        
        assert isclass(ClassWithMeta)
        assert isclasstype(ClassWithMeta)
        assert not ismetaclass(ClassWithMeta)
        
        assert ismetaclass(MetaClass)
        assert isclasstype(MetaClass)
        assert not isclass(MetaClass)
        
        assert not isclass(Class())
        assert not ismetaclass(Class())
        assert not isclasstype(Class())
        
        # Check the results of “metaclass(…)”:
        assert metaclass(Class) is type
        assert metaclass(MetaClass) is MetaClass
        assert metaclass(ClassWithMeta) is MetaClass
        
        assert metaclass(Class()) is type
        assert metaclass(ClassWithMeta()) is MetaClass
        
        # Check the results of “typeof(…)”:
        assert typeof(Class) is Class
        assert typeof(MetaClass) is MetaClass
        assert typeof(ClassWithMeta) is ClassWithMeta
        
        assert typeof(Class()) is Class
        assert typeof(ClassWithMeta()) is ClassWithMeta
        assert typeof(object()) is object
        assert typeof([]) is list
        assert typeof({}) is dict
        assert typeof('') is str
    
    def test_attr_accessor(self):
        """ » Checking “attr(•) accessor from clu.predicates …” """
        from clu.predicates import attr, uncallable
        
        # plistlib on Python 2.x uses those ungainly `writePlistToString`
        # methods; on Python 3.x you have the more reasonable and expected
        # `dumps` and `loads` calls… thus, attr(…) will bridge the gap:
        import plistlib
        dump = attr(plistlib, 'dumps', 'writePlistToString')
        load = attr(plistlib, 'loads', 'readPlistFromString')
        assert dump is not None
        assert load is not None
        assert callable(dump)
        assert callable(load)
        
        # When attr(…) can't find an attribute matching any of the names
        # provided, you get None back:
        wat = attr(plistlib, 'yo_dogg', 'wtf_hax')
        assert wat is None
        assert uncallable(wat)
        
        # … Unless of course a “default” value was specified:
        jon_snow = object() # it’s a sentinel GET IT?!?
        hax = attr(plistlib, 'yo_dogg', 'wtf_hax', default=jon_snow)
        assert hax is jon_snow
        assert uncallable(hax)
