# -*- coding: utf-8 -*-
from __future__ import print_function
from dataclasses import dataclass, field, fields

reprless = dataclass(repr=False)

import sys
import typing as tx

from clu.repr import stringify
from clu.importing import (FinderBase,
                           LoaderBase,
                           ModuleBase)

from clu.importing import MetaModule
from clu.extending import Extensible
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@reprless
class PerApp:
    
    loader:  Extensible
    finder:  Extensible
    modules: tx.Mapping[str, MetaModule] = field(default_factory=dict)
    appname: str                         = field(default_factory=str)
    
    def __repr__(self):
        return stringify(self,
                    type(self).fields,
                         try_callables=False)

PerApp.fields = tuple(field.name for field in fields(PerApp))

class PolymerType(dict):
    
    def store(self, appname, loader, finder, **modules):
        self[appname] = PerApp(loader=loader,
                               finder=finder,
                              modules=modules,
                              appname=appname)
        return self[appname]
    
    def add_module(self, appname, appspace, module):
        if not appspace:
            raise ValueError("an appspace is required")
        if not module:
            raise ValueError("a module is required")
        if not self.get(appname, None):
            raise ValueError(f"no PerApp instance for appname: {appname}")
        self[appname].modules.update({ appspace : module })
        return self[appname]

polymers = PolymerType()

def installed_appnames():
    """ Return a set of the appnames for all installed finders
        that have one defined.
    """
    appnames = set()
    for finder in sys.meta_path:
        if hasattr(finder, 'appname'):
            appnames.add(finder.appname)
    return appnames

def initialize_module(appname, appspace, loader):
    """ Private helper for “initialize_types(…)” """
    
    class Module(ModuleBase, appname=appname,
                             appspace=appspace):
        __loader__ = loader
    
    return Module

def initialize_new_types(appname, appspace):
    """ Private helper for “initialize_types(…)” """
    
    class Loader(LoaderBase, appname=appname):
        pass
    
    class Finder(FinderBase, appname=appname):
        __loader__ = Loader
        loader = Loader()
    
    Module = initialize_module(appname,
                               appspace,
                               Finder.loader)
    
    return Module, Finder, Loader

@export
def initialize_types(appname, appspace='app'):
    """ Initialize subtypes of FinderBase, LoaderBase, and ModuleBase,
        configured for a specific “appname” and “appspace” (the latter
        of which defaults to ‘app’).
        
        You use ‘initialize_types(…)’ in one of your own app’s modules
        like so:
        
            Module, Finder, Loader = initialize_types('myappname')
        
        … if you insert that line of code in a module of yours called,
        say, “myappname/modules.py” you could then either a) proceed
        to subclass Module to create your class-modules, or b) import
        the ‘Module’ class from elsewhere and subclass it subsequently.
    """
    try:
        perapp = polymers[appname]
    
    except KeyError:
        Module, Finder, Loader = initialize_new_types(appname, appspace)
        polymers.store(appname, loader=Loader,
                                finder=Finder,
                        **{ appspace : Module })
    
    else:
        Loader = perapp.loader
        Finder = perapp.finder
        Module = perapp.modules.get(appspace, None)
        
        if Module is None:
            Module = initialize_module(appname, appspace, perapp.finder.loader)
            polymers.add_module(appname=appname,
                               appspace=appspace,
                                 module=Module)
    
    if appname not in installed_appnames():
        sys.meta_path.append(Finder)
    
    return Module, Finder, Loader

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
