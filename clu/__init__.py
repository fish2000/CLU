#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    
#    CLU -- Common Lightweight Utilities
#    
#    Copyright © 2012-2025 Alexander Böhn
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy 
#    of this software and associated documentation files (the "Software"), to deal 
#    in the Software without restriction, including without limitation the rights 
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
#    copies of the Software, and to permit persons to whom the Software is 
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in all 
#    copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#    SOFTWARE.
#
from __future__ import print_function
from pkgutil import extend_path
from os.path import dirname

from clu.version.read_version import read_version_file
from clu.version import VersionInfo

# Module exports:
__all__ = ('__version__', 'version_info',
           '__title__', '__author__', '__maintainer__',
           '__license__', '__copyright__') # type: ignore

__dir__ = lambda: list(__all__)

if '__path__' in locals():
    __path__ = extend_path(__path__, __name__) # type: ignore
    __all__ += ('__path__',) # type: ignore

# Embedded project metadata:
__version__ = read_version_file(dirname(__file__))
__title__ = 'clu'
__author__ = 'Alexander Böhn'
__maintainer__ = __author__
__license__ = 'MIT'
__copyright__ = f'{__title__} © 2012-2025 {__author__}'

# The CLU project version:
version_info = VersionInfo(__version__)
