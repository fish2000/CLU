# -*- coding: utf-8 -*-
from __future__ import print_function

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
    
    def test_filesize(self, temporaryname):
        pass
    
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
