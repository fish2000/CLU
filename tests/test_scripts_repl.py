# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

mods = ('clu.all',
        'clu.abstract',
        'clu.constants.consts',
        'clu.constants.polyfills',
        'clu.config.base',
        'clu.config.settings',
        'clu.config.ns',
        'clu.csv',
        'clu.fs.appdirectories',
        'clu.keyvalue',
        'clu.dispatch',
        'clu.sanitizer',
        'clu.fs.pypath',
        'clu.scripts.ansicolors')

class TestScriptsREPL(object):
    
    """ Run the tests for the clu.scripts.repl module. """
    
    @pytest.mark.TODO
    def test_repl_module(self, consts, environment, testdir):
        # TODO: assert that the figlet banner stuff is present, too
        environment['PYTHONPATH'] = f".:{consts.PROJECT_PATH}:{consts.BASEPATH}"
        testdir.syspathinsert(consts.PROJECT_PATH)
        testdir.syspathinsert(consts.BASEPATH)
        
        result = testdir.runpython_c('import clu.scripts.repl')
        assert len(result.outlines) > 0
        
        output = "\n".join(result.outlines)
        assert 'DEBUG MODE INITIATED' in output
    
    def test_repl_explain(self):
        # “dir(clu.all)” dependably contains but 3 function names:
        import clu.all
        from clu.scripts.repl import explain
        
        from contextlib import redirect_stdout
        import io
        
        iosink = io.StringIO()
        with redirect_stdout(iosink):
            explain(clu.all)
        
        output = iosink.getvalue()
        iosink.close()
        
        assert 'Module instance' in output
        assert '3 sub-things' in output
        
        for thingname in dir(clu.all):
            assert thingname in output
    
    @pytest.mark.parametrize('modulename', mods)
    def test_repl_module_export(self, consts, modulename):
        from clu.scripts.repl import module_export
        
        module_export(modulename, namespace=locals())
        
        assert modulename in locals()
        assert modulename.split(consts.QUALIFIER)[-1] in locals()
    
    @pytest.mark.parametrize('modulename', mods)
    def test_repl_star_export(self, modulename):
        from clu.naming import qualified_import
        from clu.scripts.repl import star_export
        
        module = qualified_import(modulename)
        star_export(modulename, namespace=locals())
        
        for thingname in dir(module):
            assert thingname in locals()
