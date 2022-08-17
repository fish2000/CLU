# -*- coding: utf-8 -*-
from __future__ import print_function

import inspect
import sys

from clu.constants import consts
from clu.importing.base import Registry
from clu.importing.base import monomers, linkages, polymers
from clu.importing.base import all_registered_appnames, all_registered_modules, all_registered_appspaces
from clu.importing.base import get_appspace, modules_for_appname, appspaces_for_appname, modules_for_appname_and_appspace
from clu.importing.base import ModuleSpec, LoaderBase, FinderBase
from clu.importing.base import MetaModule, ModuleAlias, ModuleBase, DO_NOT_INCLUDE
from clu.importing.base import installed_appnames, initialize_module
from clu.importing.base import PerApp, PolymerType, initialize_types
from clu.importing.proxy import ProxyModule
from clu.exporting import Exporter

exporter = Exporter(path=__file__)

Module, Finder, Loader = initialize_types(consts.APPNAME)

with exporter as export:
    
    export(Module, name="Module", doc="CLU’s base class for class-modules")
    export(Finder, name="Finder", doc="CLU’s base class for class-module finders")
    export(Loader, name="Loader", doc="CLU’s base class for class-module loaders")

__all__ = ('monomers', 'linkages', 'polymers',
           'all_registered_appnames', 'all_registered_modules', 'all_registered_appspaces',
           'get_appspace', 'modules_for_appname', 'appspaces_for_appname', 'modules_for_appname_and_appspace',
           'ModuleSpec', 'LoaderBase', 'FinderBase',
           'MetaModule', 'ModuleAlias', 'ModuleBase', 'DO_NOT_INCLUDE',
           'installed_appnames', 'initialize_module',
           'Module', 'Finder', 'Loader',
           'PerApp', 'PolymerType', 'initialize_types',
           'ProxyModule',
           'exporter')

