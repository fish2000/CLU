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
''' CLU - Common Lightweight Utilities, or Command-Line Utilities (your pick) '''

from __future__ import print_function
from setuptools import setup, find_packages

import os
import sys
import sysconfig

# HOST PYTHON VERSION
PYTHON_VERSION = float("%s%s%s" % (sys.version_info.major, os.extsep,
                                   sys.version_info.minor))

# CONSTANTS
PROJECT_NAME = 'clu'
AUTHOR_NAME = 'Alexander Böhn'
AUTHOR_USER = 'fish2000'

GITHUB = 'github.com'
GMAIL = 'gmail.com'

AUTHOR_EMAIL = '%s@%s' % (AUTHOR_USER, GMAIL)
PROJECT_GH_URL = 'https://%s/%s/%s' % (GITHUB,
                                       AUTHOR_USER,
                                       PROJECT_NAME)
PROJECT_DL_URL = '%s/zipball/master' % PROJECT_GH_URL

KEYWORDS = ('command',
            'utilities', PROJECT_NAME,
                         AUTHOR_USER,
            'command-line',
            'modules',
            'predicates',
            'REPL', 'tools')

# PROJECT DIRECTORY
CWD = os.path.dirname(__file__)
BASE_PATH = os.path.join(
            os.path.abspath(CWD), PROJECT_NAME)

# ENTRY POINTS
ENTRY_POINTS = {
    'console_scripts'  : [    'clu-version = clu.repl.cli.print_version:print_version_command',
                          'clu-boilerplate = clu.repl.cli.boilerplate:boilerplate_command',
                           'clu-boilercopy = clu.repl.cli.boilerplate:boilerplate_copy_command'],
    'pytest11'         : [    'clu-testing = clu.testing.pytest']
}

def project_content(*filenames):
    import io
    filepath = os.path.join(CWD, *filenames)
    if not os.path.isfile(filepath):
        raise IOError("""File %s doesn't exist""" % filepath)
    out = ''
    with io.open(filepath, 'r') as handle:
        out += handle.read()
    if not out:
        raise ValueError("""File %s couldn't be read""" % os.path.sep.join(filenames))
    return out.strip()

# PROJECT VERSION & METADATA
__version__ = "<undefined>"
try:
    exec(compile(
        open(os.path.join(BASE_PATH,
            '__version__.py')).read(),
            '__version__.py', 'exec'))
except:
    __version__ = '0.5.5'

# PROJECT DESCRIPTION
LONG_DESCRIPTION = project_content('ABOUT.md')

# SOFTWARE LICENSE
LICENSE = 'MIT'

# REQUIRED INSTALLATION DEPENDENCIES
INSTALL_REQUIRES = project_content('requirements', 'install.txt').splitlines()

# PYPI PROJECT CLASSIFIERS
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Framework :: Pytest',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'Topic :: Software Development :: Testing',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: OS Independent',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
]

# NUMPY: C-API INCLUDE DIRECTORY
try:
    import numpy
except ImportError:
    class FakeNumpy(object):
        def get_include(self):
            return os.path.curdir
    numpy = FakeNumpy()

# SOURCES & INCLUDE DIRECTORIES
include_dirs = [numpy.get_include(),
                sysconfig.get_path('include')]

# THE CALL TO `setup(…)`
setup(
    name="python-%s" % PROJECT_NAME,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    
    version=__version__,
    description=__doc__.strip(),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    
    keywords=" ".join(KEYWORDS),
    url=PROJECT_GH_URL, download_url=PROJECT_DL_URL,
    license=LICENSE, platforms=['any'],
    classifiers=CLASSIFIERS,
    
    packages=[package for package in find_packages() \
                       if package.startswith(PROJECT_NAME)],
    
    package_dir={ 'clu' : 'clu' },
    package_data={ '' : ['*.*'] },
    include_package_data=True,
    zip_safe=True,
    
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIRES,
    include_dirs=include_dirs
)
