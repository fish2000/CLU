# -*- coding: utf-8 -*-
from __future__ import print_function
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

typename = lambda thing: type(thing).__name__

@export
def import_all_modules(basepath, appname):
    """ Import all modules that use the “clu.exporting.Exporter”
        mechanism for listing and exporting their module contents,
        for a given «basepath» and «appname», where:
        
            • “basepath” is the root path of a Python package, and
            • “appname” is a valid module name within «basepath»
    """
    from clu.fs.filesystem import Directory
    from clu.importing import modules_for_appname
    from clu.predicates import or_none
    from importlib import import_module
    from itertools import chain
    
    modules = {}
    importables = Directory(basepath).importables(appname)
    cls_modules = (clsmod.qualname for clsmod in modules_for_appname(appname))
    
    # Only include modules whose “exporter” entry is an instance
    # of a subclass of “clu.exporting.ExporterBase” whose class
    # name is ‘Exporter’:
    for modname in chain(importables, cls_modules):
        module = import_module(modname)
        if typename(or_none(module, 'exporter')) == 'Exporter':
            modules[modname] = module
    
    return modules

@export
def import_clu_modules():
    """ Import all CLU modules that use the “clu.exporting.Exporter”
        mechanism for listing and exporting their module contents
    """
    # Convenience function: calls “clu.all.import_all_modules(…)”
    # with «basepath=clu.constants.consts.BASEPATH»,
    # and «appname=clu.constants.consts.PROJECT_NAME»
    from clu.constants import consts
    return import_all_modules(basepath=consts.BASEPATH,
                               appname=consts.PROJECT_NAME)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()