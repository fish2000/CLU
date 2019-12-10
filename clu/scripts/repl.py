# -*- encoding: utf-8 -*-

"""
repl.py – THE RUBRICK:

1) Import all modules with an exporter, excluding those from a list
    … e.g. equivalent to “import clu.exporting”, etc.

2) Import modules without an exporter, including those from a list
    … e.g. “clu.constants.consts” and friends

3) Export everything from modules from (1) and (2)
   into the global namespace

4) Import additional modules (whether CLU, stdlib, or third-party)
   and just leave the modules themselves hanging out in
   the global namespace

5) Deal with any nitpicks – e.g. “from pprint import pprint”,
   “from clu.testing.utils import pout” and what have you

6) PUSH IT REAL GOOD

7) LOOK ON MY WORK, YE MIGHTY, AND MAYBE BE LIKE “I COULD USE THAT”

"""
from __future__ import print_function

from clu.constants import consts
from clu.all import import_clu_modules
from clu.naming import dotpath_split, qualified_import, qualified_name
from clu.typespace.namespace import Namespace

def star_export(module, namespace=None):
    """ Safely bind everything a module exports to a namespace. """
    if namespace is None:
        return
    for name in dir(module):
        namespace[name] = getattr(module, name)

def module_export(module, namespace=None):
    """ Safely bind a module to a namespace. """
    if namespace is None:
        return
    name = dotpath_split(qualified_name(module))[0]
    namespace[name] = module

modules = import_clu_modules()
namespace = Namespace(**modules)

star_export(consts, namespace=globals())
# star_export(namespace, namespace=globals())

starmods = ('clu.repl',
            'clu.config.defg',
            'clu.dicts', 'clu.enums', 'clu.exporting', 'clu.extending',
            'clu.importing', 'clu.naming', 'clu.predicates', 'clu.typology',
            'clu.fs.filesystem', 'clu.fs.misc')

mods = ('clu.all',
        'clu.config.base',
        'clu.config.env',
        'clu.config.settings',
        'clu.dispatch', 'clu.sanitizer', 'clu.fs.pypath',
        'clu.typespace.types')

for starmod in starmods:
    star_export(qualified_import(starmod), namespace=globals())

for mod in mods:
    module_export(qualified_import(mod), namespace=globals())

# Remove duplicate and invalid sys.paths:
from clu.fs.pypath import remove_invalid_paths
remove_invalid_paths()

# Print the Python banner and/or warnings, messages, and other tripe:
from clu.repl.banners import print_banner
print_banner()
