# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestKeyValue(object):
    
    """ Run the tests for the clu.keyvalue module. """
    
    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_keyvalue_cluinterface_basics(self, environment, temporarydir):
        from clu.keyvalue import CLUInterface
        from tempfile import gettempdir
        
        interface = CLUInterface(datadir=temporarydir)
        
        assert temporarydir.exists
        assert temporarydir.name.startswith(gettempdir())
        assert len(interface) == 0
        
        dict_one = { 'compress_level' : 9,
                           'optimize' : True,
                             'format' : 'png',
                                 'yo' : 'dogg' }
        
        interface.update(dict_one)
        
        assert len(tuple(temporarydir.ls())) == 4
        assert len(interface) == 4
        
        assert interface['compress_level'] == 9
        assert interface['optimize']       == True
        assert interface['format']         == "png"
        assert interface['yo']             == "dogg"
        
        with CLUInterface(datadir=temporarydir) as sidehustle:
            
            assert len(sidehustle) == 4
            
            assert sidehustle['compress_level'] == 9
            assert sidehustle['optimize']       == True
            assert sidehustle['format']         == "png"
            assert sidehustle['yo']             == "dogg"
        
        assert len(tuple(temporarydir.ls())) == 4
