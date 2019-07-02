# -*- coding: utf-8 -*-
from __future__ import print_function
from tempfile import gettempdir

import collections.abc
import contextlib
import os

from clu.fs import Directory

class TestFsFilesystem(object):
    
    """ Run the tests for the clu.fs.filesystem module. """
    
    def test_TemporaryName(self):
        """ Tests for clu.fs.filesystem.TemporaryName """
        from clu.fs import TemporaryName
        initial = os.getcwd()
        tfp = None
        
        with TemporaryName(prefix="test-temporaryname-",
                           randomized=True) as tfn:
            print("* Testing TemporaryName file instance: %s" % tfn.name)
            assert os.path.samefile(os.getcwd(),            initial)
            assert gettempdir() in tfn.name
            assert tfn.prefix == "test-temporaryname-"
            assert tfn.suffix == ".tmp"
            assert not tfn._parent
            assert tfn.prefix in tfn.name
            assert tfn.suffix in tfn.name
            assert tfn.prefix in os.fspath(tfn)
            assert tfn.suffix in os.fspath(tfn)
            assert tfn.destroy
            assert type(tfn.directory(os.path.basename(tfn.name))) == Directory
            assert isinstance(tfn,                          TemporaryName)
            assert isinstance(tfn,                          collections.abc.Hashable)
            assert isinstance(tfn,                          contextlib.AbstractContextManager)
            assert isinstance(tfn,                          os.PathLike)
            p = tfn.parent()
            assert os.path.samefile(os.fspath(p),           gettempdir())
            # The next four asserts will be “not” asserts while
            # the TemporaryName has not been written to:
            assert not tfn.exists
            assert not os.path.isfile(os.fspath(tfn))
            assert not tfn.basename in tfn.dirname
            assert not tfn.basename in p
            # Here we write something to the TemporaryName:
            with open(os.fspath(tfn), mode="w") as handle:
                handle.write("yo dogg")
            # Now we repeat the above four asserts,
            # as positive assertions:
            assert tfn.exists
            assert os.path.isfile(os.fspath(tfn))
            assert tfn.basename in tfn.dirname
            assert tfn.basename in p
            # Stash the TemporaryName’s path to later assert
            # that it no longer exists - that it has been correctly
            # deleted on scope exit:
            tfp = tfn.name
            assert os.path.exists(tfp)
            
        # Confirm that the TemporaryName has been deleted:
        assert not os.path.exists(tfp)
    
    def test_wd(self):
        """ Tests for clu.fs.filesystem.wd """
        from clu.fs import wd
        initial = os.getcwd()
        
        with wd() as cwd:
            print("* Testing working-directory instance: %s" % cwd.name)
            assert os.path.samefile(os.getcwd(),           cwd.new)
            assert os.path.samefile(os.getcwd(),           cwd.old)
            assert os.path.samefile(os.getcwd(),           os.fspath(cwd))
            assert os.path.samefile(cwd.new,               cwd.old)
            assert os.path.samefile(cwd.new,               initial)
            assert os.path.samefile(cwd.old,               initial)
            assert os.path.samefile(cwd.new,               os.fspath(cwd))
            assert os.path.samefile(cwd.old,               os.fspath(cwd))
            assert os.path.samefile(os.fspath(cwd),        initial)
            assert not cwd.subdirectory('yodogg').exists
            assert not cwd.will_change
            assert not cwd.did_change
            assert not cwd.will_change_back
            assert not cwd.did_change_back
            assert type(cwd.directory(cwd.new)) == Directory
            assert isinstance(cwd,                         wd)
            assert isinstance(cwd,                         Directory)
            assert isinstance(cwd,                         collections.abc.Hashable)
            assert isinstance(cwd,                         collections.abc.Mapping)
            assert isinstance(cwd,                         collections.abc.Sized)
            assert isinstance(cwd,                         contextlib.AbstractContextManager)
            assert isinstance(cwd,                         os.PathLike)
            assert os.path.isdir(os.fspath(cwd))
            assert not 'yodogg' in cwd
            assert cwd.basename in cwd.dirname
    
    def test_cd(self):
        """ Tests for clu.fs.filesystem.cd """
        from clu.fs import cd
        initial = os.getcwd()
        
        with cd(gettempdir()) as tmp:
            print("* Testing directory-change instance: %s" % tmp.name)
            assert os.path.samefile(os.getcwd(),          gettempdir())
            assert os.path.samefile(os.getcwd(),          tmp.new)
            assert os.path.samefile(gettempdir(),         tmp.new)
            assert os.path.samefile(os.getcwd(),          os.fspath(tmp))
            assert os.path.samefile(gettempdir(),         os.fspath(tmp))
            assert not os.path.samefile(os.getcwd(),      initial)
            assert not os.path.samefile(tmp.new,          initial)
            assert not os.path.samefile(os.fspath(tmp),   initial)
            assert os.path.samefile(tmp.old,              initial)
            assert tmp.will_change
            assert tmp.did_change
            assert tmp.will_change_back
            assert not tmp.did_change_back
            assert type(tmp.directory(tmp.new)) == Directory
            assert isinstance(tmp,                        cd)
            assert isinstance(tmp,                        Directory)
            assert isinstance(tmp,                        collections.abc.Hashable)
            assert isinstance(tmp,                        collections.abc.Mapping)
            assert isinstance(tmp,                        collections.abc.Sized)
            assert isinstance(tmp,                        contextlib.AbstractContextManager)
            assert isinstance(tmp,                        os.PathLike)
            assert os.path.isdir(os.fspath(tmp))
            assert tmp.basename in tmp.dirname
    
    def test_TemporaryDirectory(self):
        """ Tests for clu.fs.filesystem.TemporaryDirectory """
        from clu.fs import TemporaryDirectory
        initial = os.getcwd()
        tdp = None
        
        with TemporaryDirectory(prefix="test-temporarydirectory-") as ttd:
            print("* Testing TemporaryDirectory instance: %s" % ttd.name)
            assert gettempdir() in ttd.name
            assert gettempdir() in ttd.new
            assert gettempdir() in os.fspath(ttd)
            assert initial not in ttd.name
            assert initial not in ttd.new
            assert initial not in os.fspath(ttd)
            assert initial in ttd.old
            assert not ttd.subdirectory('yodogg').exists
            assert ttd.subdirectory('yodogg').makedirs().exists
            assert 'yodogg' in ttd
            assert ttd.prefix == "test-temporarydirectory-"
            assert not ttd.suffix
            assert not ttd._parent
            assert ttd.prefix in ttd.name
            assert ttd.exists
            assert ttd.destroy
            assert ttd.will_change
            assert ttd.did_change
            assert ttd.will_change_back
            assert not ttd.did_change_back
            assert type(ttd.directory(ttd.new)) == Directory
            assert isinstance(ttd,                          TemporaryDirectory)
            assert isinstance(ttd,                          Directory)
            assert isinstance(ttd,                          collections.abc.Hashable)
            assert isinstance(ttd,                          collections.abc.Mapping)
            assert isinstance(ttd,                          collections.abc.Sized)
            assert isinstance(ttd,                          contextlib.AbstractContextManager)
            assert isinstance(ttd,                          os.PathLike)
            p = ttd.parent()
            assert os.path.samefile(os.fspath(p),           gettempdir())
            assert os.path.isdir(os.fspath(ttd))
            assert os.path.isdir(os.fspath(p))
            assert ttd.basename in p
            assert ttd.basename in ttd.dirname
            assert ttd.dirname == p
            # Stash the TemporaryDirectory’s path as a Directory
            # instance, to later assert that it no longer exists –
            # that it has been correctly deleted on scope exit:
            tdp = Directory(ttd)
            assert tdp.exists
        
        # Confirm that the TemporaryDirectory has been deleted:
        assert not tdp.exists

