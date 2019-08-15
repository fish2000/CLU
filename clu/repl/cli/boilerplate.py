#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

def boilerplate_command():
    """ Write out the boilerplate code for a CLU python module file """
    print('''
# -*- coding: utf-8 -*-
from __future__ import print_function
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# INSERT MODULE CODE HERE

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()'''.lstrip())
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(boilerplate_command())