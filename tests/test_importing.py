# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestImporting(object):
    
    def test_module_dict_proxy_idea(self, consts):
        from clu.dicts import ChainMap
        from clu.importing import Module, Registry
        from clu.typology import ismodule, ismapping
        
        overrides = dict(PROJECT_NAME='yodogg',
                         PROJECT_PATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg/yodogg',
                         BASEPATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg')
        
        try:
            
            class PutativeProxyModule(Module):
                
                def add_targets(self, *targets):
                    if getattr(self, 'target_dicts', None) is None:
                        self.target_dicts = []
                    for target in targets:
                        if target is None:
                            continue
                        if ismodule(target):
                            self.target_dicts.append(target.__dict__)
                            continue
                        if ismapping(target):
                            self.target_dicts.append(target)
                            continue
                
                def __init__(self, name, *targets, doc=None):
                    self.target_dicts = []
                    super(Module, self).__init__(name, doc=doc)
                    self.add_targets(*targets)
                    if hasattr(self, 'targets'):
                        self.add_targets(*self.targets)
                
                def __execute__(self):
                    self.__proxies__ = ChainMap(*self.target_dicts)
                    super().__execute__()
                
                def __getattr__(self, key):
                    # N.B. AttributeError typenames (herein “PutativeProxyModule”)
                    # must be hardcoded – using “self.name” leads to an infinite
                    # recursion kertwang within “__getattr__(…)” – since “name”
                    # is a property that uses “nameof(self)” which invariably will
                    # attempt to get one or another nonexistant attributes from ‘self’.
                    if not '_executed' in self.__dict__:
                        raise AttributeError(f"'PutativeProxyModule' object has no attribute '{key}'")
                    try:
                        return self.__proxies__[key]
                    except KeyError:
                        raise AttributeError(f"'PutativeProxyModule' object has no attribute '{key}'")
            
            class testing_overridden_consts(PutativeProxyModule):
                # def __execute__(self):
                #     self.add_targets(overrides, consts)
                #     super().__execute__()
                targets = (overrides, consts)
            
            from clu.app import testing_overridden_consts as overridden
            
            assert overridden.USER == consts.USER
            assert overridden.BUILTINS == consts.BUILTINS
            assert overridden.PROJECT_NAME == 'yodogg'
            assert overridden.PROJECT_PATH.endswith('yodogg')
            assert overridden.BASEPATH.endswith('yodogg')
            
            with pytest.raises(AttributeError) as exc:
                assert overridden.YODOGG
            assert "has no attribute" in str(exc.value)
        
        finally:
            for clsmod in (PutativeProxyModule,
                           testing_overridden_consts):
                Registry.unregister(clsmod.appname,
                                    clsmod.qualname)
    
    def test_module_export_within_execute(self):
        from clu.importing import Module, Registry, DO_NOT_INCLUDE
        from clu.exporting import Exporter
        
        try:
        
            class DerivedWithExecute(Module):
                
                """ I heard you like docstrings """
                
                yo = 'dogg'
                
                def iheard(self):
                    return "I heard"
                
                def youlike(self):
                    return "you like"
                
                def unexported(self):
                    return "conditionally exporting things"
                
                def __execute__(self):
                    """ Class-module execution hook code """
                    cls = type(self)
                    # export class-module functions:
                    export = cls.exporter.decorator()
                    export(self.yo,      name='yo')
                    export(self.iheard,  name='iheard')
                    export(self.youlike, name='youlike')
                    # assert module attributes:
                    assert cls.appname == 'clu'
                    assert cls.appspace == 'app'
                    assert cls.name == 'DerivedWithExecute'
                    assert cls.prefix == 'clu.app'
                    assert cls.qualname == 'clu.app.DerivedWithExecute'
                    # calling up not technically necessary RN:
                    super().__execute__()
            
            # Normally we’d just call the class “derived”, rather
            # than “Derived” – in this case we need to differentiate
            # betweeen the name of the defined class and the thing
            # we imported within the same code block (normally they’d
            # be in separate files):
            from clu.app import DerivedWithExecute as derived
            
            assert type(derived) is DerivedWithExecute
            assert repr(derived) == "<class-module ‘clu.app.DerivedWithExecute’ from “clu.app”>"
            assert derived.yo == 'dogg'
            
            assert type(derived.exporter) is Exporter
            assert len(derived.exporter) == len(dir(derived))
            assert derived.exporter.dotpath == derived.qualname
            
            durr = dir(derived)
            assert 'yo' in durr
            assert 'iheard' in durr
            assert 'youlike' in durr
            assert 'unexported' not in durr
            
            for attname in dir(derived):
                assert hasattr(derived, attname)
            
            for attname in DO_NOT_INCLUDE:
                assert attname not in dir(derived)
            
            assert derived._executed
            
            assert derived.iheard() == 'I heard'
            assert derived.youlike() == 'you like'
            assert derived.unexported() == 'conditionally exporting things'
            
            from clu.app.DerivedWithExecute import yo, iheard, youlike
            
            assert yo == 'dogg'
            assert iheard() == 'I heard'
            assert youlike() == 'you like'
        
        finally:
            Registry.unregister(derived.appname, derived.qualname)
    
    def test_basic_module(self, consts):
        from clu.naming import nameof
        from clu.importing import Registry, Module
        
        m = Module(name=consts.PROJECT_NAME)
        assert m
        assert m.appname == consts.PROJECT_NAME
        assert m.appspace == 'app'
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == consts.PROJECT_NAME
        
        assert len(Registry.monomers) > 0
        assert len(m.monomers) == 0
    
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
        assert repr(module) == "<class-module ‘clu.app.findme’>"
        
        # …calling “module_repr(…)” directly doesn’t know about the location:
        # assert finder.loader.module_repr(module) == "<class-module ‘clu.app.findme’>"
    
    def test_derived_import(self):
        from clu.importing import Module, Registry, DO_NOT_INCLUDE
        
        try:
        
            class Derived(Module):
                
                """ I heard you like docstrings """
                
                yo = 'dogg'
                
                def iheard(self):
                    return "I heard you like"
            
            # Normally we’d just call the class “derived”, rather
            # than “Derived” – in this case we need to differentiate
            # betweeen the name of the defined class and the thing
            # we imported within the same code block (normally they’d
            # be in separate files):
            from clu.app import Derived as derived
            
            assert type(derived) is Derived
            assert repr(derived) == "<class-module ‘clu.app.Derived’ from “clu.app”>"
            assert derived.yo == 'dogg'
            
            for attname in dir(derived):
                assert hasattr(derived, attname)
            
            for attname in DO_NOT_INCLUDE:
                assert attname not in dir(derived)
            
            assert derived.iheard() == 'I heard you like'
            
            from clu.app.Derived import iheard
            
            assert iheard() == 'I heard you like'
        
        finally:
            Registry.unregister(derived.appname, derived.qualname)
    
    def test_initialize_types(self, dirname):
        from clu.fs import pypath
        
        # Ensure “sys.path” contains the “yodogg” package:
        prefix = dirname.subdirectory('yodogg')
        assert prefix.exists
        pypath.enhance(prefix)
        
        # Bring in the package-specific Module subclass
        from yodogg.config import Module
        
        try:
            
            class Derived(Module):
                
                """ I heard you like docstrings """
                
                yo = 'dogg'
                
                def iheard(self):
                    return "I heard you like"
            
            from yodogg.modules import Derived as derived
            
            assert type(derived) is Derived
            assert repr(derived) == "<class-module ‘yodogg.modules.Derived’ from “yodogg.modules”>"
            assert derived.yo == 'dogg'
            
            for attname in dir(derived):
                assert hasattr(derived, attname)
            
            assert derived.iheard() == 'I heard you like'
            
            from yodogg.modules.Derived import iheard
            
            assert iheard() == 'I heard you like'
        
        finally:
            from clu.importing import Registry
            Registry.unregister(derived.appname, derived.qualname)
    
    def test_derived_import_with_export(self):
        from clu.importing import Module, Registry, DO_NOT_INCLUDE
        from clu.exporting import Exporter
        export = None # SHUT UP, PYFLAKES!!
        
        try:
        
            class AnotherDerived(Module):
                
                """ I heard you like docstrings """
                
                yo = 'dogg'
                
                @export
                def iheard(self):
                    return "I heard"
                
                @export
                def youlike(self):
                    return "you like"
                
                def unexported(self):
                    return "conditionally exporting things"
                
                export(yo, name='yo')
            
            # Normally we’d just call the class “derived”, rather
            # than “Derived” – in this case we need to differentiate
            # betweeen the name of the defined class and the thing
            # we imported within the same code block (normally they’d
            # be in separate files):
            from clu.app import AnotherDerived as derived
            
            assert type(derived) is AnotherDerived
            assert repr(derived) == "<class-module ‘clu.app.AnotherDerived’ from “clu.app”>"
            assert derived.yo == 'dogg'
            
            assert type(derived.exporter) is Exporter
            assert len(derived.exporter) == len(dir(derived))
            assert derived.exporter.dotpath == derived.qualname
            
            durr = dir(derived)
            assert 'yo' in durr
            assert 'iheard' in durr
            assert 'youlike' in durr
            assert 'unexported' not in durr
            
            for attname in dir(derived):
                assert hasattr(derived, attname)
            
            for attname in DO_NOT_INCLUDE:
                assert attname not in dir(derived)
            
            assert derived.iheard() == 'I heard'
            assert derived.youlike() == 'you like'
            assert derived.unexported() == 'conditionally exporting things'
            
            from clu.app.AnotherDerived import yo, iheard, youlike
            
            assert yo == 'dogg'
            assert iheard() == 'I heard'
            assert youlike() == 'you like'
        
        finally:
            Registry.unregister(derived.appname, derived.qualname)
    
    def test_SubModule_contextmanager_derived_import_statement(self):
        from clu.importing import all_registered_modules
        from clu.importing import SubModule
        
        before = all_registered_modules()
        
        with SubModule('derived_module0', __module__=__name__) as DerivedModule:
            from clu.app import derived_module0 as derived
            
            assert type(derived) is DerivedModule
            assert type(derived.exporter).__name__ == 'Exporter'
            assert len(all_registered_modules()) == len(before) + 1
        
        after = all_registered_modules()
        assert before == after
    
    def test_SubModule_contextmanager_derived_import_importlib(self):
        from clu.importing import all_registered_modules
        from clu.importing import SubModule
        # from clu.predicates import mro
        from clu.typology import subclasscheck
        import importlib
        
        before = all_registered_modules()
        
        with SubModule('derived_module1', __module__=__name__) as DerivedModule:
            derived = importlib.import_module('clu.app.derived_module1')
            
            assert type(derived) is DerivedModule
            assert derived.__class__ is DerivedModule
            assert isinstance(derived, DerivedModule)
            assert subclasscheck(type(derived), DerivedModule)
            
            # print(type(DerivedModule))
            # print(DerivedModule)
            # print(type(derived))
            # pprint(mro(derived))
            
            assert type(derived.exporter).__name__ == 'Exporter'
            assert len(all_registered_modules()) == len(before) + 1
        
        after = all_registered_modules()
        assert before == after
