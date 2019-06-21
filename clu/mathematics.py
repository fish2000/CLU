# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy

def clamp(value, min=None, max=None):
    """ Clamp a value within the bounds of an unsigned 8-bit integer """
    min = min or clamp.info.min
    max = max or clamp.info.max
    return numpy.clip(value, a_min=min,
                             a_max=max)

# Specify the numpy type to use with `clamp(…)`:
clamp.type = numpy.uint8

# Supply the upper and lower bounds for the `clamp(…)` type:
clamp.info = numpy.iinfo(clamp.type)
