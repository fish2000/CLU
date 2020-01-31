# -*- coding: utf-8 -*-
from __future__ import print_function
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def import_all_modules(basepath, appname, exportername='exporter'):
    """ Import all modules that use the “clu.exporting.ExporterBase”
        mechanism for listing and exporting their module contents,
        for a given «basepath», «appname», and «exportername» – where:
        
            • “basepath” is the root path of a Python package;
            • “appname” is a valid module name within «basepath»; and
            • “exportername” is the name of the “Exporter” instances.
    """
    from clu.fs.filesystem import Directory
    from clu.exporting import ExporterBase
    from clu.importing import modules_for_appname
    from clu.predicates import resolve
    from importlib import import_module
    from itertools import chain
    
    modules = {}
    importables = Directory(basepath).importables(appname)
    cls_modules = (clsmod.qualname for clsmod in modules_for_appname(appname))
    
    # Only include those modules whose exporter instance is
    # a subclass of “clu.exporting.ExporterBase” named as
    # “exportername” indicates, within the module in question:
    for modname in chain(importables, cls_modules):
        module = import_module(modname)
        exporter = resolve(module, exportername)
        if isinstance(exporter, ExporterBase):
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
                               appname=consts.APPNAME,
                          exportername=consts.EXPORTER_NAME)

code_attrs = tuple(f'__code__.co_{attname}' for attname in ('cellvars',
                                                            'names',
                                                            'varnames'))

@export
def clu_inline_tests():
    """ Generator over all CLU modules that contain inline tests """
    # Use “resolve(…)” and “attrs(…)” for nested attribute access:
    from clu.predicates import resolve, attrs
    
    # Find and yield all CLU modules defining inline test functions:
    for dotpath, module in import_clu_modules().items():
        test_fn = resolve(module, 'test')
        if callable(test_fn):
            names = attrs(test_fn, *code_attrs)
            if any('inline' in name for name in names):
                yield dotpath

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()