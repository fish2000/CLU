# -*- coding: utf-8 -*-
from __future__ import print_function

snippet = """
import sys
sys.path.insert(0, "%s")
sys.path.insert(0, "%s")
"""

class TestBoilerplate(object):
    
    """ Run the tests for the “clu.repl.cli.boilerplate” module """
    
    def test_boilerplate_function(self):
        """ Sanity-check the output of the boilerplate-generation function """
        from clu.repl.cli.boilerplate import boilerplate_command
        from contextlib import redirect_stdout
        import io
        
        iosink = io.StringIO()
        with redirect_stdout(iosink):
            boilerplate_command()
        
        output = iosink.getvalue()
        iosink.close()
        
        assert "from clu.exporting import Exporter" in output
        assert "INSERT MODULE CODE HERE" in output
        assert "INSERT TESTING CODE HERE" in output
        assert "INSERT DIAGNOSTIC CODE HERE" in output
        assert "return inline.test(100)" in output
    
    def test_boilerplate_code(self, testdir, consts):
        """ Actually run the boilerplate code, ensuring that it’ll basically work """
        from clu.repl.cli.boilerplate import boilerplate
        
        testdir.syspathinsert(consts.PROJECT_PATH)
        testdir.syspathinsert(consts.BASEPATH)
        testdir.makeconftest("""
            pytest_plugins = "clu.testing.pytest"
        """)
        
        code = boilerplate.replace("from __future__ import print_function",
                                    snippet % (consts.PROJECT_PATH,
                                               consts.BASEPATH))
        
        path = testdir.makepyfile(code)
        result = testdir.runpython(path)
        assert len(result.outlines) > 0
        
        output = "\n".join(result.outlines)
        assert "RUNNING TEST" in output
        assert "test_one(¬)" in output
        assert "TIME TOTALS" in output
        assert "a hundred times" in output