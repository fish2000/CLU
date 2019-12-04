# -*- encoding: utf-8 -*-
from __future__ import print_function

def star_export(module, namespace=None):
    """ Safely bind everything a module exports to a namespace. """
    if namespace is None:
        return
    for name in dir(module):
        namespace[name] = getattr(module, name)

from clu.constants import consts
from clu.all import import_clu_modules
from clu.naming import dotpath_split, qualified_import
from clu.typespace.namespace import Namespace

modules = import_clu_modules()
namespace = Namespace(**modules)

star_export(consts, namespace=globals())
# star_export(namespace, namespace=globals())

starmods = ('clu.dicts', 'clu.enums', 'clu.exporting', 'clu.extending',
            'clu.importing', 'clu.naming', 'clu.predicates', 'clu.typology')

mods = ('clu.all', 'clu.dispatch', 'clu.sanitizer')

for starmod in starmods:
    star_export(qualified_import(starmod), namespace=globals())

for mod in mods:
    module = qualified_import(mod)
    name = dotpath_split(mod)[0]
    globals()[name] = module

# Set up some “example” instances –
# I frequently create trivial lists, strings, tuples etc.,
# to be used as exemplars from which I can check methods and
# suchlike using the interactive interpreter:
b = b'yo dogg'
B = bytearray(b)
m = memoryview(b)
c = complex(0, 1)
d = { 'yo' : "dogg" }
t = ('yo', 'dogg')
l = ['yo', 'dogg']
S = { 'yo', 'dogg' }
F = frozenset(S)
f = 0.666
i = 666
o = object()
s = 'yo dogg'

# Remove duplicate and invalid sys.paths:
from clu.fs.pypath import remove_invalid_paths
remove_invalid_paths()

# Print the Python banner and/or warnings, messages, and other tripe:
from clu.repl.banners import print_banner
print_banner()
