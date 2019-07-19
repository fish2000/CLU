# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestMathematics(object):
    
    """ Run the tests for the clu.mathematics module. """
    
    def test_numpy_type_member_predicate(self):
        numpy = pytest.importorskip('numpy')
        from clu.mathematics import isnumpytype
        from clu.predicates import negate
        from clu.typology import array_types
        from itertools import dropwhile
        
        # Chop off the numpy end of “array_types”:
        numpies = tuple(dropwhile(negate(isnumpytype),
                                         array_types))
        
        # Confirm it’s got our types:
        assert len(numpies) == 3
        assert numpy.ndarray in numpies
        assert numpy.matrix in numpies
        assert numpy.ma.core.MaskedArray in numpies
    
    def test_sigma_lowercase_sum_alias(self):
        from clu.mathematics import σ           # same as “sum”
        
        # As simple as these things get:
        assert sum(range(10), 666) == 711
        assert σ(range(10), 666) == 711
    
    def test_sigma_uppercase_reduce_alias(self):
        numpy = pytest.importorskip('numpy')
        from clu.mathematics import Σ           # same as “reduce”
        from clu.predicates import apply_to     # functional helper
        from clu.naming import nameof           # predicate function
        from clu.typology import (array_types,  # data on which to operate
                                numeric_types)
        
        # Double-check numpy:
        assert hasattr(numpy, 'ndarray')
        assert getattr(numpy, 'ndarray') in array_types
        
        # Compose a function to select the longest typename,
        # given an arbitrary typelist:
        reduce_function = lambda a, b: (len(a) > len(b)) and a or b
        sigma_function = lambda total: Σ(reduce_function, total, '')
        longest_typename = apply_to(nameof, sigma_function)
        
        # Affirm that we know what we’re doing:
        assert longest_typename(*numeric_types) == 'Decimal'
        assert longest_typename(*array_types) == 'MaskedArray'
    
    def test_isdtype_predicate(self):
        numpy = pytest.importorskip('numpy')
        from clu.mathematics import isdtype
        
        assert isdtype(numpy.uint8)
        assert isdtype(int)
        assert isdtype(float)
        assert isdtype(complex)
        assert isdtype(numpy.float32)
        assert isdtype(numpy.float64)
        assert isdtype(numpy.floating)
        assert isdtype(numpy.double)
        assert not isdtype(numpy.array)
        
        assert isdtype('u8')
        assert isdtype('|u8')
        assert isdtype('>u8')
        assert isdtype('<u8')
        assert not isdtype('@u8')
        
        assert isdtype('uint8')
        assert isdtype('uint16')
        assert isdtype('uint32')
        assert isdtype('uint64')
        assert not isdtype('uint128')
        
        class ObjectType(object):
            pass
        
        # Passing ObjectType to numpy.dtype(…) would return
        # a dtype object matching typecode 'O' – but for our
        # `isdtype(…)` predicate, we don’t allow for that:
        assert not isdtype(ObjectType)
        assert not isdtype(ObjectType())
    
    def test_uint8_clamp_basics(self):
        numpy = pytest.importorskip('numpy')
        from clu.mathematics import clamp
        from clu.predicates import uncallable, isslotted, isdictish, isslotdicty
        from clu.typology import isfunction, islambda
        
        assert clamp.bits == '8-bit'
        assert clamp.kind == 'unsigned integer'
        assert clamp.type is numpy.uint8
        
        # You evidently can’t directly eq-compare “iinfo” instances,
        # sooooo…
        assert clamp.info.min == numpy.iinfo(numpy.uint8).min
        assert clamp.info.max == numpy.iinfo(numpy.uint8).max
        assert clamp.info.dtype == numpy.iinfo(numpy.uint8).dtype
        assert clamp.info.key == numpy.iinfo(numpy.uint8).key
        assert clamp.info.kind == numpy.iinfo(numpy.uint8).kind
        
        assert not uncallable(clamp)
        assert isslotted(clamp)
        assert not isdictish(clamp)
        assert not isslotdicty(clamp)
        
        assert not isfunction(clamp)
        assert not islambda(clamp)
    
    def test_uint8_clamp_functionality(self):
        numpy = pytest.importorskip('numpy')
        from clu.mathematics import clamp
        
        a = numpy.array([0, -2, 100, 256, 500])
        u = 257
        s = -200
        
        assert (clamp(a) == numpy.array([0, 0, 100, 255, 255])).all()
        assert all(clamp(a) == numpy.array([0, 0, 100, 255, 255]))
        assert clamp(u) == 255
        assert clamp(s) == 0
