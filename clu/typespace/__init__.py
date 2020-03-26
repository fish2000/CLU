# -*- coding: utf-8 -*-
from __future__ import print_function

import array
import collections
import collections.abc
import weakref
import sys, re

from clu.constants.consts import pytuple, BASEPATH, APPNAME, VERBOTEN
from clu.exporting import Exporter, path_to_dotpath

exporter = Exporter(path=__file__)
export = exporter.decorator()

typed = re.compile(r"^(?P<typename>\w+)(?:Type)$")

def prepare_types_ns(path, basepath):
    """ Prepare and return the “types” alias namespace """
    from clu.constants.polyfills import cache_from_source
    from clu.typespace.namespace import SimpleNamespace, Namespace
    from clu.predicates import pyattr
    
    # Import-rename the original “types” module:
    import types as thetypes
    types = Namespace()
    
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
    
    # Throw in the `cache_from_source` function:
    setattr(types, 'cache_from_source', cache_from_source)
    
    # Manually set `types.__file__` and related attributes:
    setattr(types, '__file__',          path)
    setattr(types, '__cached__',        cache_from_source(path))
    setattr(types, '__package__',       path_to_dotpath(path, relative_to=basepath))
    setattr(types, '__qualname__',      pyattr(thetypes, 'qualname', 'name'))
    
    return types

# Prepare CLU’s typespace:
types = prepare_types_ns(path=__file__,
                         basepath=BASEPATH)

@export
def modulize(name, namespace, docs=None,
                              path=None,
                           appname=APPNAME,
                          basepath=BASEPATH):
    """ Convert a dictionary mapping into a legit Python module """
    from clu.dicts import asdict
    from clu.naming import dotpath_join, dotpath_split
    from clu.typology import ismapping
    import inspect
    
    # Ensure a module with the given module name we received
    # doesn’t already exist in `sys.modules`:
    if name is None:
        raise TypeError("Module name cannot be None")
    if namespace is None:
        raise TypeError("Module namespace cannot be None")
    if not ismapping(namespace):
        raise TypeError("Module namespace must be a mapping type")
    
    # Ensure we have an instance of “clu.typespace.namespace.Namespace”:
    ns = types.Namespace(asdict(namespace))
    
    # Check for a __file__ entry in the namespace if we weren’t
    # called with a path:
    if not path:
        path = ns.get('__file__', None)
    
    # Construct a trivially namespaced name for the module,
    # based on the given name, the given file path (if any), and
    # some reasonable prefixes:
    qname = dotpath_join(path_to_dotpath(path,
                         relative_to=basepath) or appname,
                         name)
    
    # Has this already been done with this name?
    if qname in sys.modules:
        return sys.modules[qname]
    
    # Add '__all__' and '__dir__' to the namespace if necessary:
    if '__all__' not in ns:
        ns['__all__'] = tuple(sorted(ns.keys()))
    
    if '__dir__' not in ns:
        allval = ns['__all__']
        ns['__dir__'] = lambda: list(allval)
    
    # Note that one can use a file path that does not
    # have to necessarily exist on the filesystem in an
    # accessible manner:
    if path:
        ns.update({ '__file__' : path,
                  '__cached__' : types.cache_from_source(path) })
    
    # Ensure we have a name and a package dotpath in our namespace:
    ns.update({ '__name__' : name,
            '__qualname__' : name,
             '__package__' : dotpath_split(qname)[-1] })
    
    # Construct the module type from the qualified name, using
    # any given docstring text:
    module = types.Module(qname, inspect.cleandoc(docs))
    
    # Update the module’s `__dict__` with our namespaced mapping
    module.__dict__.update(ns.__dict__)
    
    # Update the `sys.modules` mapping with the new module,
    # as required by Python’s internal import machinery --
    # Once `sys.modules` has been thusly updated, the new module
    # can be imported with an “import «name»” statement, as with
    # any other available module:
    sys.modules[qname] = module
    
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

def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_one():
        """ Check the typespace (the “types” namespace) """
        import types as thetypes
        
        for typename in dir(thetypes):
            
            if typename.endswith('Type'):
                shortname = typed.match(typename).group('typename')
                assert hasattr(types, shortname)
                assert getattr(types, shortname) == getattr(thetypes, typename)
            
            elif typename not in VERBOTEN:
                # Can’t assert equality – many of these are different:
                assert hasattr(types, typename)
    
    # __doc__ won’t be equal as we reset it during the export;
    # and neither will the name attributes, like by definition:
    verboten = VERBOTEN + pytuple('doc', 'name', 'qualname')
    
    @inline
    def test_two():
        """ Check the output of the “prepare_types_ns(…)” function """
        moretypes = prepare_types_ns(path=__file__, basepath=BASEPATH)
        
        for typename in dir(types):
            if typename not in verboten:
                assert types[typename] == getattr(moretypes, typename)
                # print("UNEQUAL:", typename, types[typename], moretypes[typename])
    
    @inline
    def test_three():
        """ Check modulization """
        moretypes = prepare_types_ns(path=__file__, basepath=BASEPATH)
        modulize('moretypes', moretypes, "A module containing aliases into the `types` module")
        
        # from pprint import pprint
        # pprint([key for key in sys.modules.keys() if key.startswith('clu')])
        
        from clu.typespace import moretypes
        
        for typename in dir(types):
            if typename not in verboten:
                assert types[typename] == getattr(moretypes, typename)
                # print("UNEQUAL:", typename, types[typename], getattr(moretypes, typename))
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
