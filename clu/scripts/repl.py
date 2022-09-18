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

import importlib

from clu.all import import_clu_modules
from clu.naming import nameof, qualified_import
from clu.predicates import ispublic

# MODULE EXPORT FUNCTIONS: given a module name, export
# either the module or its contents into a given namespace:

def star_export(modulename, namespace):
    """ Safely bind everything a module exports to a namespace. """
    try:
        module = qualified_import(modulename)
    except ValueError:
        module = importlib.import_module(modulename)
    for name in dir(module):
        if ispublic(name):
            namespace[name] = getattr(module, name)

def module_export(modulename, namespace):
    """ Safely bind a module to a namespace. """
    try:
        module = qualified_import(modulename)
    except ValueError:
        module = importlib.import_module(modulename)
    name = nameof(module)
    namespace[modulename] = namespace[name] = module

# Warm up sys.modules and friends:

import_clu_modules()

# Set up the GLOBAL namespace and the __all__ tuple:

__all__ = tuple()
GLOBALS = globals()

starmods = ('clu.repl.ansi',
            'clu.repl.columnize',
            'clu.repl.modules',
            'clu.constants.enums',
            'clu.constants.data',
            'clu.application',
            'clu.config.abc',
            'clu.config.env',
            'clu.config.keymap',
            'clu.config.proxy',
            'clu.dicts', 'clu.enums', 'clu.exporting', 'clu.extending', 'clu.shelving.redat',
            'clu.importing', 'clu.mathematics', 'clu.naming', 'clu.predicates', 'clu.typology',
            'clu.fs.abc', 'clu.fs.filesystem', 'clu.fs.misc', 'clu.repr', 'clu.scripts.treeline', 'clu.stdio',
            'clu.typespace.namespace',
            'clu.testing.utils',
            'clu.version', 'clu.version.git_version')

mods = ('clu',
        'clu.all',
        'clu.abstract',
        'clu.constants.consts',
        'clu.constants.polyfills',
        'clu.config.base',
        'clu.config.codecs',
        'clu.config.settings',
        'clu.config.ns',
        'clu.csv',
        'clu.fs.appdirectories',
        'clu.keyvalue',
        'clu.dispatch', 'clu.sanitizer', 'clu.fs.pypath',
        'clu.scripts.ansicolors',
        'clu.scripts.treeline',
        'clu.typespace.types', # not technically a module!
        'sys', 'os', 'io', 're', 'abc',
        'argparse', 'collections', 'contextlib', 'copy',
        'datetime', 'functools', 'importlib', 'inspect',
        'itertools', 'math', 'operator', 'pickle', 'six',
        'shutil', 'sysconfig', 'weakref',
        'numpy', 'more_itertools', 'colorama', 'termcolor',
        'xerox', 'zict', 'pytz', 'dateutil',
        'termplotlib', 'termtables')

# “Star-import” all starmods – this is equivalent to doing:
# 
#    from <starmod> import *
# 
# … for each <starmod> module name…

for starmod in starmods:
    star_export(starmod, namespace=GLOBALS)

# Import all modules in “mods” – this is equivalent to doing:
# 
#    qualified_import(<mod>)
# 
# … for each <mod> module name; q.v. “qualified_import(…)”
# function definition supra.

for mod in mods:
    module_export(mod, namespace=GLOBALS)

# Additionals and corner-cases – imports requiring their own
# bespoke import-statement forms:

import collections.abc
from PIL import Image
from pprint import pprint, pformat

ppt = lambda thing: pprint(tuple(thing))

# These two imports trigger module-level __getattr__ actions:

from clu.testing.utils import pout, inline

# Not quite sure where to put this, for now:

_explain = lambda thing=None: print(columnize(dir(thing),
                                    display_width=consts.SEPARATOR_WIDTH,
                                            ljust=True))

def explain(thing, width=None):
    """ Print the “dir(…)” results of something, nicely columnized """
    display_width = width or consts.SEPARATOR_WIDTH
    
    typename = nameof(type(thing)).capitalize()
    thingname = nameof(thing, "¡unknown!")
    subthings = dir(thing)
    subcount = len(subthings)
    
    contents = f"» {typename} instance «{thingname}» "
    if subcount == 0:
        contents += "contains no “dir(…)” results"
        print(contents)
        return
    elif subcount == 1:
        contents += "contains one sub-thing"
        print(contents)
    else:
        contents += f"contains {subcount} sub-things"
        print(contents)
    
    # print_ansi_centered()
    print('—' * display_width)
    print()
    
    print(columnize(subthings,
          display_width=display_width,
                  ljust=True))

try:
    from instakit.utils.static import asset
except (ImportError, SyntaxError, TypeError): # pragma: no cover
    pass
else:
    # Extend `__all__`:
    __all__ += ('asset', 'image_paths', 'catimage')
    # Prepare a list of readily open-able image file paths:
    image_paths = list(map(
        lambda image_file: asset.path('img', image_file),
            asset.listfiles('img')))
    # I do this practically every time, so I might as well do it here:
    catimage = Image.open(image_paths[0])

# Remove duplicate and invalid sys.paths:

pypath.remove_invalid_paths()

# Print the Python banner and/or warnings, messages, and other tripe:

if __name__ == '__main__':
    # In theory, this will *not* run when repl.py
    # is loaded into a REPL using a “-i” flag:
    if consts.IPYTHON or consts.BPYTHON:
        print()
    else:
        print(__doc__)

from clu.repl.banners import print_banner
print()
print_banner()
print()
