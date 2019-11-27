# -*- coding: utf-8 -*-
from __future__ import print_function

# import pytest

class TestDispatch(object):
    
    """ Run the tests for the “clu.dispatch” module """
    
    def test_exithandle(self, testdir, consts):
        testdir.syspathinsert(consts.PROJECT_PATH)
        testdir.syspathinsert(consts.BASEPATH)
        testdir.makeconftest("""
            pytest_plugins = "clu.testing.pytest"
        """)
        
        path = testdir.makepyfile("""
            import sys
            sys.path.insert(0, "%s")
            sys.path.insert(0, "%s")
            
            def test():
                from clu.dispatch import (exithandle,
                                          signal_for,
                                          trigger,
                                          nhandles)
                
                @exithandle
                def xhandle0(signum, frame=None):
                    print("Entering xhandle0")
                    sig = signal_for(signum)
                    print(f"Received signal: {sig.name} ({sig.value})")
                    return True
                
                @exithandle
                def xhandle1(signum, frame=None):
                    print("Entering xhandle1")
                    sig = signal_for(signum)
                    print(f"Received signal: {sig.name} ({sig.value})")
                    return True
                
                # Won’t register an already-registered handle:
                exithandle(xhandle1)
                
                assert nhandles() == 2
                
                print("Triggering…")
                assert trigger()
                assert nhandles() == 0
                
                @exithandle
                def xhandleX(signum, frame=None):
                    print("Entering xhandleX")
                    sig = signal_for(signum)
                    print(f"Received signal: {sig.name} ({sig.value})")
                    return True
                
                assert nhandles() == 1
                print("About to exit function test()…")
                return 0
            
            if __name__ == '__main__':
                sys.exit(test())
        """ % (consts.PROJECT_PATH,
               consts.BASEPATH))
        
        result = testdir.runpython(path)
        
        assert len(result.outlines) == 8
        assert result.outlines[0] == "Triggering…"
        assert result.outlines[1] == "Entering xhandle0"
        assert result.outlines[2] == "Received signal: SIGSTOP (17)"
        assert result.outlines[3] == "Entering xhandle1"
        assert result.outlines[4] == "Received signal: SIGSTOP (17)"
        assert result.outlines[5] == "About to exit function test()…"
        assert result.outlines[6] == "Entering xhandleX"
        assert result.outlines[7] == "Received signal: SIGSTOP (17)"