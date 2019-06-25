# -*- coding: utf-8 -*-
from __future__ import print_function
from pkg_resources.extern.packaging.version import Version as PkgResourcesVersion

import os

from clu.version import VersionInfo, read_version_file

BASEPATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clu')
__version__ = read_version_file(BASEPATH)

class TestVersionInfo(object):
    
    """ Run the tests for the clu.version module. """
    
    def test_VersionInfo(self):
        version = VersionInfo(__version__)
        
        assert version  < VersionInfo("9.0.0")
        assert version == VersionInfo(version)
        assert version == VersionInfo(__version__)
        assert version == VersionInfo(PkgResourcesVersion(__version__))
        assert version == VersionInfo(str(PkgResourcesVersion(__version__)))
        assert version <= VersionInfo(__version__)
        assert version >= VersionInfo(__version__)
        assert version  > VersionInfo(b'0.0.1')
        assert version != VersionInfo(b'0.0.1')
        
        assert bool(version)
        assert not bool(VersionInfo('‽.‽.‽'))