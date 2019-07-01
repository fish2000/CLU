# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestMathematics(object):
    
    """ Run the tests for the clu.mathematics module. """
    
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
        
        assert isfunction(clamp)
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
