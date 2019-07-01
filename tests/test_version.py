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
        version_info = VersionInfo(__version__)
        
        assert version_info  < VersionInfo("9.0.0")
        assert version_info == VersionInfo(version_info)
        assert version_info == VersionInfo(__version__)
        assert version_info == VersionInfo(PkgResourcesVersion(__version__))
        assert version_info == VersionInfo(str(PkgResourcesVersion(__version__)))
        assert version_info <= VersionInfo(__version__)
        assert version_info >= VersionInfo(__version__)
        assert version_info  > VersionInfo(b'0.0.1')
        assert version_info != VersionInfo(b'0.0.1')
        
        assert bool(version_info)
        assert not bool(VersionInfo('‽.‽.‽'))