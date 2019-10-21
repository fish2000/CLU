# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestImporting(object):
    
    def test_basic_module(self):
        from clu.constants.consts import PROJECT_NAME
        from clu.naming import nameof
        from clu.importing import Registry, Module
        
        m = Module(name=PROJECT_NAME)
        assert m
        assert m.appname == PROJECT_NAME
        assert m.appspace == 'app'
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == PROJECT_NAME
        
        assert len(Registry.monomers) > 0
        
        with pytest.raises(AttributeError) as exc:
            assert len(m.monomers) == 0
        assert "has no attribute" in str(exc.value)
    
    def test_derived_modules(self):
        from clu.importing import ModuleBase, Module
        
        class MyOtherModule(ModuleBase):
            pass
        
        class MyDerivedModule(Module):
            pass
        
        class MyDerivedOther(MyOtherModule):
            pass
        
        o = MyOtherModule(name="other")
        d = MyDerivedModule(name="derived")
        O = MyDerivedOther(name="derived-other")
        
        assert o
        assert d
        assert O
    
    def test_derived_module_methods(self):
        from clu.importing import ModuleBase, Module
        
        class ThisOtherModule(ModuleBase):
            def yodogg(self):
                return True
        
        class ThisDerivedModule(Module):
            def yodogg(self):
                return False
        
        class ThisDerivedOther(ThisOtherModule):
            def yodogg(self):
                return "Yo Dogg"
        
        o = ThisOtherModule(name="other")
        d = ThisDerivedModule(name="derived")
        O = ThisDerivedOther(name="derived-other")
        
        assert o.yodogg()
        assert not d.yodogg()
        assert O.yodogg() == 'Yo Dogg'
    
    def test_finder_and_loader_methods(self):
        from clu.importing import Finder, Loader, Module
        import sys
        
        finder = Finder()
        assert type(finder.loader) is Loader
        assert type(finder) in sys.meta_path
        
        class findme(Module):
            pass
        
        spec = finder.find_spec('clu.app.findme', [])
        assert spec.name == 'clu.app.findme'
        
        module = finder.loader.create_module(spec)
        assert type(module) is findme
        
        # assert repr(module) == "<class-module ‘clu.app.findme’ from “clu.app”>"
    
    def test_derived_import(self):
        from clu.importing import Module, DO_NOT_INCLUDE
        
        class Derived(Module):
            
            """ I heard you like docstrings """
            
            yo = 'dogg'
            
            def iheard(self):
                return "I heard you like"
        
        from clu.app import Derived as derived
        
        assert type(derived) is Derived
        assert derived.yo == 'dogg'
        
        for attname in dir(derived):
            assert hasattr(derived, attname)
        
        for attname in DO_NOT_INCLUDE:
            assert attname not in dir(derived)
        
        assert derived.iheard() == 'I heard you like'
        
        from clu.app.Derived import iheard
        
        assert iheard() == 'I heard you like'
    
    