# -*- coding: utf-8 -*-
from __future__ import print_function
from tempfile import gettempdir, NamedTemporaryFile

import collections.abc
import contextlib
import os
import pytest

from clu.fs import Directory

class TestFsFilesystem(object):
    
    """ Run the tests for the clu.fs.filesystem module. """
    
    def test_script_path(self):
        from clu.fs.filesystem import script_path
        
        scripts = Directory(script_path())
        assert scripts.exists
        assert '.gitignore' in scripts
        assert '__init__.py' in scripts # it’s a Python module directory
    
    def test_temporary(self):
        from clu.fs.filesystem import temporary, write_to_path
        from clu.fs.filesystem import FilesystemError
        
        # Prepare the temporary directory:
        d = Directory(gettempdir())
        assert d.exists
        
        # These automatically randomize:
        assert temporary(dir=d).startswith(gettempdir())
        assert temporary(parent=d).startswith(gettempdir())
        
        # These are deterministic:
        prefix = os.path.join(gettempdir(), 'yo-dogg')
        assert temporary(prefix='yo-dogg', dir=d) == prefix
        assert temporary(prefix='yo-dogg', parent=d) == prefix
        
        # These are deterministic (see below):
        prefix_suffix = os.path.join(gettempdir(), 'yo-dogg.tmp')
        assert temporary(prefix='yo-dogg', suffix='tmp', dir=d) == prefix_suffix
        assert temporary(prefix='yo-dogg', suffix='tmp', parent=d) == prefix_suffix
        assert temporary(prefix='yo-dogg', suffix='.tmp', dir=d) == prefix_suffix
        assert temporary(prefix='yo-dogg', suffix='.tmp', parent=d) == prefix_suffix
        
        # These are manually randomized:
        starts = os.path.join(gettempdir(), 'yo-dogg-')
        ends = '.tmp'
        
        assert temporary(prefix='yo-dogg-',
                         suffix='tmp',
                         randomized=True,
                         dir=d).startswith(starts)
        assert temporary(prefix='yo-dogg-',
                         suffix='tmp',
                         randomized=True,
                         parent=d).startswith(starts)
        
        assert temporary(prefix='yo-dogg-',
                         suffix='tmp',
                         randomized=True,
                         dir=d).endswith(ends)
        assert temporary(prefix='yo-dogg-',
                         suffix='tmp',
                         randomized=True,
                         parent=d).endswith(ends)
        
        # Prepare the subpath
        p = d.subpath('yo-dogg.tmp')
        assert not os.path.exists(p)
        
        # Prepare data:
        data = "yo dogg, " * 1000
        data += "yo dogg."
        
        try:
            write_to_path(data, p)
            
            with open(p, 'rb') as handle:
                roundtrip = handle.read()
                assert len(data) == len(roundtrip)
            
            # Ensure we wrote data to the subpath:
            assert os.path.exists(p)
            
            # Ensure that temporary() raises when a deterministic call results
            # in the computation of a file path that already exists –
            # see also the original forms of the deterministic calls, above:
            with pytest.raises(FilesystemError) as exc:
                temporary(prefix='yo-dogg', suffix='tmp', dir=d)
            assert "file exists" in str(exc.value)
            
            with pytest.raises(FilesystemError) as exc:
                temporary(prefix='yo-dogg', suffix='tmp', parent=d)
            assert "file exists" in str(exc.value)
            
            with pytest.raises(FilesystemError) as exc:
                temporary(prefix='yo-dogg', suffix='.tmp', dir=d)
            assert "file exists" in str(exc.value)
            
            with pytest.raises(FilesystemError) as exc:
                temporary(prefix='yo-dogg', suffix='.tmp', parent=d)
            assert "file exists" in str(exc.value)
        
        finally:
            os.unlink(p)
        
        assert not os.path.exists(p)
    
    def test_rm_rf(self):
        # Also involves `write_to_path(…)` and `Directory.walk()`
        from clu.fs.filesystem import write_to_path, rm_rf
        
        # Prepare the temporary directory:
        d = Directory(gettempdir())
        assert d.exists
        
        # Make subdirectories:
        dd = d.subdirectory('yo')
        dd.makedirs()
        ddd = dd.subdirectory('dogg')
        ddd.makedirs()
        dddd = ddd.subdirectory('i_heard')
        dddd.makedirs()
        
        # Check subdirectories:
        assert dd.exists
        assert ddd.exists
        assert dddd.exists
        
        # Prepare some data:
        data = "yo dogg, " * 1000
        data += "yo dogg."
        
        # Make files:
        pp = dd.subpath('yo-dogg.txt')
        write_to_path(data, pp)
        ppp = ddd.subpath('yo-dogg.txt')
        write_to_path(data, ppp)
        pppp = dddd.subpath('yo-dogg.txt')
        write_to_path(data, pppp)
        
        # Check files:
        assert os.path.exists(pp)
        assert os.path.exists(ppp)
        assert os.path.exists(pppp)
        
        yo_dogg_count = 0
        
        for root, dirs, files in dd.walk():
            for filename in files:
                if filename == 'yo-dogg.txt':
                    yo_dogg_count += 1
        
        assert yo_dogg_count == 3
        assert rm_rf(dd)
        
        yo_dogg_count = 0
        
        for root, dirs, files in dd.walk():
            for filename in files:
                if filename == 'yo-dogg.txt':
                    yo_dogg_count += 1
        
        assert yo_dogg_count == 0
        
        # Re-check subdirectories:
        assert not dd.exists
        assert not ddd.exists
        assert not dddd.exists
        
        # Re-check files:
        assert not os.path.exists(pp)
        assert not os.path.exists(ppp)
        assert not os.path.exists(pppp)
    
    def test_which_and_back_tick(self):
        """ Test clu.fs.which(…) and clu.fs.back_tick(…) against one another """
        from clu.fs.filesystem import which, back_tick
        
        BINARIES = ('ls', 'clang', 'gawk',
                    'bpython',
                    'bumpversion')
        
        for binary in BINARIES:
            assert which(binary) == back_tick("which %s" % binary)
    
    def test_write_to_path(self):
        from clu.fs.filesystem import write_to_path
        
        # Prepare the temporary directory:
        d = Directory(gettempdir())
        assert d.exists
        
        # Prepare a new file subpath:
        p = d.subpath('yodogg.txt')
        assert not os.path.exists(p)
        
        # Prepare some data:
        data = "yo dogg, " * 1000
        data += "yo dogg."
        
        try:
            # Call write_to_path(…):
            write_to_path(data, p)
            
            # Check for the file:
            assert os.path.exists(p)
            
            # Read the data back in and compare:
            with open(p, 'rb') as handle:
                roundtrip = handle.read()
                assert len(data) == len(roundtrip)
        
        finally:
            # Ensure we unlink the temporary file subpath:
            os.unlink(p)
        
        assert not os.path.exists(p)
    
    def test_ensure_path_is_valid(self):
        from clu.fs.filesystem import ensure_path_is_valid
        from clu.fs.filesystem import FilesystemError
        
        with pytest.raises(FilesystemError) as exc:
            ensure_path_is_valid(object())
        assert "path type" in str(exc.value)
        
        with pytest.raises(FilesystemError) as exc:
            ensure_path_is_valid(gettempdir())
        assert "over directory" in str(exc.value)
        
        with pytest.raises(FilesystemError) as exc:
            ensure_path_is_valid(gettempdir())
        assert "over directory" in str(exc.value)
        
        with NamedTemporaryFile() as tf:
            tf.write(b"Yo dogg.")
            tf.flush()
            with pytest.raises(FilesystemError) as exc:
                ensure_path_is_valid(tf.name)
            assert "file exists" in str(exc.value)
        
        d = Directory(gettempdir())
        p = d.subdirectory('a/b')
        assert d.exists
        assert not p.exists
        
        with pytest.raises(FilesystemError) as exc:
            ensure_path_is_valid(p)
        assert "Directory" in str(exc.value)
        
        # This one should be sucessful (as in it will not raise):
        ensure_path_is_valid(d.subpath('yodogg.txt'))
        assert not os.path.exists(d.subpath('yodogg.txt'))
    
    def test_TemporaryName(self):
        """ Tests for clu.fs.filesystem.TemporaryName """
        from clu.fs import TemporaryName
        initial = os.getcwd()
        tfp = None
        
        with TemporaryName(prefix="test-temporaryname-",
                           randomized=True) as tfn:
            # print("* Testing TemporaryName file instance: %s" % tfn.name)
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
            # print("* Testing working-directory instance: %s" % cwd.name)
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
            # print("* Testing directory-change instance: %s" % tmp.name)
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
            # print("* Testing TemporaryDirectory instance: %s" % ttd.name)
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

