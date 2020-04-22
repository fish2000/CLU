# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestImporting(object):
    
    """ Run the tests for the “clu.importing” module. """
    
    def test_modulealias(self):
        from clu.importing import ModuleAlias
        from clu.importing import ProxyModule, Module
        
        subscript = ProxyModule[Module]
        
        assert type(subscript) is ModuleAlias
        assert subscript.origin is ProxyModule
        assert subscript.specializer is Module
        assert subscript.__mro_entries__((object,)) == (ProxyModule, Module)
        assert subscript(object) == (ProxyModule, Module) # calls __mro_entries__(…)
        
        assert subscript == ModuleAlias(ProxyModule, Module)
        assert subscript != ModuleAlias(Module, ProxyModule)
        assert not (subscript == None)
        assert subscript != None
        assert hash(subscript) == hash(ModuleAlias(ProxyModule, Module))
        
        reprstring = "ModuleAlias(origin=‘<class-module “ProxyModule”>’, " \
                     "specializer=’<class-module “clu.app.Module”>’)"
        assert repr(subscript).startswith(reprstring)
        
        unspecialized = ProxyModule[None]
        
        assert type(unspecialized) is ModuleAlias
        assert unspecialized.origin is ProxyModule
        assert unspecialized.specializer is None
        assert unspecialized.__mro_entries__((object,)) == (ProxyModule,)
        assert unspecialized(object) == (ProxyModule,) # calls __mro_entries__(…)
        
        assert unspecialized == ModuleAlias(ProxyModule, None)
        assert unspecialized != ModuleAlias(Module, None)
        assert not (unspecialized == None)
        assert unspecialized != None
        
        reprstring = "ModuleAlias(origin=‘<class-module “ProxyModule”>’, " \
                     "specializer=’None’)"
        assert repr(unspecialized).startswith(reprstring)
        
        with pytest.raises(TypeError) as exc:
            ModuleAlias(None, None)
        assert "Specialization requires a Module type" in str(exc.value)
        
        with pytest.raises(TypeError) as exc:
            ModuleAlias(Module, 'wat')
        assert "Specialization requires a Module type" in str(exc.value)
    
    def test_modulealias_respecialization_reprs(self):
        from clu.importing import ModuleAlias, ModuleBase, Module
        
        reprstring = "<class “clu.importing.ModuleAlias”>"
        
        assert repr(ModuleAlias) == reprstring
        
        reprstring = "ModuleAlias(origin=‘<class-module “ModuleBase”>’, " \
                     "specializer=’<class-module “clu.app.Module”>’) @ 0x"
        
        assert repr(ModuleBase[Module]).startswith(reprstring)
        assert repr(ModuleBase[Module][Module]).startswith(reprstring)
        assert repr(ModuleAlias[ModuleBase, Module]).startswith(reprstring)
        assert repr(ModuleAlias(ModuleBase, Module)).startswith(reprstring)
        assert repr(ModuleAlias[ModuleBase][Module]).startswith(reprstring)
        assert repr(ModuleAlias[ModuleBase, None][Module]).startswith(reprstring)
        assert repr(ModuleAlias(ModuleBase, None)[Module]).startswith(reprstring)
        
        reprstring = "ModuleAlias(origin=‘<class-module “clu.app.Module”>’, " \
                     "specializer=’None’) @ 0x"
        
        assert repr(Module[None]).startswith(reprstring)
        assert repr(ModuleAlias[Module]).startswith(reprstring)
        assert repr(ModuleAlias[Module, None]).startswith(reprstring)
        assert repr(ModuleAlias(Module, None)).startswith(reprstring)
        assert repr(ModuleAlias[Module, None][None]).startswith(reprstring)
        assert repr(ModuleAlias(Module, None)[None]).startswith(reprstring)
        
        with pytest.raises(TypeError) as exc:
            assert repr(ModuleAlias[None, None]).startswith(reprstring)
        assert "Specialization requires a Module type" in str(exc.value)
        
        with pytest.raises(TypeError) as exc:
            assert repr(ModuleAlias[None][Module, None]).startswith(reprstring)
        assert "Specialization requires a Module type" in str(exc.value)
    
    def test_proxy_module_for_reals(self, consts):
        from clu.importing import ProxyModule, Module, Registry
        
        overrides = dict(APPNAME='yodogg',
                         PROJECT_PATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg/yodogg',
                         BASEPATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg')
        
        try:
            
            class testing1_overridden_consts(ProxyModule[Module]):
                targets = (overrides, consts)
            
            from clu.app import testing1_overridden_consts as overridden
            
            assert overridden.USER == consts.USER
            assert overridden.BUILTINS == consts.BUILTINS
            assert overridden.APPNAME == 'yodogg'
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
        
        overrides = dict(APPNAME='yodogg',
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
                targets = (overrides, consts)
            
            from clu.app import testing0_overridden_consts as overridden
            
            assert overridden.USER == consts.USER
            assert overridden.BUILTINS == consts.BUILTINS
            assert overridden.APPNAME == 'yodogg'
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
    
    def test_module_export_within_execute(self, consts):
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
                    assert cls.appname == consts.APPNAME
                    assert cls.appspace == consts.DEFAULT_APPSPACE
                    assert cls.name == 'DerivedWithExecute'
                    assert cls.prefix == f'{consts.APPNAME}.{consts.DEFAULT_APPSPACE}'
                    assert cls.qualname == f'{consts.APPNAME}.{consts.DEFAULT_APPSPACE}.DerivedWithExecute'
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
            
            assert hasattr(derived, consts.EXPORTER_NAME)
            
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
        
        m = Module(consts.APPNAME)
        assert m
        assert m.appname == consts.APPNAME
        assert m.appspace == consts.DEFAULT_APPSPACE
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == consts.APPNAME
        
        assert len(Registry.monomers) > 0   # full registry dict-of-dicts
        assert len(Module.monomers) == 0    # dummy class property, empty dict
        assert not hasattr(m, 'monomers')   # no instance property available
    
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
    
    def test_polymertype_cache_methods(self, consts):
        from clu.importing import Finder, Loader, Module
        from clu.importing import ModuleBase, PolymerType
        from clu.importing import initialize_new_types
        from clu.typology import iterlen
        from clu.exporting import thismodule
        
        polymers = PolymerType()
        
        polymers.store(consts.APPNAME,    loader=Loader,
                                          finder=Finder,
                   **{ consts.DEFAULT_APPSPACE : Module }) # key: appspace,
                                                           # value: module class
        
        # Check that lengths are 1:
        assert len(polymers) == 1
        assert len(polymers[consts.APPNAME].modules) == 1
        assert iterlen(polymers.all_appspaces()) == 1
        
        # Check get_finder(…) and get_loader(…)
        assert polymers.get_finder(consts.APPNAME) is Finder
        assert polymers.get_loader(consts.APPNAME) is Loader
        
        # Check error conditions for get_finder(…) and get_loader(…)
        with pytest.raises(ValueError) as exc:
            polymers.get_finder('WTF')
        assert "no PerApp instance" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            polymers.get_loader('WTF')
        assert "no PerApp instance" in str(exc.value)
        
        new_appspace = 'new'
        
        NewModule, NewFinder, NewLoader = initialize_new_types(consts.APPNAME,
                                                               appspace=new_appspace,
                                                               module=thismodule())
        
        # polymers.store(consts.APPNAME, loader=NewLoader,
        #                                finder=NewFinder,
        #                    **{ new_appspace : NewModule })
        polymers.add_module(NewModule,
                            appname=consts.APPNAME,
                            appspace=new_appspace)
        
        # Check that some lengths have increaced:
        assert len(polymers) == 1
        assert len(polymers[consts.APPNAME].modules) == 2
        assert iterlen(polymers.all_appspaces()) == 2
        
        # Check error conditions for add_module(…)
        with pytest.raises(ValueError) as exc:
            polymers.add_module(NewModule,
                                appname=consts.APPNAME,
                                appspace=None)
        assert "an appspace is required" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            polymers.add_module(None,
                                appname=consts.APPNAME,
                                appspace=new_appspace)
        assert "a module is required" in str(exc.value)
        
        with pytest.raises(ValueError) as exc:
            polymers.add_module(NewModule,
                                appname='WTF',
                                appspace=new_appspace)
        assert "no PerApp instance" in str(exc.value)
        
        with pytest.raises(NameError) as exc:
            polymers.add_module(NewModule,
                                appname=consts.APPNAME,
                                appspace=new_appspace)
        assert "module already exists in" in str(exc.value)
        
        perapp = polymers[consts.APPNAME]
        
        assert perapp.appname == consts.APPNAME
        assert iterlen(perapp.appspaces()) == 2
        assert perapp.loader is Loader
        assert perapp.finder is Finder
        assert perapp.modules[consts.DEFAULT_APPSPACE] is Module
        assert perapp.modules[new_appspace] is NewModule
        assert all(issubclass(m, ModuleBase) for m in perapp.modules.values())
    
    def test_installed_appnames(self, consts):
        from clu.importing import installed_appnames
        assert consts.APPNAME in installed_appnames()
    
    @pytest.mark.TODO
    def test_curiously_recurring_modulebase_subtypes(self, consts):
        # TODO: add method-inheritance resolution checks
        from clu.importing import Finder, Loader, Module
        from clu.importing import ModuleBase
        from clu.importing import initialize_module
        modulename = "tests.test_importing"
        
        class TemplatedType(ModuleBase):
            __module__ = modulename
        
        AuxModule = initialize_module(consts.APPNAME,
                                      appspace='aux',
                                      module=modulename)
        
        class application_t(TemplatedType[Module]):
            __module__ = modulename
        
        class auxilliary_t(TemplatedType[AuxModule]):
            __module__ = modulename
        
        from clu.app import application_t as application
        from clu.aux import auxilliary_t as auxilliary
        
        assert isinstance(application, TemplatedType)
        assert isinstance(auxilliary,  TemplatedType)
        assert isinstance(application, Module)
        assert isinstance(auxilliary,  AuxModule)
        
        assert application.appname  == consts.APPNAME
        assert auxilliary.appname   == consts.APPNAME
        assert application.appspace == consts.DEFAULT_APPSPACE
        assert auxilliary.appspace  == 'aux'
        
        from clu.predicates import attr_across, pyattr_across
        
        assert pyattr_across('module', Module, Finder, Loader) == ('clu.importing', 'clu.importing', 'clu.importing')
        
        # names = pyattr_across('module', application,
        #                                 application_t,
        #                                 auxilliary,
        #                                 auxilliary_t)
        
        # assert len(names) == 4
        
        names = attr_across('__module__', application,
                                          application_t,
                                          auxilliary,
                                          auxilliary_t)
        
        assert names == (modulename,) * 4
        assert len(frozenset(names)) == 1
        assert set(names).pop() == modulename
        
        assert application.__module__ == modulename
        assert application_t.__module__ == modulename
        assert auxilliary.__module__ == modulename
        assert auxilliary_t.__module__ == modulename
    
    def test_finder_and_loader_methods(self):
        from clu.importing import Registry, ModuleSpec
        from clu.importing import Finder, Loader, Module
        import importlib.machinery
        import sys
        
        # FinderBase subclasses created with a call to
        # “initialize_types(…)” will furnish references
        # to the LoaderBase subclass of the same appname,
        # and are registered with “sys.meta_path”:
        assert Finder.__loader__ is Loader
        assert type(Finder.loader) is Loader
        assert Finder in sys.meta_path
        
        # Finder instances are practically the same
        # as specific FinderBase subclasses, in terms
        # of their utility – their properties and methods
        # are largely identical:
        finder = Finder()
        assert finder.__loader__ is Loader
        assert type(finder.loader) is Loader
        assert type(finder) in sys.meta_path
        
        class findme(Module):
            pass
        
        # “finder.find_spec(…)” returns our bespoke subclass
        # of importlib.machinery.ModuleSpec:
        spec = finder.find_spec('clu.app.findme', [])
        assert spec.name == 'clu.app.findme'
        assert type(spec) is ModuleSpec
        assert isinstance(spec,       importlib.machinery.ModuleSpec)
        assert issubclass(ModuleSpec, importlib.machinery.ModuleSpec)
        
        # Calling “loader.create_module(spec)” followed by
        # “loader.exec_module(module)” follows the codepath
        # used when importing via an import statement:
        module = finder.loader.create_module(spec)
        finder.loader.exec_module(module)
        assert getattr(module, '_executed', False)
        assert type(module) is findme
        assert repr(module) == "<class-module ‘clu.app.findme’>"
        
        # Registry lookup returns the Module subclass, as written:
        registered = Registry.for_qualname('clu.app.findme')
        assert registered == findme
        assert issubclass(findme, Module)
        assert issubclass(registered, Module)
        
        # Importing the subclass instances the class-module:
        from clu.app import findme as found
        assert isinstance(found, findme)
        assert isinstance(found, Module)
    
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
        basepath = dirname.subdirectory('yodogg')
        assert basepath.exists
        pypath.enhance(basepath)
        
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
    
    def test_derived_import_with_export(self, consts):
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
            
            assert hasattr(derived, consts.EXPORTER_NAME)
            
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
