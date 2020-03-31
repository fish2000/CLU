# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

from clu.predicates import newtype, mro, allattrs, attr_search
from clu.typespace import types
from clu.importing import (ModuleBase,
                           MetaModule,
                           installed_appnames)

from clu.constants import consts
from clu.exporting import Exporter

# save some typographic room:
sns = types.SimpleNamespace

exporter = Exporter(path=__file__)
export = exporter.decorator()

class AppMeta(MetaModule):
    
    @property
    def exportercls(cls):
        from clu.exporting import Registry
        if Registry.has_appname(cls.appname):
            return Registry[cls.appname]
        raise TypeError(f"exporter class not found for appname: {cls.appname}")

@export
class AppBase(ModuleBase, metaclass=AppMeta):
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        # 1) Process default class keywords:
        if 'appspace' not in kwargs:
            kwargs['appspace'] = consts.DEFAULT_APPSPACE
        basepath = kwargs.pop('basepath', None)
        cls.basepath = basepath or attr_search('basepath', *mro(cls))
        
        # 2) Call up:
        super(AppBase, cls).__init_subclass__(**kwargs)
        
        # 3) Check appname:
        if not cls.appname:
            raise NameError("no appname available on AppBase subclass")
        
        # 4) install finder, loader, exporter…
        cls.environ    = cls.initialize_environ()
        cls._exporter  = cls.initialize_exporter()
        Finder, Loader = cls.initialize_finder_and_loader()
        cls.finder     = Finder
        cls.loader     = Loader
        cls.__loader__ = Finder.loader
        
        # 5) possibly update `sys.meta_path`
        if cls.appname not in installed_appnames():
            sys.meta_path.append(cls.finder)
    
    @classmethod
    def initialize_finder_and_loader(cls):
        # name, *bases, metaclass, attributes, **keywords
        from clu.importing import FinderBase, LoaderBase
        
        if allattrs(cls, 'finder', 'loader'):
            return cls.finder, cls.loader
        
        LoaderCls = newtype('Loader', LoaderBase, appname=cls.appname)
        FinderCls = newtype('Finder', FinderBase, appname=cls.appname)
        return FinderCls, LoaderCls
    
    @classmethod
    def initialize_exporter(cls):
        from clu.exporting import ExporterBase
        
        try:
            return cls.exportercls
        except TypeError:
            ExporterCls = newtype('Exporter', ExporterBase, appname=cls.appname,
                                                            basepath=cls.basepath)
            return ExporterCls
    
    @classmethod
    def initialize_environ(cls):
        from clu.config.env import Environ
        
        if hasattr(cls, 'environ'):
            return cls.environ
        
        return Environ(appname=cls.appname)

@export
class Application(AppBase, appname=consts.APPNAME,
                          basepath=consts.BASEPATH,
                          appspace=consts.DEFAULT_APPSPACE):
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline, pout
    
    @inline
    def test_one():
        """ Instance the base Application class """
        # First, instance it normally:
        test_app = Application('test_app', doc="Test Application Instance")
        
        assert test_app
        assert test_app._exporter is Exporter
        assert test_app.appname == consts.APPNAME
        assert test_app.appspace == consts.DEFAULT_APPSPACE
        
        # Scond, instance it via import hook:
        from clu.app import Application as app
        
        assert app
        assert app._exporter is Exporter
        assert app.appname == consts.APPNAME
        assert app.appspace == consts.DEFAULT_APPSPACE
    
    @inline
    def test_two():
        """ Subclass and instance a second AppBase subclass """
        
        class Shmapplication(AppBase, appname='flynn'):
            pass
        
        # First, instance it normally:
        shmapp = Shmapplication('test_subclass', doc="Test Secondary Subclass")
        
        assert shmapp
        assert shmapp.appname == 'flynn'
        assert shmapp.appspace == consts.DEFAULT_APPSPACE
        
        # Scond, instance it via import hook:
        from flynn.app import Shmapplication as shmodule
        
        assert shmodule
        assert shmodule.appname == 'flynn'
        assert shmodule.appspace == consts.DEFAULT_APPSPACE
    
    # @inline.diagnostic
    def show_app_class_attribs():
        pout.v(Application)
        
        stuff = dir(Application)
        pout.v({ k : getattr(Application, k) for k in stuff })
        
        print("APPNAME:", Application.appname)
        print("APPSPACE:", Application.appspace)
        
        print("consts.APPNAME:", consts.APPNAME)
        print("consts.DEFAULT_APPSPACE:", consts.DEFAULT_APPSPACE)
    
    @inline.diagnostic
    def show_spec_cache():
        from clu.importing import FinderBase
        from pprint import pformat
        
        speccount = len(FinderBase.specs)
        plural = (speccount == 1) and "spec" or "specs"
        
        print(f"SPEC CACHE ({speccount} {plural} total):")
        
        for specname in sorted(FinderBase.specs.keys()):
            spec = FinderBase.specs[specname]
            string = pformat(spec.__dict__, indent=4)
            cached = getattr(spec, 'cached', None)
            hasloc = getattr(spec, 'has_location', None)
            parent = getattr(spec, 'parent', None)
            print()
            print(f"    «{specname}»")
            print(f"{string}")
            print(f"    +      cached: {cached}")
            print(f"    +has_location: {hasloc}")
            print(f"    +      parent: {parent}")
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())


