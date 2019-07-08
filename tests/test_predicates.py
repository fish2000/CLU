# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestPredicates(object):
    
    """ Run the tests for the clu.predicates module. """
    
    def test_utility_helper_functions(self):
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
        from clu.typespace import Namespace, SimpleNamespace
        from clu.predicates import (thing_has, class_has,
                                    isslotted, isdictish, isslotdicty)
        
        assert isslotted(Namespace())
        assert isslotted(SimpleNamespace())
        assert isdictish(Namespace())
        assert isdictish(SimpleNamespace())
        assert isslotdicty(Namespace())
        assert isslotdicty(SimpleNamespace())
        
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
    
    def test_applyto(self):
        """ » Checking “apply_to(…)” core function from clu.predicates … """
        from string import capwords
        from clu.predicates import apply_to, isclasstype
        from clu.constants import ENCODING, SINGLETON_TYPES
        from clu.typology import (numeric_types, string_types, bytes_types,
                                  callable_types, array_types, path_types)
        
        # Test apply_to(…) returning a partial --
        # N.B. this is the exact implementation of actual functions
        # in use in clu.typology:
        istypelist = apply_to(isclasstype, all)
        maketypelist = apply_to(lambda thing: isclasstype(thing) and thing or type(thing),
                                lambda total: tuple(frozenset(total)))
        
        assert istypelist(SINGLETON_TYPES)
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
        
        s = lambda by: str(by, encoding=ENCODING)
        r = "Yo Dogg I Heard You Love Apply_to"
        assert apply_to(lambda thing: isinstance(thing, string_types) and thing or s(thing),
                        lambda total: capwords(" ".join(total)),
                        "yo", "dogg", b"I", b"heard", "you", b"love", "apply_to") == r
    
    def test_applyto_predicate_logicals(self):
        """ » Checking “apply_to(…)” derived predicate logicals from clu.predicates … """
        from clu.predicates import (haslength, uncallable, isiterable, isslotted)
        from clu.predicates import (predicate_all, predicate_any,
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
        assert predicate_all(isiterable, rstr, byts, slot.yo, slot.dogg, slot.wtf)
        assert predicate_all(lambda thing: not uncallable(thing), Slotted, call, type)
        assert predicate_any(lambda thing: not uncallable(thing), Slotted, call, type, slot)
        
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
        from clu.constants import Enum, System, CSIDL
        
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
        from clu.constants import NoDefault
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
    
    def test_nops(self):
        """ » Checking “always/never/nuhuh/no_op” lambdas from clu.predicates … """
        from clu.predicates import (always, never, nuhuh,
                                    no_op, predicate_nop,
                                            function_nop)
        
        singles = (True, False, None)
        
        for single in singles:
            assert always(single) is True
            assert never(single) is False
            assert nuhuh(single) is None
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
            __iter__ = "wtf"
            __getitem__ = "hax"
            get = "IDK"
        
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
        """ » Checking “ismetaclass/isclass/isclasstype” from clu.predicates … """
        from clu.predicates import ismetaclass, isclass, isclasstype
        
        class Class(object):
            pass
        
        class MetaClass(type):
            pass
        
        assert isclass(Class)
        assert isclasstype(Class)
        assert not ismetaclass(Class)
        
        assert ismetaclass(MetaClass)
        assert isclasstype(MetaClass)
        assert not isclass(MetaClass)
        
        assert not isclass(Class())
        assert not ismetaclass(Class())
        assert not isclasstype(Class())
    
    def test_attr_accessor(self):
        """ » Checking “attr(•) accessor from clu.predicates …” """
        from clu.predicates import attr
        
        # plistlib on Python 2.x uses those ungainly `writePlistToString`
        # methods; on Python 3.x you have the more reasonable and expected
        # `dumps` and `loads` calls… thus, attr(…) will bridge the gap:
        import plistlib
        dump = attr(plistlib, 'dumps', 'writePlistToString')
        load = attr(plistlib, 'loads', 'readPlistFromString')
        assert dump is not None
        assert load is not None
        
        # When attr(…) can't find an attribute matching any of the names
        # provided, you get None back:
        wat = attr(plistlib, 'yo_dogg', 'wtf_hax')
        assert wat is None
    
    def test_boolean_predicates(self):
        """ » Checking basic isXXX(•) functions from clu.typology … """
        import array, decimal, os
        from clu.predicates import attr
        from clu.typespace import SimpleNamespace
        from clu.typology import (graceful_issubclass,
                                  ispathtype, ispath, isvalidpath,
                                  isnumber, isnumeric, isarray,
                                  isstring, isbytes,
                                  islambda,
                                  isfunction)
        
        assert graceful_issubclass(int, int)
        
        assert ispathtype(str)
        assert ispathtype(bytes)
        if hasattr(os, 'PathLike'):
            assert ispathtype(os.PathLike)
        assert not ispathtype(SimpleNamespace)
        assert ispath('/yo/dogg')
        assert not ispath(SimpleNamespace())
        assert not isvalidpath('/yo/dogg')
        assert isvalidpath('/')
        assert isvalidpath('/private/tmp')
        assert isvalidpath('~/')
        
        assert isnumber(int)
        assert isnumber(decimal.Decimal)
        assert isnumber(666)
        assert not isnumber(str)
        assert not isnumber("666")
        assert isnumeric(int)
        assert isnumeric(float)
        assert isnumeric(1)
        assert not isnumeric(bytes)
        assert not isnumeric("2001e50")
        
        assert isarray(array.array)
        assert isstring(str)
        assert isstring("")
        assert isbytes(bytes)
        assert isbytes(bytearray)
        assert isbytes(b"")
        
        assert islambda(lambda: None)
        assert islambda(attr)
        # assert not islambda(export)
        assert islambda(graceful_issubclass) # IT IS NOW DOGG
        assert isfunction(lambda: None)
        assert isfunction(attr)
        # assert isfunction(export)
        assert isfunction(graceful_issubclass)
        assert not isfunction(SimpleNamespace())
        assert isfunction(SimpleNamespace) # classes are callable!
    
    def test_numpy_predicates(self):
        from clu.typology import isarray
        numpy = pytest.importorskip('numpy')
        assert isarray(numpy.ndarray)
        assert isarray(numpy.array([0, 1, 2]))
