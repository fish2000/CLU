# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

mods = ('clu.all',
        'clu.abstract',
        'clu.constants.consts',
        'clu.constants.polyfills',
        'clu.config.keymap',
        'clu.config.ns',
        'clu.csv',
        'clu.fs.appdirectories',
        'clu.keyvalue',
        'clu.dispatch',
        'clu.scripts.boilerplate',
        'clu.sanitizer',
        'clu.fs.pypath',
        'clu.scripts.ansicolors')

class TestScriptsREPL(object):
    
    """ Run the tests for the “clu.scripts.repl” module. """
    
    @pytest.mark.TODO
    def test_repl_module(self, consts, environment, testdir):
        # TODO: assert that the figlet banner stuff is present, too
        environment['PYTHONPATH'] = f".:{consts.PROJECT_PATH}:{consts.BASEPATH}"
        testdir.syspathinsert(consts.PROJECT_PATH)
        testdir.syspathinsert(consts.BASEPATH)
        
        result = testdir.runpython_c('import clu.scripts.repl')
        assert len(result.outlines) > 0
        
        output = "\n".join(result.outlines)
        # assert 'DEBUG MODE INITIATED' in output
        assert '888' in output # part of 'python' figlet banner
    
    @pytest.mark.parametrize('modulename', mods)
    def test_repl_explain(self, modulename):
        from clu.scripts.repl import explain
        from clu.naming import suffix, qualified_import
        from contextlib import redirect_stdout
        import io
        
        module = qualified_import(modulename)
        thingcount = len(dir(module))
        
        iosink = io.StringIO()
        with redirect_stdout(iosink):
            explain(module)
        
        output = iosink.getvalue()
        iosink.truncate(0)
        iosink.close()
        
        assert 'Module instance' in output
        assert suffix(modulename) in output
        if thingcount == 0:
            assert "contains no “dir(…)” results" in output
        elif thingcount == 1:
            assert "contains one sub-thing" in output
        else:
            assert f'{thingcount} sub-things' in output
        
        for thingname in dir(module):
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
        from clu.predicates import ispublic
        from clu.scripts.repl import star_export
        
        module = qualified_import(modulename)
        star_export(modulename, namespace=locals())
        
        for thingname in dir(module):
            if ispublic(thingname):
                assert thingname in locals()