def test():
    
    from clu.predicates import mro
    from clu.naming import nameof, dotpath_join, qualified_name
    from clu.exporting import ExporterBase
    
    from clu.testing.utils import inline
    from pprint import pprint, pformat
    from clu.naming import moduleof
    
    @inline.precheck
    def show_python_executable():
        """ Show the Python executable """
        print("PYTHON:", sys.executable)
    
    # @inline.precheck
    def show_module_from_frame():
        """ Use `inspect.currentframe()` to find the parent module """
        parentframe = inspect.currentframe().f_back.f_back.f_back
        parentname = parentframe.f_code.co_name
        module = inspect.getmodule(parentframe)
        print("Frame:", parentframe)
        print("name:", parentname)
        print("module:", module)
        print("module name:", nameof(module))
        print("qualified module name:", qualified_name(module))
        print("module of module:", moduleof(module))
    
    @inline.precheck
    def show_module_fucking_seriously():
        from clu.exporting import thismodule
        module_from = globals().get('exporter', ExporterBase()).dotpath
        print("module from:", module_from)
        print("module():", thismodule())
    
    @inline
    def test_one():
        """ Class-module basics """
        
        m = Module(consts.APPNAME)
        assert m
        assert m.appname == consts.APPNAME
        assert m.appspace == consts.DEFAULT_APPSPACE
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == consts.APPNAME
    
    @inline
    def test_two():
        """ Class-module subtype basics """
        
        class OtherModule(ModuleBase):
            pass
        
        class DerivedModule(Module):
            pass
        
        class DerivedOther(OtherModule):
            pass
        
        o = OtherModule("other")
        d = DerivedModule("derived")
        O = DerivedOther("derived-other")
        
        assert o
        assert d
        assert O
    
    @inline
    def test_three():
        """ Class-module registry basics """
        
        print("all_registered_appnames():")
        pprint(tuple(all_registered_appnames()))
        print()
        
        print("all_registered_modules():")
        pprint(tuple(all_registered_modules()))
        print()
        
        m = Module(consts.APPNAME)
        
        assert len(Registry.monomers) > 0
        assert len(Module.monomers) == 0
        assert not hasattr(m, 'monomers')
        
        assert m.appname == consts.APPNAME
        assert m.appspace == consts.DEFAULT_APPSPACE
        assert m.__name__ == 'clu.app.clu'
        assert nameof(m) == consts.APPNAME
        
        print("mro(m):")
        pprint(mro(m))
        print()
        
    class FindMe(Module):
        pass
    
    @inline
    def test_three_point_five():
        """ System import hooks, specs and finders """
        finder = Finder()
        assert type(finder.loader) is Loader
        assert type(finder) in sys.meta_path
        
        spec0 = finder.find_spec('clu.app.FindMe', [])
        assert spec0.name == 'clu.app.FindMe'
        
        module0 = finder.loader.create_module(spec0)
        assert isinstance(module0, (FindMe, Module))
        
        module1 = finder.loader.create_module(spec0)
        assert isinstance(module1, (FindMe, Module))
        
        spec1 = finder.find_spec('clu.app.FindMe', [])
        assert spec1.name == 'clu.app.FindMe'
        
        # If “FindMe” is defined inline, this next assert fails –
        # not the first time, but one of the 2..100 other times
        # the test function runs:
        registered = Registry.for_qualname('clu.app.FindMe')
        assert registered == FindMe
    
    @inline
    def test_four():
        """ Class-module subclass properties, methods, and exporting """
        
        export = None
        
        class Derived(Module):
            
            """ I heard you like docstrings """
            
            yo = 'dogg'
            
            @export
            def yodogg(self):
                return "I heard you like"
            
            @export
            def nodogg(self):
                return None
            
            export(yo, name='yo')
        
        from clu.app import Derived as derived
        
        assert isinstance(derived, Module)
        assert derived.yo == 'dogg'
        assert derived.yodogg() == "I heard you like"
        assert derived.nodogg() is None
        
        for attname in dir(derived):
            assert hasattr(derived, attname)
        
        print("dir(derived):")
        pprint(dir(derived))
        print()
        
        print("derived.exporter.exports():")
        pprint(derived.exporter.exports())
        print()
        
        assert type(derived.exporter).__name__ == 'Exporter'
    
    @inline
    def test_five():
        """ Polymer-type caching and “initialize_types(…)” checks """
        
        Module0, Finder0, Loader0 = initialize_types(consts.APPNAME)
        
        assert Finder is Finder0
        assert Loader is Loader0
        assert Module is Module0
        assert Finder0.__loader__ is Loader0
        assert isinstance(Module0.__loader__, Loader0)
        assert isinstance(Finder0.loader, Loader0)
        
        Module1, Finder1, Loader1 = initialize_types(consts.APPNAME, appspace='aux')
        
        assert Finder is Finder1
        assert Loader is Loader1
        assert Module is not Module1 # DIFFERENT!!!
        assert Finder1.__loader__ is Loader1
        assert isinstance(Module1.__loader__, Loader1)
        assert isinstance(Finder1.loader, Loader1)
        
        from clu.aux import Module as aux_module # Note how this is the things’ actual name,
                                                 # “Module”, and not just what we called it,
                                                 # «Module1» …ooof.
        
        assert type(aux_module) is Module1
    
    @inline
    def test_five_point_five():
        """ “PerApp” dataclass and module cache check """
        
        for appname in all_registered_appnames():
            
            assert appname in polymers
            assert appname in monomers
            
            per_app = polymers[appname]
            modules = monomers[appname]
            
            for appspace, module_base in per_app.modules.items():
                assert module_base.qualname in modules
                assert module_base.qualname.startswith(dotpath_join(appname, appspace))
            
            for module_info in per_app.finder.iter_modules():
                module_spec = per_app.finder.find_spec(module_info.name, [])
                assert module_info.name in modules
                assert module_spec.name == module_info.name
                assert modules[module_info.name].qualname.startswith(module_spec.origin)
            
            # This will fail unless we try it after the “find_spec(…)” business above:
            for module_base in per_app.modules.values():
                assert module_base.qualname in FinderBase.specs
                assert module_base.qualname in FinderBase.cache
    
    @inline.diagnostic
    def show_spec_cache():
        speccount = len(FinderBase.specs)
        plural = (speccount == 1) and "spec" or "specs"
        
        print(f"SPEC CACHE ({speccount} {plural} total):")
        
        for specname in sorted(FinderBase.specs.keys()):
            spec = FinderBase.specs[specname]
            string = pformat(spec.__dict__, indent=4, width=consts.SEPARATOR_WIDTH)
            cached = getattr(spec, 'cached', None)
            hasloc = getattr(spec, 'has_location', None)
            parent = getattr(spec, 'parent', None)
            print()
            print(f"    «{specname}»")
            print(f"{string}")
            print(f"    +      cached: {cached}")
            print(f"    +has_location: {hasloc}")
            print(f"    +      parent: {parent}")
    
    @inline.diagnostic
    def show_monomers():
        """ Show all registered Module subclasses """
        appnames = tuple(all_registered_appnames())
        appcount = len(appnames)
        plural = (appcount == 1) and "app" or "apps"
        print(f"MONOMERS ({appcount} {plural} total):")
        
        for appname in appnames:
            monos = dict(monomers[appname])
            monocount = len(monos)
            monoplural = (monocount == 1) and "monomer" or "monomers"
            string = pformat(monos, indent=4, width=consts.SEPARATOR_WIDTH)
            print()
            print(f"    «{appname}» ({monocount} {monoplural}):")
            print(f"{string}")
    
    @inline.diagnostic
    def show_linkages():
        """ Show all registered Loader subclasses """
        appnames = tuple(linkages.keys())
        appcount = len(appnames)
        plural = (appcount == 1) and "app" or "apps"
        print(f"LINKAGES ({appcount} {plural} total):")
        
        for appname in appnames:
            LoaderCls = linkages[appname]
            qname = qualified_name(LoaderCls)
            instancedict = dict(LoaderCls.instances)
            instancecount = len(LoaderCls.instances)
            instanceplural = (instancecount == 1) and "instance" or "instances"
            string = pformat(instancedict, indent=4, width=consts.SEPARATOR_WIDTH)
            print()
            print(f"    «{appname}» ({qname}, {instancecount} {instanceplural}):")
            print(f"{string}")
    
    @inline.diagnostic
    def show_polymers():
        """ Show per-app class-module-related subclasses """
        appnames = tuple(all_registered_appnames())
        appcount = len(appnames)
        plural = (appcount == 1) and "app" or "apps"
        print(f"POLYMERS ({appcount} {plural} total):")
        
        for appname in appnames:
            perapp = polymers[appname]
            modcount = len(perapp.modules)
            modplural = (modcount == 1) and "module" or "modules"
            string = pformat(perapp.__dict__, indent=4, width=consts.SEPARATOR_WIDTH)
            print()
            print(f"    «{appname}» ({modcount} {modplural}):")
            print(f"{string}")
    
    # Run all tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())