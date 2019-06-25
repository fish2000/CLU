# -*- coding: utf-8 -*-
from __future__ import print_function

class TestNaming(object):
    
    """ Run the tests for the clu.naming module. """
    
    def test_qualified_name(self):
        """ » Checking “qualified_name(¬) …” """
        # print(test_qualified_name.__doc__)
        # print()
        from clu.constants import BUILTINS
        from clu.naming import qualified_name
        from clu.typespace import types
        
        assert qualified_name(BUILTINS) == 'clu.constants.consts.BUILTINS'
        assert qualified_name(types) == 'clu.typespace.namespace.types'
        
        # print_separator()
        # print('qualified_name(BUILTINS):', qualified_name(BUILTINS))
        # print('qualified_name(types):', qualified_name(types))
        # print_separator()
        # print()
    
    def test_qualified_import(self):
        """ » Checking “qualified_import(¬) …” """
        # print(test_qualified_import.__doc__)
        # print()
        # print()
        from clu.naming import qualified_import, qualified_name
        
        print_python_banner = qualified_import('clu.repl.print_python_banner')
        print_warning       = qualified_import('clu.repl.print_warning')
        # replenv_modules     = qualified_import('clu.repl.modules')
        # python2_expires     = qualified_import('clu.repl.python2_expires')
        # is_python2_dead     = qualified_import('clu.repl.banners.is_python2_dead')
        
        assert qualified_name(print_python_banner) == 'clu.repl.banners.print_python_banner'
        assert qualified_name(print_warning)       == 'clu.repl.banners.print_warning'
        # assert qualified_name(replenv_modules)     == 'clu.repl.modules' # huh.
        # assert qualified_name(python2_expires)     == 'clu.repl.python2_expires'
        # assert qualified_name(is_python2_dead)     == 'clu.repl.is_python2_dead'
        
        # print_separator()
        # print('qualified_name(print_python_banner):', qualified_name(print_python_banner), '', repr(Clade.of(print_python_banner)))
        # print('qualified_name(print_warning):      ',       qualified_name(print_warning), '      ', repr(Clade.of(print_warning)))
        # print('qualified_name(replenv_modules):    ',     qualified_name(replenv_modules), '            ', repr(Clade.of(replenv_modules)))
        # print('qualified_name(python2_expires):    ',     qualified_name(python2_expires), '    ', repr(Clade.of(python2_expires)))
        # print('qualified_name(is_python2_dead):    ',     qualified_name(is_python2_dead), '    ', repr(Clade.of(is_python2_dead)))
        # print_separator()
        # print()
    
    def _test_determine_module(self):
        """ » Checking `determine_module(…)` against `pickle.whichmodule(…)` …"""
        # print(test_determine_module.__doc__)
        # print()
        from clu.naming import determine_module
        
        import pickle
        mismatches = 0
        # print_separator()
        
        for name, thing in exporter.exports().items():
            # clade = Clade.of(thing, name_hint=name)
            determination = determine_module(thing)
            whichmodule = pickle.whichmodule(thing, None)
            try:
                assert determination == whichmodule
            except AssertionError:
                mismatches += 1
                # print("»»» Module-lookup mismatch for %s “%s”" % (clade.to_string(), name))
                # print("»»»   determine_module(…) → %s" % determination)
                # print("»»» pickle.whichmodule(…) → %s" % whichmodule)
                # print()
        
        # print("≠≠≠ TOTAL EXPORTED THING COUNT: %i" % len(exporter))
        # print("≠≠≠ TOTAL MISMATCHES FOUND: %i" % mismatches)
        # print_separator()
        # print()
    