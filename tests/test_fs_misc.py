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
        pass
    
    def test_suffix_searcher(self, datadir):
        pass
    
    def test_swapext(self):
        pass
    
    def test_filesize(self, datadir, temporaryname):
        from clu.testing.utils import countfiles
        from clu.fs.misc import filesize
        
        # Ensure the “datadir” fixture has something
        # in it, of which we can make use:
        assert countfiles(datadir) > 10
        
        # Use a TemporaryName instance for the zip archive:
        tzip = temporaryname(prefix='test-fs-misc-filesize-',
                             suffix='zip')
        
        # Create a large zipfile with that instance:
        fzip = datadir.zip_archive(tzip.name)
        
        # Check the zipfile’s size attributes:
        assert tzip.exists
        assert tzip.filesize > 10000
        assert os.path.exists(tzip)
        assert filesize(tzip.name) > 10000
        
        assert os.path.exists(fzip)
        assert os.path.samefile(tzip, fzip)
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
    
    def test_differentfile(self, datadir):
        pass
    
    def test_samesize(self, temporaryname):
        pass
    
    def test_differentsize(self, temporaryname):
        pass
    
    def test_u8bytes_and_u8str(self):
        pass
    
    @pytest.mark.TODO
    def test_win32_longpath(self):
        """ Win32 longpath test TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
