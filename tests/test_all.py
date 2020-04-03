# -*- coding: utf-8 -*-
from __future__ import print_function

# import pytest

class TestAll(object):
    
    """ Run the tests for the “clu.all” module. """
    
    def test_all_inline_tests(self):
        from clu.all import inline_tests, code_attrs
        from clu.naming import qualified_import
        from clu.predicates import resolve, attrs
        import inspect
        
        inlines = tuple(inline_tests())
        modules = (qualified_import(inline) for inline in inlines)
        
        test_nm = 'test'
        for module in modules:
            test_fn = resolve(module, test_nm)
            assert inspect.isfunction(test_fn)
            code_nm = attrs(test_fn, *code_attrs)
            assert any('inline' in name for name in code_nm)
