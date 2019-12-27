# -*- coding: utf-8 -*-
from __future__ import print_function

import array
import collections
import collections.abc
import weakref
import re

from clu.constants.consts import (BASEPATH,
                                  DYNAMIC_MODULE_PREFIX,
                                  PROJECT_NAME, VERBOTEN)

from clu.constants.polyfills import cache_from_source
from clu.typespace.namespace import SimpleNamespace, Namespace
from clu.exporting import Exporter, path_to_dotpath

exporter = Exporter(path=__file__)
export = exporter.decorator()

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
setattr(types, 'SimpleNamespace',   SimpleNamespace)
setattr(types, 'Namespace',         Namespace)

# Add the array.ArrayType base type as “Array”:
setattr(types, 'Array',             array.ArrayType)

# Add the collections.abc.MappingView base type:
setattr(types, 'MappingView',       collections.abc.MappingView)

# Add weakref builtin types:
setattr(types, 'Reference',         weakref.ReferenceType)
setattr(types, 'Proxy',             weakref.ProxyType)
setattr(types, 'CallableProxy',     weakref.CallableProxyType)

# Manually set `types.__file__` and related attributes:
setattr(types, '__file__',          __file__)
setattr(types, '__cached__',        cache_from_source(__file__))
setattr(types, '__package__',       path_to_dotpath(__file__,
                                                    relative_to=BASEPATH))

@export
def modulize(name, namespace, docs=None,
                              path=None,
                           appname=PROJECT_NAME,
                       relative_to=BASEPATH):
    """ Convert a dictionary mapping into a legit Python module """
    from clu.naming import dotpath_join
    from clu.predicates import nopyattr
    from clu.typology import ismapping
    import inspect, sys
    
    # Ensure a module with the given module name we received
    # doesn’t already exist in `sys.modules`:
    if name is None:
        raise TypeError("Module name cannot be None")
    if namespace is None:
        raise TypeError("Module namespace cannot be None")
    if not ismapping(namespace):
        raise TypeError("Module namespace must be a mapping type")
    
    # Ensure “namespace” is an instance of “clu.typespace.namespace.Namespace”:
    namespace = Namespace(namespace)
    
    # Update the namespace with '__all__' and '__dir__' if necessary:
    ns_all = None
    
    if '__all__' not in namespace and not nopyattr(namespace, 'all'):
        ns_all = tuple(sorted(namespace.keys()))
        namespace['__all__'] = ns_all
    
    if '__dir__' not in namespace:
        if ns_all is None:
            ns_all = namespace.get('__all__', None) or \
                     tuple(sorted(namespace.keys()))
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
                                      appname,
                                      path_to_dotpath(path,
                                                      relative_to),
                                      name)
        
        # Note that one can use a file path that does not
        # have to necessarily exist on the filesystem in an
        # accessible manner:
        namespace.update({ '__file__' : path,
                         '__cached__' : cache_from_source(path) })
    else:
        qualified_name = dotpath_join(DYNAMIC_MODULE_PREFIX,
                                      appname,
                                      name)
    
    # Has this already been done with this name?
    if qualified_name in sys.modules:
        return sys.modules[qualified_name]
    
    # Ensure we have a name and a package dotpath in our namespace:
    namespace.update({ '__name__' : name,
                   '__qualname__' : name,
                    '__package__' : qualified_name })
    
    # Construct the module type from the qualified name, using
    # any given docstring text:
    module = types.Module(qualified_name, inspect.cleandoc(docs))
    
    # Update the module’s `__dict__` with our namespaced mapping
    module.__dict__.update(namespace.__dict__)
    
    # Update the `sys.modules` mapping with the new module,
    # as required by Python’s internal import machinery --
    # Once `sys.modules` has been thusly updated, the new module
    # can be imported with an “import «name»” statement, as with
    # any other available module:
    sys.modules[qualified_name] = module
    
    # Return our new module instance:
    return module

export(types,           name='types',       doc=""" A Namespace instance containing aliases into the `types` module,
                                                    sans the irritating and lexically unnecessary “Type” suffix --
                                                    e.g. `types.ModuleType` can be accessed as just `types.Module`
                                                    from this Namespace, which is less pointlessly redundant and far
                                                    more typographically pleasing, like definitively.
                                                """)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
