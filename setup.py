#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    
#    CLU -- Common Lightweight Utilities
#    
#    Copyright © 2012-2035 Alexander Böhn
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
''' CLU - Common Lightweight Utilities '''

from __future__ import print_function
from setuptools import setup, find_packages

import sys, os, io
import sysconfig

# CONSTANTS
PROJECT_NAME = 'clu'
AUTHOR_NAME = 'Alexander Böhn'
AUTHOR_USER = 'fish2000'

GITHUB = 'github.com'
GMAIL = 'gmail.com'

AUTHOR_EMAIL = f'{AUTHOR_USER}@{GMAIL}'
PROJECT_GH_URL = f'https://{GITHUB}/{AUTHOR_USER}/{PROJECT_NAME}'
PROJECT_DL_URL = f'{PROJECT_GH_URL}/zipball/master'

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
                             'clu-ansidocs = clu.repl.cli.ansidocs:ansidocs_command',
                          'clu-boilerplate = clu.repl.cli.boilerplate:boilerplate_command',
                           'clu-boilercopy = clu.repl.cli.boilerplate:boilerplate_copy_command'],
    'pytest11'         : [    'clu-testing = clu.testing.pytest']
}

def project_content(*filenames):
    filepath = os.path.join(CWD, *filenames)
    if not os.path.isfile(filepath):
        raise IOError(f"File {filepath} doesn't exist")
    out = ''
    with io.open(filepath, 'r') as handle:
        out += handle.read()
    if not out:
        raise ValueError(f"File {filepath} couldn't be read")
    return out.strip()

# PROJECT VERSION & METADATA
__version__ = "<undefined>"
try:
    exec(compile(
        open(os.path.join(BASE_PATH,
            '__version__.py')).read(),
            '__version__.py', 'exec'))
except:
    __version__ = '0.12.15'

# PROJECT DESCRIPTION
LONG_DESCRIPTION = project_content('ABOUT.md')

# SOFTWARE LICENSE
LICENSE = 'MIT'

# REQUIRED INSTALLATION DEPENDENCIES
INSTALL_REQUIRES = project_content('requirements', 'install.txt').splitlines()

# PYPI PROJECT CLASSIFIERS
CLASSIFIERS = project_content('CLASSIFIERS.txt').splitlines()

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
    platforms=['any'],
    classifiers=CLASSIFIERS,
    
    packages=[package for package in find_packages() \
                       if package.startswith(PROJECT_NAME)],
    
    package_dir={ 'clu' : 'clu' },
    package_data={ '' : ['*.*'] },
    include_package_data=True,
    zip_safe=True,
    
    entry_points=ENTRY_POINTS,
    include_dirs=include_dirs
)
