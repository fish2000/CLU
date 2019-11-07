# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import pytest

class TestFsMisc(object):
    
    """ Run the tests for the clu.fs.misc module. """
    
    def test_re_matcher(self):
        from clu.fs.misc import re_matcher
        
        always = re_matcher(None)
        assert always()
        assert always('yo')
        assert always('yo dogg')
        
        yo = re_matcher('yo')
        assert yo('yo')
        assert yo('yo dogg')
        assert not yo('dogg')
        assert not yo('dogg yo')
    
    def test_re_searcher(self):
        from clu.fs.misc import re_searcher
        
        always = re_searcher(None)
        assert always()
        assert always('yo')
        assert always('yo dogg')
        
        yo = re_searcher('yo')
        assert yo('yo')
        assert yo('yo dogg')
        assert not yo('dogg')
        assert yo('dogg yo')
    
    def test_re_suffix(self):
        from clu.fs.misc import re_suffix
        
        assert re_suffix(None) is None
        assert re_suffix('') is None
        assert re_suffix(".jpg") == "jpg$"
        assert re_suffix("jpg") == "jpg$"
        assert re_suffix(".jpg$") == "jpg$"
        assert re_suffix(".JPG") == "jpg$"
        assert re_suffix("JPG") == "jpg$"
        assert re_suffix(".JPG$") == "jpg$"
    
    def test_suffix_searcher(self, dirname):
        pass
    
    def test_swapext(self):
        from clu.fs.misc import swapext
        
        assert swapext('/yo/dogg.obj', 'odb') == '/yo/dogg.odb'
        assert swapext('/yo/dogg.obj', '.odb') == '/yo/dogg.odb'
        assert swapext('/yo/dogg', 'odb') == '/yo/dogg.odb'
    
    def test_filesize_samesize(self, dirname, temporaryname):
        from clu.testing.utils import countfiles
        from clu.fs.misc import filesize, samesize
        from clu.constants.exceptions import FilesystemError
        
        # Ensure the “data” directory has something
        # in it, of which we can make use:
        data = dirname.subdirectory('data')
        assert countfiles(data) > 10
        
        # Use a TemporaryName instance for the zip archive:
        tzip = temporaryname(prefix='test-fs-misc-filesize-',
                             suffix='zip')
        
        # Create a large zipfile with that instance:
        fzip = data.zip_archive(tzip.name)
        
        # Check the zipfile’s size attributes:
        assert tzip.exists
        assert tzip.filesize > 10000
        assert os.path.exists(tzip)
        assert filesize(tzip.name) > 10000
        
        assert os.path.exists(fzip)
        assert os.path.samefile(tzip, fzip)
        assert samesize(tzip, fzip)
        assert filesize(fzip) > 10000
        
        assert filesize(tzip.name) == filesize(fzip)
        assert filesize(tzip.name) != -1
        assert filesize(fzip) != -1
        
        # Create a nonexistant TemporaryName instance:
        nofile = temporaryname(prefix='test-fs-misc-filesize-',
                               suffix='none')
        
        # Check the nonexistant files’ size attributes:
        assert not nofile.exists
        assert nofile.filesize == -1
        assert not os.path.exists(nofile)
        assert filesize(nofile.name) == -1
        
        with pytest.raises(FilesystemError) as exc:
            assert samesize(tzip, nofile)
        assert "paths must both" in str(exc.value)
        
        with pytest.raises(FilesystemError) as exc:
            assert samesize(fzip, nofile)
        assert "paths must both" in str(exc.value)
    
    def test_differentfile_differentsize_samesize(self, dirname, temporaryname):
        from clu.fs.misc import differentfile, differentsize, samesize
        
        data = "YO DOGG!, " * 1000
        data += "YO DOGG."
        
        somefile = temporaryname(prefix='test-fs-misc-differentfile-',
                                 suffix='wat')
        somefile.write(data)
        
        for root, dirs, files in dirname.subdirectory('data').walk():
            for someotherfile in files:
                theother = os.path.join(root, someotherfile)
                assert differentfile(theother, somefile)
                assert differentsize(theother, somefile)
                assert not samesize(theother, somefile)
        
        yetanotherfile = temporaryname(prefix='test-fs-misc-differentfile-',
                                       suffix='wat')
        yetanotherfile.write(data)
        assert samesize(somefile, yetanotherfile)
        assert differentfile(somefile, yetanotherfile)
        assert not differentsize(somefile, yetanotherfile)
    
    def test_u8bytes_and_u8str(self):
        pass
    
    @pytest.mark.TODO
    def test_win32_longpath(self):
        """ Win32 longpath test TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
