#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, os

boilerplate = '''
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# INSERT MODULE CODE HERE

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
'''.lstrip()

def boilerplate_command(function=print):
    """ Write out the boilerplate code for a CLU python module file """
    function(boilerplate)
    return os.EX_OK

if __name__ == '__main__':
    sys.exit(boilerplate_command())