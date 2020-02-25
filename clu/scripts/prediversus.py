# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

from clu.naming import nameof
from clu.repr import strfield
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

predicate_test      = lambda predicate, argument: (          predicate,          argument,              predicate(argument))
predicate_test_repr = lambda predicate, argument: (f"{nameof(predicate)}({nameof(argument)})", strfield(predicate(argument)))

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_one():
        pass # INSERT TESTING CODE HERE, pt. I
    
    #@inline
    def test_two():
        pass # INSERT TESTING CODE HERE, pt. II
    
    #@inline.diagnostic
    def show_me_some_values():
        pass # INSERT DIAGNOSTIC CODE HERE
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())

