# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import pytest

tmps = ('/tmp',
        '/private/tmp',
        '/var/tmp',
        '/private/var/tmp',
        os.environ.get('TMPDIR'))

class TestFsMisc(object):
    
    """ Run the tests for the “clu.fs.abc” module. """
    
    def test_TypeLocker(self):
        from clu.fs.abc import TypeLocker, BaseFSName, TemporaryFileWrapper
        from clu.fs.filesystem import Directory
        
        assert 'Directory' in TypeLocker.types
        assert TypeLocker.types['Directory'] is Directory
        
        assert BaseFSName in TypeLocker.types.values()
        assert Directory in TypeLocker.types.values()
        assert TemporaryFileWrapper in TypeLocker.types.values()
    
    @pytest.mark.parametrize('tmp', filter(os.path.exists, tmps))
    def test_BaseFSName_concrete_subclass(self, consts,
                                                temporarydir,
                                                tmp):
        from clu.fs.abc import BaseFSName
        from clu.fs.filesystem import Directory
        
        class TmpFSName(BaseFSName):
            
            """ A trivial “clu.fs.abc.BaseFSName” subclass """
            
            @property
            def name(self):
                return tmp
        
        tname = TmpFSName()
        assert tname
        
        # Check all of the BaseFSName properties:
        assert tname.exists
        assert tname.basename == os.path.basename(tmp)
        assert tname.dirname == Directory(os.path.abspath(
                                          os.path.dirname(tmp)))
        
        # Check all of the BaseFSName methods:
        assert tname.split() == (Directory(os.path.abspath(
                                          os.path.dirname(tmp))),
                                          os.path.basename(tmp))
        assert tname.realpath() == os.path.realpath(tmp)
        assert tname.parent() == Directory(os.path.abspath(
                                           os.path.dirname(tmp)))
        assert tname.relparent(consts.BASEPATH) == os.path.relpath(consts.BASEPATH,
                                             start=os.path.abspath(
                                                   os.path.dirname(tmp)))
        assert tname.relprefix(consts.BASEPATH) == (os.path.relpath(consts.BASEPATH,
                                              start=os.path.abspath(
                                                    os.path.dirname(tmp))) + os.sep).replace(os.sep,
                                                                                             consts.ENVIRONS_SEP)
        
        # Attempt to forge a symlink from inside the temporarydir
        # to that which is pointed at by “tname”:
        symlink = temporarydir.subpath(os.path.split(tmp)[-1])
        
        # … but bail if the subpath isn’t really a subpath:
        try:
            os.path.samefile(symlink, tmp)
        except FileNotFoundError:
            tname.symlink(symlink)
            assert os.path.exists(symlink)
            assert os.path.islink(symlink)
        
        # Always returns True:
        assert tname.close()
        
        # Inspect the stringified form:
        tnstring = tname.to_string()
        assert "exists=«True»" in tnstring
        assert f"name=“{tmp}”" in tnstring
        assert "exists=«True»" in repr(tname)
        assert f"name=“{tmp}”" in repr(tname)
        
        # Boolean value is True if it exists:
        assert bool(tname)
        
        # equal and unequal:
        assert tname == TmpFSName()
        assert tname != consts.BASEPATH