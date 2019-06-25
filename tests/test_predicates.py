# -*- coding: utf-8 -*-
from __future__ import print_function

import array, decimal, numpy, os

from clu.typology import (graceful_issubclass,
                          ispathtype, ispath, isvalidpath,
                          isnumber, isnumeric, isarray,
                          isstring, isbytes,
                          # islambda,
                          isfunction)

from clu.predicates import attr
from clu.typespace import SimpleNamespace

class TestPredicates(object):
    
    """ Run the tests for the clu.predicates and clu.typology modules. """
    
    def test_attr_accessor(self):
        """ » Checking “attr(•) accessor from clu.predicates …” """
        # print(test_attr_accessor.__doc__)
        # print()
        
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
        # print(test_boolean_predicates.__doc__)
        # print()
        
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
        if numpy is not None:
            assert isarray(numpy.ndarray)
            assert isarray(numpy.array([0, 1, 2]))
        assert isstring(str)
        assert isstring("")
        assert isbytes(bytes)
        assert isbytes(bytearray)
        assert isbytes(b"")
        
        # assert islambda(lambda: None)
        # assert islambda(attr)
        # assert not islambda(export)
        assert isfunction(lambda: None)
        assert isfunction(attr)
        # assert isfunction(export)
        assert not isfunction(SimpleNamespace())
        assert isfunction(SimpleNamespace) # classes are callable!
