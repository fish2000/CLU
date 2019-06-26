# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest
import array, decimal, os

from clu.typology import (graceful_issubclass,
                          ispathtype, ispath, isvalidpath,
                          isnumber, isnumeric, isarray,
                          isstring, isbytes,
                          islambda,
                          isfunction)

from clu.predicates import attr
from clu.typespace import SimpleNamespace

class TestPredicates(object):
    
    """ Run the tests for the clu.predicates and clu.typology modules. """
    
    def test_nops(self):
        """ » Checking “always/never/nuhuh/no_op” lambdas from clu.predicates … """
        from clu.predicates import always, never, nuhuh, no_op
        
        singles = (True, False, None)
        
        for single in singles:
            assert always(single) is True
            assert never(single) is False
            assert nuhuh(single) is None
            assert no_op(single, 'get') is single
    
    def test_ismergeable(self):
        """ » Checking “ismergeable” lambda from clu.predicates … """
        from clu.predicates import ismergeable
        from clu.typespace import Namespace
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
    
    def test_hasattr_shortcuts(self):
        """ » Checking “hasattr/haspyattr” shortcuts from clu.predicates … """
        from clu.predicates import (haspyattr, anyattrs, allattrs,
                                               anypyattrs, allpyattrs)
        assert not hasattr(object, 'base')
        assert not hasattr(object, 'class')
        assert hasattr(object, 'mro')
        
        assert haspyattr(object, 'base')
        assert haspyattr(object, 'class')
        assert haspyattr(object, 'mro')
        assert not haspyattr(object, 'yo')
        assert not haspyattr(object, 'dogg')
        assert not haspyattr(object, 'wtf')
        
        assert anyattrs(object, 'base', 'class', 'mro')
        assert not allattrs(object, 'base', 'class', 'mro')
        assert not anyattrs(object, 'yo', 'dogg', 'i', 'have', 'not', 'heard')
        assert allattrs(object, '__base__', '__class__', '__mro__')
        
        assert anypyattrs(object, 'yo', 'dogg', 'mro')
        assert not allpyattrs(object, 'yo', 'dogg', 'mro')
        assert not anypyattrs(object, 'yo', 'dogg', 'wtf')
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
        assert not islambda(graceful_issubclass)
        assert isfunction(lambda: None)
        assert isfunction(attr)
        # assert isfunction(export)
        assert isfunction(graceful_issubclass)
        assert not isfunction(SimpleNamespace())
        assert isfunction(SimpleNamespace) # classes are callable!
    
    def test_numpy_predicates(self):
        numpy = pytest.importorskip('numpy')
        assert isarray(numpy.ndarray)
        assert isarray(numpy.array([0, 1, 2]))
