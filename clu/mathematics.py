# -*- coding: utf-8 -*-
from __future__ import print_function

MOCK_NUMPY = False

from clu.constants.polyfills import numpy, reduce # type: ignore
from clu.naming import moduleof
from clu.predicates import isclasstype
from clu.typology import isxlist
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

if numpy is None:
    from mock import Mock
    numpy = Mock()
    MOCK_NUMPY = True

# JUST LIKE THE GREEKS
σ = sum
Σ = reduce

# Some numpy types are found in subpackages, like e.g. `numpy.ma.core.MaskedArray`;
# … this predicate function cuts through that nonsense by only looking at the 
# start of the deduced module string:
isnumpything = lambda thing: moduleof(thing).casefold().startswith('numpy')
isnumpytype = lambda cls: isclasstype(cls) and isnumpything(cls)

isnumpythinglist = lambda thinglist: isxlist(isnumpything, thinglist)
isnumpytypelist = lambda thinglist: isxlist(isnumpytype, thinglist)

@export
def isdtype(thing):
    """ isdtype(thing) → boolean predicate, True if thing is a non-object numpy dtype """
    try:
        dt = numpy.dtype(thing)
    except TypeError:
        return False
    return dt != numpy.object_

@export
class Clamper(object):
    
    """ A callable object representing a per-dtype clamp function """
    
    __slots__ = ('type', 'info')
    
    def __init__(self, dtype):
        """ Initialize a Clamper callable with a numpy dtype """
        if not isdtype(dtype):
            raise TypeError("Valid dtype required to initialize a Clamper")
        self.type = dtype
        self.info = numpy.iinfo(dtype)
    
    @property
    def bits(self):
        """ A human-readable string showing the bitlength of the dtype """
        return f"{self.info.bits!s}-bit"
    
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
        return f"Clamp a value within the bounds of an {self.bits} {self.kind}"
    
    def __call__(self, value, a_min=None, a_max=None):
        """ Clamp a value within the bounds of the initializing dtype """
        a_min = a_min or self.info.min
        a_max = a_max or self.info.max
        return numpy.clip(value, a_min=a_min,
                                 a_max=a_max)

clamp = Clamper(dtype=numpy.uint8)

if MOCK_NUMPY is not True:
    
    export(σ,                   name='σ')
    export(Σ,                   name='Σ')
    
    export(isnumpything,        name='isnumpything',        doc="isnumpything(thing) → boolean predicate, True if thing’s qualified module name starts with “numpy”")
    export(isnumpytype,         name='isnumpytype',         doc="isnumpytype(cls) → boolean predicate, True if thing is from the “numpy” module and is a classtype")
    
    export(isnumpythinglist,    name='isnumpythinglist',    doc="isnumpythinglist(thinglist) → boolean predicate, True if `thinglist` is a sequence of things from the “numpy” module")
    export(isnumpytypelist,     name='isnumpytypelist',     doc="isnumpytypelist(thinglist) → boolean predicate, True if `thinglist` is a sequence of types from the “numpy” module")
    
    export(clamp,               name='clamp')
    
    __all__, __dir__ = exporter.all_and_dir()
    
