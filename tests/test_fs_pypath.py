# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest
import sys, os

from clu.typology import isvalidpathlist
from clu.fs.misc import temporary
from clu.fs import pypath

prepend = (False, True)

class TestFsPypath(object):
    
    existing = []
    existings = {}
    
    @classmethod
    def setup_class(cls):
        """ Stash the operating values for sys.path """
        pypath.remove_invalid_paths()
        cls.existing = list(sys.path)
    
    @classmethod
    def teardown_class(cls):
        """ Restore the operating values for sys.path """
        sys.path[:] = list(cls.existing)
    
    def setup_method(self, method):
        """ Stash the operating values for sys.path """
        type(self).existings[method.__name__] = list(sys.path)
    
    def teardown_method(self, method):
        """ Restore the operating values for sys.path """
        sys.path[:] = list(type(self).existings[method.__name__])
    
    @pytest.mark.parametrize('prepend', prepend)
    def test_add_paths(self, temporarydir, prepend):
        """ Add paths to sys.path """
        badpth = temporary(prefix='yo-dogg-',
                           suffix='tmp',
                           randomized=True,
                           dir=temporarydir)
        goodpth = temporary(prefix='yo-dogg-',
                            suffix='tmp',
                            randomized=True,
                            dir=temporarydir)
        os.makedirs(goodpth)
        
        badadd = pypath.add_paths(badpth, prepend=prepend)
        goodadd = pypath.add_paths(goodpth, prepend=prepend)
        
        assert badadd[badpth] == False
        assert goodadd[goodpth] == True
        # with pytest.raises()
        
        assert badpth not in sys.path
        assert goodpth in sys.path
        
        if prepend:
            assert sys.path[0] == goodpth
        else:
            assert sys.path[-1:][0] == goodpth
        
        existing = prepend and sys.path[-1:][0] or sys.path[0]
        assert existing in sys.path
        
        existingadd = pypath.add_paths(existing)
        assert existingadd[existing] == False
        
        os.rmdir(goodpth)
        assert not os.path.exists(goodpth)
    
    def test_mutate_syspath(self):
        """ Remove non-matching paths from sys.path """
        iterable = sys.path[:2]
        out = pypath.mutate_syspath(iterable)
        assert sys.path == iterable
        assert out == iterable
    
    def test_remove_paths(self, temporarydir):
        """ Remove paths from sys.path """
        # pypath.remove_invalid_paths()
        removals = list(sys.path[:2])
        removals.append(temporary(parent=temporarydir))
        out = pypath.remove_paths(*removals)
        # pathset = set(sys.path)
        for removal in removals:
            assert removal not in sys.path
            assert out[removal] == os.path.exists(removal)
            # assert out[removal] == bool(removal in pathset)
    
    def test_remove_invalid_paths(self, temporarydir):
        """ Remove invalid paths from sys.path """
        badpth = temporary(parent=temporarydir)
        sys.path.append(badpth)
        out = pypath.remove_invalid_paths()
        for path in sys.path:
            assert os.path.exists(path)
        assert out[badpth] == True
    
    def test_enhance(self):
        """ Check the “enhance(¬)” convenience method """
        # clu.fs.pypath.ehhance(¬) removes invalid paths,
        # before adding its operand paths using “add_paths(¬)”