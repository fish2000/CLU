# -*- coding: utf-8 -*-
from __future__ import print_function

class TestVersion(object):
    
    """ Run the tests for the clu.version module. """
    
    def test_print_version(self, cluversion):
        from clu.predicates import anyof
        from clu.repl.cli.print_version import version_string
        
        version = cluversion.to_string()
        
        vstring = version_string()
        assert vstring.startswith(f'{version}')
        
        snapshot = 'SNAPSHOT' in vstring
        release = 'release' in vstring
        assert anyof(snapshot, release)
    
    def test_git_version_function(self, cluversion):
        from clu.version.git_version import git_version_tags
        from clu.fs.filesystem import td
        
        version = cluversion.to_string()
        
        vtags0 = git_version_tags()
        assert vtags0 is not None
        assert vtags0.startswith(f'v{version}')
        
        vtags1 = git_version_tags(directory=td())
        assert vtags1 is None
    
    def test_are_we_gitted_function(self):
        from clu.version.git_version import are_we_gitted
        from clu.fs.filesystem import td
        
        assert are_we_gitted()
        assert not are_we_gitted(directory=td())
     
    def test_cluversion_and_VersionInfo(self, consts, cluversion):
        from clu.version import VersionInfo, read_version_file
        from pkg_resources.extern.packaging.version import Version as PkgResourcesVersion
        
        __version__ = read_version_file(consts.PROJECT_PATH)
        version_info = VersionInfo(__version__)
        
        assert cluversion  < VersionInfo("9.0.0")
        assert cluversion == VersionInfo(version_info)
        assert cluversion == VersionInfo(__version__)
        assert cluversion == VersionInfo(PkgResourcesVersion(__version__))
        assert cluversion == VersionInfo(str(PkgResourcesVersion(__version__)))
        assert cluversion <= VersionInfo(__version__)
        assert cluversion >= VersionInfo(__version__)
        assert cluversion  > VersionInfo(b'0.0.1')
        assert cluversion != VersionInfo(b'0.0.1')
        
        assert bool(cluversion)
        assert not bool(VersionInfo('‽.‽.‽'))
    
    def test_VersionInfo(self, consts):
        from clu.version import VersionInfo, read_version_file
        from pkg_resources.extern.packaging.version import Version as PkgResourcesVersion
        
        __version__ = read_version_file(consts.PROJECT_PATH)
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