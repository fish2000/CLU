# -*- coding: utf-8 -*-
from __future__ import print_function
from tempfile import gettempdir

import collections.abc
import contextlib
import os
import pytest

from clu.testing.utils import countfiles
from clu.fs.filesystem import Directory

class TestFsFilesystem(object):
    
    """ Run the tests for the clu.fs.filesystem module. """
    
    @pytest.mark.TODO
    def test_walkback(self, consts, dirname):
        # TODO: this probably falls apart if permissions are
        # unexpectedly restrictive – particularly the check
        # on the ROOT_PATH constant
        directories = {}
        predicate = lambda direntry: len(direntry[0].name)
        
        for root, dirs, files in dirname.walkback():
            directories[Directory(root)] = (dirs, files)
        
        assert len(directories)
        assert Directory(consts.ROOT_PATH) in directories
        
        for root, contents in sorted(directories.items(), key=predicate):
            dirs, files = contents
            for r, d, f in root.walk():
                assert r == root
                assert list(sorted(d)) == list(sorted(dirs))
                assert list(sorted(f)) == list(sorted(files))
                break
    
    def test_suffixes(self, dirname):
        from clu.fs.misc import extension
        
        histo = dirname.suffix_histogram()
        keys = tuple(histo.keys()) # same as dirname.suffixes()
        
        for suffix in dirname.suffixes():
            assert suffix in histo
            assert suffix in keys
        
        for root, dirs, files in dirname.walk():
            for filename in files:
                ext = extension(filename)
                if ext:
                    assert ext in histo
                    assert ext in keys
    
    def test_suffix_histogram(self, dirname):
        histo = dirname.suffix_histogram()
        
        assert len(histo)
        assert 'py' in histo
        assert 'pyc' in histo
        
        for suffix in histo.keys():
            assert histo[suffix] == countfiles(dirname, suffix=suffix)
    
    def test_flatten(self, datadir,
                           temporarydir):
        from clu.typology import isvalidpathlist
        
        # target directory should not already exist:
        target = temporarydir.subdirectory('yodogg')
        
        # call flatten(…) on the datadir, collecting
        # and copying all files contained within it into
        # the target directory, renaming them as per their
        # original pathnames:
        destination, files = datadir.flatten(target)
        
        # target and destination should be the same thing:
        assert target == destination
        
        # files should be a valid path list:
        assert isvalidpathlist(files)
        
        # datadir, target and destination should each
        # contain the same amount of things, regardless
        # of any of their structures:
        assert countfiles(datadir) \
            == countfiles(target) \
            == countfiles(destination) \
            == len(files)
        
        for f in files:
            assert os.path.exists(f)
            assert os.path.basename(f) in destination
    
    def test_flatten_with_suffix_filter(self, datadir,
                                              temporarydir):
        from clu.typology import isvalidpathlist
        
        # target directory should not already exist:
        target = temporarydir.subdirectory('yodogg')
        
        # call flatten(…) on the datadir, collecting
        # and copying all files contained within it with
        # the “jpg” suffix into the target directory,
        # renaming them as per their original pathnames:
        destination, files = datadir.flatten(target, suffix='jpg')
        
        # target and destination should be the same thing:
        assert target == destination
        
        # files should be a valid path list:
        assert isvalidpathlist(files)
        
        # datadir, target and destination should each
        # contain the same amount of JPGs, regardless
        # of any of their structures:
        assert countfiles(datadir, suffix='jpg') \
            == countfiles(target) \
            == countfiles(destination) \
            == len(files)
        
        for f in files:
            assert f.endswith('.jpg')
            assert os.path.exists(f)
            assert os.path.basename(f) in destination
    
    def test_flatten_with_new_suffix(self, datadir,
                                           temporarydir):
        from clu.typology import isvalidpathlist
        
        # target directory should not already exist:
        target = temporarydir.subdirectory('yodogg')
        
        # call flatten(…) on the datadir, collecting
        # and copying all files contained within it into
        # the target directory, renaming them as per their
        # original pathnames and giving *all* of them
        # the “image” suffix:
        destination, files = datadir.flatten(target, new_suffix='image')
        
        # target and destination should be the same thing:
        assert target == destination
        
        # files should be a valid path list:
        assert isvalidpathlist(files)
        
        # datadir, target and destination should each
        # contain the same amount of things, regardless
        # of any of their structures or file suffixes:
        assert countfiles(datadir) \
            == countfiles(target, suffix='image') \
            == countfiles(destination) \
            == len(files)
        
        for f in files:
            assert f.endswith('.image')
            assert os.path.exists(f)
            assert os.path.basename(f) in destination
    
    def test_flatten_with_new_suffix_and_suffix_filter(self, datadir,
                                                             temporarydir):
        from clu.typology import isvalidpathlist
        
        # target directory should not already exist:
        target = temporarydir.subdirectory('yodogg')
        
        # call flatten(…) on the datadir, collecting
        # and copying all files contained within it into
        # the target directory, renaming them as per their
        # original pathnames and giving *all* of them
        # the “jpeg” suffix:
        destination, files = datadir.flatten(target, suffix='jpg',
                                                 new_suffix='jpeg')
        
        # target and destination should be the same thing:
        assert target == destination
        
        # files should be a valid path list:
        assert isvalidpathlist(files)
        
        # datadir, target and destination should each
        # contain the same amount of things, regardless
        # of any of their structures or file suffixes:
        assert countfiles(datadir, suffix='jpg') \
            == countfiles(target, suffix='jpeg') \
            == countfiles(destination) \
            == len(files)
        
        for f in files:
            assert f.endswith('.jpeg')
            assert os.path.exists(f)
            assert os.path.basename(f) in destination
    
    def test_zip_archive_temporaryname(self, dirname, temporaryname):
        from clu.fs.misc import modeflags
        
        # Ensure the “data” directory has something
        # in it, of which we can make use:
        data = dirname.subdirectory('data')
        assert countfiles(data) > 10
        
        # Use a TemporaryName instance for the zip archive:
        tzip = temporaryname(prefix='test-zip-archive-',
                             suffix='zip')
        
        fzip = data.zip_archive(tzip.name)
        
        assert tzip.exists
        assert tzip.filesize > 10000
        assert tzip.flags == modeflags(tzip.mode, tzip.destroy)
        assert os.path.exists(tzip)
        assert os.lstat(tzip).st_size > 10000
        
        assert os.path.exists(fzip)
        assert os.path.samefile(tzip, fzip)
    
    def test_zip_archive(self, dirname):
        from clu.fs.misc import temporary
        
        # Ensure the “data” directory has something
        # in it, of which we can make use:
        data = dirname.subdirectory('data')
        assert countfiles(data) > 10
        
        # Use a temporary file path for the zip archive:
        tzip = temporary(prefix='test-zip-archive-',
                         suffix='zip',
                         randomized=True)
        
        try:
            # Create the zip archive:
            fzip = data.zip_archive(tzip)
            
            assert os.path.exists(tzip)
            assert os.lstat(tzip).st_size > 10000
            
            assert os.path.exists(fzip)
            assert os.path.samefile(tzip, fzip)
        
        finally:
            os.unlink(tzip)
    
    def test_script_path(self):
        from clu.fs.filesystem import script_path
        
        scripts = Directory(script_path())
        assert scripts.exists
        assert scripts.parent().basename == 'clu'
        assert '.gitignore' in scripts
        assert '__init__.py' in scripts # it’s a Python module directory
        
    def test_rm_rf(self, temporarydir):
        # Also involves `write_to_path(…)` and `Directory.walk()`
        from clu.fs.filesystem import write_to_path, rm_rf
        
        # Make subdirectories:
        dd = temporarydir.subdirectory('yo')
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
        
        assert countfiles(dd, suffix='yo-dogg.txt') == 3
        assert rm_rf(dd)
        
        assert countfiles(dd, suffix='yo-dogg.txt') == 0
        
        # Re-check subdirectories:
        assert not dd.exists
        assert not ddd.exists
        assert not dddd.exists
        
        # Re-check files:
        assert not os.path.exists(pp)
        assert not os.path.exists(ppp)
        assert not os.path.exists(pppp)
    
    @pytest.mark.TODO
    def test_which_and_back_tick(self):
        """ Test clu.fs.which(…) and clu.fs.back_tick(…) against one another """
        # TODO: ensure that these binaries are plausibly portable
        from clu.fs.filesystem import which, back_tick
        
        BINARIES = ('ls', 'cat', 'df',
                    'python',
                    'python-config')
        
        for binary in BINARIES:
            assert which(binary) == back_tick(f"which {binary}")
    
    def test_write_to_path(self, temporarydir):
        from clu.fs.filesystem import write_to_path
        
        # Prepare a new file subpath:
        p = temporarydir.subpath('yodogg.txt')
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
    
    def test_ensure_path_is_valid(self, temporarydir):
        from clu.constants.exceptions import FilesystemError
        from clu.fs.filesystem import ensure_path_is_valid
        from clu.fs.filesystem import NamedTemporaryFile
        
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
        
        p = temporarydir.subdirectory('a/b')
        assert temporarydir.exists
        assert not temporarydir.change
        assert not p.exists
        
        with pytest.raises(FilesystemError) as exc:
            ensure_path_is_valid(p)
        assert "Directory" in str(exc.value)
        
        # This one should be sucessful (as in it will not raise):
        ensure_path_is_valid(temporarydir.subpath('yodogg.txt'))
        assert not os.path.exists(temporarydir.subpath('yodogg.txt'))
    
    def test_TemporaryName(self):
        """ Tests for clu.fs.filesystem.TemporaryName """
        from clu.fs.filesystem import TemporaryName
        from clu.fs.misc import modeflags
        initial = os.getcwd()
        tfp = None
        
        with TemporaryName(prefix="test-temporaryname-",
                           randomized=True) as tfn:
            # print("* Testing TemporaryName file instance: %s" % tfn.name)
            assert os.path.samefile(os.getcwd(),            initial)
            assert gettempdir() in tfn.name
            assert tfn.prefix == "test-temporaryname-"
            assert tfn.suffix == ".tmp"
            assert tfn.mode == 'wb'
            assert tfn.binary_mode
            assert not tfn._parent
            assert tfn.prefix in tfn.name
            assert tfn.suffix in tfn.name
            assert tfn.prefix in os.fspath(tfn)
            assert tfn.suffix in os.fspath(tfn)
            assert tfn.destroy
            assert tfn.flags == modeflags('wb', delete=True)
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
        from clu.fs.filesystem import wd
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
        from clu.fs.filesystem import cd
        from clu.fs.misc import differentfile
        initial = os.getcwd()
        
        with cd(gettempdir()) as tmp:
            # print("* Testing directory-change instance: %s" % tmp.name)
            assert os.path.samefile(os.getcwd(),          gettempdir())
            assert os.path.samefile(os.getcwd(),          tmp.new)
            assert os.path.samefile(gettempdir(),         tmp.new)
            assert os.path.samefile(os.getcwd(),          os.fspath(tmp))
            assert os.path.samefile(gettempdir(),         os.fspath(tmp))
            assert differentfile(os.getcwd(),             initial)
            assert differentfile(tmp.new,                 initial)
            assert differentfile(os.fspath(tmp),          initial)
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
    
    def test_td(self):
        """ Tests for clu.fs.filesystem.td """
        from clu.fs.filesystem import td
        from clu.fs.misc import differentfile
        initial = os.getcwd()
        
        with td() as tmp:
            # print("* Testing directory-change instance: %s" % tmp.name)
            assert os.path.samefile(os.getcwd(),          gettempdir())
            assert os.path.samefile(os.getcwd(),          tmp.new)
            assert os.path.samefile(gettempdir(),         tmp.new)
            assert os.path.samefile(os.getcwd(),          os.fspath(tmp))
            assert os.path.samefile(gettempdir(),         os.fspath(tmp))
            assert differentfile(os.getcwd(),             initial)
            assert differentfile(tmp.new,                 initial)
            assert differentfile(os.fspath(tmp),          initial)
            assert os.path.samefile(tmp.old,              initial)
            assert tmp.will_change
            assert tmp.did_change
            assert tmp.will_change_back
            assert not tmp.did_change_back
            assert type(tmp.directory(tmp.new)) == Directory
            assert isinstance(tmp,                        td)
            assert isinstance(tmp,                        Directory)
            assert isinstance(tmp,                        collections.abc.Hashable)
            assert isinstance(tmp,                        collections.abc.Mapping)
            assert isinstance(tmp,                        collections.abc.Sized)
            assert isinstance(tmp,                        contextlib.AbstractContextManager)
            assert isinstance(tmp,                        os.PathLike)
            assert os.path.isdir(os.fspath(tmp))
            assert tmp.basename in tmp.dirname
    
    def test_hd(self):
        """ Tests for clu.fs.filesystem.hd """
        from clu.fs.filesystem import hd
        from clu.fs.misc import differentfile, gethomedir
        initial = os.getcwd()
        
        with hd() as home:
            # print("* Testing directory-change instance: %s" % tmp.name)
            assert os.path.samefile(os.getcwd(),          gethomedir())
            assert os.path.samefile(os.getcwd(),          home.new)
            assert os.path.samefile(gethomedir(),         home.new)
            assert os.path.samefile(os.getcwd(),          os.fspath(home))
            assert os.path.samefile(gethomedir(),         os.fspath(home))
            assert differentfile(os.getcwd(),             initial)
            assert differentfile(home.new,                initial)
            assert differentfile(os.fspath(home),         initial)
            assert os.path.samefile(home.old,             initial)
            assert home.will_change
            assert home.did_change
            assert home.will_change_back
            assert not home.did_change_back
            assert type(home.directory(home.new)) == Directory
            assert isinstance(home,                        hd)
            assert isinstance(home,                        Directory)
            assert isinstance(home,                        collections.abc.Hashable)
            assert isinstance(home,                        collections.abc.Mapping)
            assert isinstance(home,                        collections.abc.Sized)
            assert isinstance(home,                        contextlib.AbstractContextManager)
            assert isinstance(home,                        os.PathLike)
            assert os.path.isdir(os.fspath(home))
            assert home.basename in home.dirname
    
    def test_TemporaryDirectory(self):
        """ Tests for clu.fs.filesystem.TemporaryDirectory """
        from clu.fs.filesystem import TemporaryDirectory
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
            assert ttd.change
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

