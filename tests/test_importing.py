# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestImporting(object):
    
    def test_proxy_module_for_reals(self, consts):
        from clu.importing import ProxyModule, Registry
        
        overrides = dict(PROJECT_NAME='yodogg',
                         PROJECT_PATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg/yodogg',
                         BASEPATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg')
        
        try:
            
            class testing1_overridden_consts(ProxyModule):
                targets = (overrides, consts)
            
            from clu.app import testing1_overridden_consts as overridden
            
            assert overridden.USER == consts.USER
            assert overridden.BUILTINS == consts.BUILTINS
            assert overridden.PROJECT_NAME == 'yodogg'
            assert overridden.PROJECT_PATH.endswith('yodogg')
            assert overridden.BASEPATH.endswith('yodogg')
            
            assert not hasattr(overridden, 'targets')
            assert not hasattr(overridden, 'target_dicts')
            assert hasattr(overridden, '_targets')
            
            with pytest.raises(AttributeError) as exc:
                assert overridden.YODOGG
            assert "access failure" in str(exc.value)
            
            with pytest.raises(AttributeError) as exc:
                assert overridden.add_targets
            assert "access failure" in str(exc.value)
        
        finally:
            Registry.unregister(overridden.appname,
                                overridden.qualname)
    
    def test_module_dict_proxy_idea(self, consts):
        from clu.dicts import ChainMap
        from clu.importing import Module, Registry
        from clu.typology import ismodule, ismapping
        
        overrides = dict(PROJECT_NAME='yodogg',
                         PROJECT_PATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg/yodogg',
                         BASEPATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg')
        
        try:
            
            class PutativeProxyModule(Module):
                
                def __init__(self, name, *targets, doc=None):
                    """ Initialize a proxy-module instance.
                        
                        The signature for initializing a proxy module is the same
                        as that for a class-based module – the proxy module class
                        derives directly from the application-specific class-based
                        module definition – with the optional addition of zero-to-N
                        “targets”.
                        
                        Each target so named can be either a mapping-ish type, or a
                        module. The proxy module will then use the list of targets
                        – considerate of order – to construct a “clu.dicts.ChainMap”
                        instance that pulls, in turn, from the target list.
                        
                        Attribute lookup on the proxy module instance will follow
                        along through the “ChainMap” instances’ internal stack of
                        mappings.
                    """
                    # Establish a base list of target dicts, and call up:
                    self.target_dicts = []
                    super(PutativeProxyModule, self).__init__(name, doc=doc)
                    
                    # Define inline target-processing function:
                    def add_targets(self, *targets):
                        """ Inline use-twice-and-destroy function for processing targets """
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
                    
                    # Process any targets with which this instance
                    # may have been constructed:
                    add_targets(self, *targets)
                    
                    # Process and strip off class-level “targets” 
                    # list attribute, if it exists:
                    cls = type(self)
                    if hasattr(cls, 'targets'):
                        add_targets(self, *cls.targets)
                        del cls.targets
                
                def __execute__(self):
                    # Create the internal ChainMap instance:
                    self.__proxies__ = ChainMap(*self.target_dicts)
                    
                    # Call up:
                    super().__execute__()
                    
                    # Further unclutter the module namespace:
                    del self.target_dicts
                
                def __getattr__(self, key):
                    # N.B. AttributeError typenames (herein “PutativeProxyModule”)
                    # must be hardcoded – using “self.name” leads to an infinite
                    # recursion kertwang within “__getattr__(…)” – since “name”
                    # is a property that uses “nameof(self)” which invariably will
                    # attempt to get one or another nonexistant attributes from ‘self’.
                    try:
                        if not self.__dict__.get('_executed', False):
                            raise KeyError(key)
                        return self.__proxies__[key]
                    except KeyError:
                        typename = type(self).__name__
                        raise AttributeError(f"‘{typename}’ proxy module has no attribute ‘{key}’")
            
            class testing0_overridden_consts(PutativeProxyModule):
                # def __execute__(self):
                #     self.add_targets(overrides, consts)
                #     super().__execute__()
                targets = (overrides, consts)
            
            from clu.app import testing0_overridden_consts as overridden
            
            assert overridden.USER == consts.USER
            assert overridden.BUILTINS == consts.BUILTINS
            assert overridden.PROJECT_NAME == 'yodogg'
            assert overridden.PROJECT_PATH.endswith('yodogg')
            assert overridden.BASEPATH.endswith('yodogg')
            
            assert not hasattr(overridden, 'targets')
            assert not hasattr(overridden, 'target_dicts')
            
            with pytest.raises(AttributeError) as exc:
                assert overridden.YODOGG
            assert "has no attribute" in str(exc.value)
            
            with pytest.raises(AttributeError) as exc:
                assert overridden.add_targets
            assert "has no attribute" in str(exc.value)
        
        finally:
            for clsmod in (PutativeProxyModule,
                           testing0_overridden_consts):
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
        
        m = Module(consts.PROJECT_NAME)
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
        
        o = MyOtherModule("other")
        d = MyDerivedModule("derived")
        O = MyDerivedOther("derived-other")
        
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
        
        o = ThisOtherModule("other")
        d = ThisDerivedModule("derived")
        O = ThisDerivedOther("derived-other")
        
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
