# -*- coding: utf-8 -*-
from __future__ import print_function

class TestExtending(object):
    
    """ Run the tests for extensible and pair types. """
    
    def test_extensible_metaclass(self, dirname):
        from clu.constants.consts import PROJECT_NAME, TEST_PATH
        from clu.extending import Extensible
        import os
        
        class X(metaclass=Extensible):
            
            appname = PROJECT_NAME
            filepath = os.getcwd()
            
            def __init__(self, name=None):
                self._name = name
            
            @property
            def name(self):
                return self._name or type(self).appname
        
        class __extend__(X):
            
            appname = "YoDogg".lower()
            filepath = dirname.subpath(appname)
            
            def __fspath__(self):
                return os.path.realpath(
                       type(self).filepath)
        
        class __extend__(X):
            
            @property
            def path(self):
                return os.fspath(self)
        
        ex = X(name='dogg')
        ux = X()
        
        assert ex.name == 'dogg'
        assert ux.name == 'yodogg'
        assert ex.path == os.path.join(TEST_PATH, ex.appname)
        assert ux.path == os.path.join(TEST_PATH, ux.appname)
        