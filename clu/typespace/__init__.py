# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import re
import sys

from clu.constants import DYNAMIC_MODULE_PREFIX, PROJECT_NAME, VERBOTEN, cache_from_source
from .namespace import SimpleNamespace, Namespace
from clu.exporting import doctrim, path_to_dotpath
from clu.naming import dotpath_join

import types as thetypes
types = Namespace()
typed = re.compile(r"^(?P<typename>\w+)(?:Type)$")

# Fill a Namespace with type aliases, minus the fucking 'Type' suffix --
# We know they are types because they are in the fucking “types” module, OK?
# And those irritating four characters take up too much pointless space, if
# you asked me, which you implicitly did by reading the comments in my code,
# dogg.

for typename in dir(thetypes):
    if typename.endswith('Type'):
        setattr(types, typed.match(typename).group('typename'),
        getattr(thetypes, typename))
    elif typename not in VERBOTEN:
        setattr(types, typename, getattr(thetypes, typename))

# Substitute our own SimpleNamespace class, instead of the provided version:
setattr(types, 'SimpleNamespace', SimpleNamespace)
setattr(types, 'Namespace',       Namespace)

# Manually set `types.__file__` and related attributes:
setattr(types, '__file__',        __file__)
setattr(types, '__cached__',      cache_from_source(__file__))
setattr(types, '__package__',     os.path.splitext(
                                  os.path.basename(__file__))[0])

def modulize(name, namespace, docs=None,
                              path=None):
    """ Convert a dictionary mapping into a legit Python module """
    
    # Ensure a module with the given module name we received
    # doesn’t already exist in `sys.modules`:
    if name in sys.modules:
        raise LookupError("Module “%s” already in sys.modules" % name)
    
    # Update the namespace with '__all__' and '__dir__' if necessary:
    ns_all = None
    
    if '__all__' not in namespace and not hasattr(namespace, '__all__'):
        ns_all = tuple(sorted(namespace.keys()))
        namespace['__all__'] = ns_all
    
    if '__dir__' not in namespace:
        if ns_all is None:
            ns_all = namespace['__all__']
        namespace['__dir__'] = lambda: list(ns_all)
    
    # Check for a __file__ entry in the namespace if we weren’t
    # called with a name:
    if '__file__' in namespace:
        if not path:
            path = namespace.get('__file__', path)
    
    # Construct a trivially namespaced name for the module,
    # based on the given name, the given file path (if any), and
    # some reasonable prefixes:
    if path:
        qualified_name = dotpath_join(DYNAMIC_MODULE_PREFIX,
                                      PROJECT_NAME,
                                      path_to_dotpath(path), name)
        
        # Note that one can use a file path that does not
        # have to necessarily exist on the filesystem in an
        # accessible manner:
        namespace.update({ '__file__' : path,
                         '__cached__' : cache_from_source(path) })
    else:
        qualified_name = dotpath_join(DYNAMIC_MODULE_PREFIX,
                                      PROJECT_NAME,
                                      name)
    
    # Ensure we have a name and a package dotpath in our namespace:
    namespace.update({ '__name__' : name,
                   '__qualname__' : name,
                    '__package__' : qualified_name })
    
    # Construct the module type from the qualified name, using
    # any given docstring text:
    module = types.Module(qualified_name, doctrim(docs))
    
    # Update the module’s `__dict__` with our namespaced mapping
    module.__dict__.update(namespace)
    
    # Update the `sys.modules` mapping with the new module,
    # as required by Python’s internal import machinery --
    # Once `sys.modules` has been thusly updated, the new module
    # can be imported with an “import «name»” statement, as with
    # any other available module:
    sys.modules[name] = module
    
    # Return our new module instance:
    return module

__all__ = ('SimpleNamespace', 'Namespace', 'types', 'modulize')
__dir__ = lambda: list(__all__)