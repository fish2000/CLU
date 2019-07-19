# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestTypology(object):
    
    """ Run the tests for the clu.typology module. """
    
    def test_lambda_double_uppercase_lambda_double_lowercase_lambda_and_isfunction(self):
        from clu.typology import ΛΛ, λλ, iscallable
        
        def function_def(*args, **kwargs):
            return "Yo dogg"
        
        function_lambda = lambda *args, **kwargs: "Yo dogg"
        
        class function_class(object):
            
            def __call__(self, *args, **kwargs):
                return "Yo dogg"
        
        function_object = function_class()
        
        assert ΛΛ(function_def)
        assert ΛΛ(function_lambda)
        assert not ΛΛ(function_class)
        assert not ΛΛ(function_object)
        
        assert not λλ(function_def)
        assert λλ(function_lambda)
        assert not λλ(function_class)
        assert not λλ(function_object)
        
        assert not iscallable(function_def)
        assert not iscallable(function_lambda)
        assert iscallable(function_class)
        assert iscallable(function_object)
    
    def test_subclasscheck(self):
        from clu.typology import subclasscheck
        from abc import ABC
        
        assert subclasscheck(int, int)
        assert subclasscheck(666, int)
        
        class Int(int):
            pass
        
        assert subclasscheck(Int, int)
        assert not subclasscheck(int, Int)
        assert not subclasscheck(666, Int)
        
        class FunnyYouDontLookIntish(ABC):
            pass
        
        FunnyYouDontLookIntish.register(int)
        
        assert subclasscheck(int, FunnyYouDontLookIntish)
        assert subclasscheck(666, FunnyYouDontLookIntish)
        assert not subclasscheck(FunnyYouDontLookIntish, int)
    
    def test_boolean_predicates(self):
        """ » Checking basic isXXX(•) functions from clu.typology … """
        import array, decimal, os
        from clu.predicates import attr
        from clu.typespace import SimpleNamespace
        from clu.typology import (subclasscheck,
                                  ispathtype, ispath, isvalidpath,
                                  isnumber, isnumeric, isarray,
                                  isstring, isbytes,
                                  islambda,
                                  isfunction)
        
        if hasattr(os, 'PathLike'):
            assert ispathtype(os.PathLike)
        
        assert ispathtype(str)
        assert ispathtype(bytes)
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
        assert islambda(subclasscheck) # IT IS NOW DOGG
        
        assert isfunction(lambda: None)
        assert isfunction(attr)
        assert isfunction(subclasscheck)
        assert not isfunction(SimpleNamespace())
        assert not isfunction(SimpleNamespace)
    
    def test_numpy_predicates(self):
        from clu.typology import isarray
        numpy = pytest.importorskip('numpy')
        assert isarray(numpy.ndarray)
        assert isarray(numpy.array([0, 1, 2]))
