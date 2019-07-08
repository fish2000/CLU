# -*- coding: utf-8 -*-
from __future__ import print_function

MOCK_NUMPY = False
from clu.constants import numpy
from clu.exporting import Exporter

exporter = Exporter()
export = exporter.decorator()

if numpy is None:
    from mock import Mock
    numpy = Mock()
    MOCK_NUMPY = True

@export
def isdtype(thing):
    """ isdtype(thing) → boolean predicate, True if thing is a non-object NumPy dtype """
    try:
        dt = numpy.dtype(thing)
    except TypeError:
        return False
    return dt != numpy.object_

@export
class Clamper(object):
    __slots__ = ('type', 'info')
    
    """ A callable object representing a per-dtype clamp function """
    
    def __init__(self, dtype):
        """ Initialize a Clamper callable with a NumPy dtype """
        if not isdtype(dtype):
            raise TypeError("Valid dtype required to initialize a Clamper")
        self.type = dtype
        self.info = numpy.iinfo(dtype)
    
    @property
    def bits(self):
        """ A human-readable string showing the bitlength of the dtype """
        return "%i-bit" % self.info.bits
    
    @property
    def kind(self):
        """ A human-readable string describing the “kind” of the dtype """
        if self.info.kind == 'u':
            return 'unsigned integer'
        elif self.info.kind == 'i':
            return 'signed integer'
        elif self.info.kind == 'f':
            return 'float'
        elif self.info.kind == 'd':
            return 'double'
        return 'number'
    
    @property
    def description(self):
        return "Clamp a value within the bounds of an %s %s" % (self.bits, self.kind)
    
    def __call__(self, value, a_min=None, a_max=None):
        """ Clamp a valiue within the bounds of the initializing dtype """
        a_min = a_min or self.info.min
        a_max = a_max or self.info.max
        return numpy.clip(value, a_min=a_min,
                                 a_max=a_max)

clamp = Clamper(dtype=numpy.uint8)

if MOCK_NUMPY is not True:
    export(clamp, name='clamp')
    __all__, __dir__ = exporter.all_and_dir()