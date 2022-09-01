# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import lru_cache
from itertools import chain

cache = lambda function: lru_cache()(function)
iterchain = chain.from_iterable

import clu.abstract
import clu.dicts
import inspect
import sys

from clu.constants import consts
from clu.naming import nameof, qualified_name

from clu.predicates import anyattrs, attr, item_search, tuplize
from clu.typology import ismodule, ismapping
from clu.importing import ModuleBase, DO_NOT_INCLUDE
from clu.exporting import ExporterBase, Exporter

NoDefault = consts.NoDefault

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class ChainModuleMap(clu.dicts.ChainMap):
    
    """ Custom “clu.dicts.ChainMap” subclass, tailored for module dicts.
        
        In addition to the arguments accepted by its ancestor, one may
        pass in a sequence of functions as a keyword argument “fallbacks”.
        Each of these functions should accept exactly one argument –
        a mapping key string – and either return something for it, or
        raise either an AttributeError or a KeyError.
        
        … This is meant to allow one to pass in one or more module-level
        “__getattr__(…)” functions, “Mapping.__missing__(…)” methods, or
        similar callables – the ChainModuleMap “__missing__(…)” method
        itself will attempt to invoke these functions in order, should
        it be called upon (hence the name “fallbacks”).
    """
    
    __slots__ = 'fallbacks'
    
    def __init__(self, *dicts, fallbacks=None, **overrides):
        super().__init__(*dicts, **overrides)
        self.fallbacks = fallbacks or tuple()
    
    def __iter__(self):
        yield from filter(lambda item: item not in consts.BUILTINS,
                          super().__iter__())
    
    def __getitem__(self, key):
        # Use “item_search(…)” in order to only trigger a constituent
        # maps’ “__missing__(…)” method within our own “__missing__(…)”
        # function call:
        item = item_search(key, *self.maps, default=NoDefault)
        if item is NoDefault:
            return self.__missing__(key)
        return item
    
    def __missing__(self, key):
        # “self.fallbacks” should be populated with any module-level
        # “__getattr__(…)” functions, mapping “__missing__(…)” instance-
        # member methods, as extracted from targets – or custom callables
        # with identical signatures and exception-raising characteristics:
        for fallback in self.fallbacks:
            try:
                return fallback(key)
            except (AttributeError, KeyError):
                continue
        if key in self:
            return 0
        raise KeyError(key)

# Define an out-of-line target-processing function:
def add_targets(instance, *targets):
    """ Out-of-line, use-twice-and-destroy function for processing targets """
    
    # Ensure the necessary lists have been established on the proxy:
    if getattr(instance, 'target_dicts', None) is None:
        instance.target_dicts = []
    if getattr(instance, 'target_lists', None) is None:
        instance.target_lists = []
    if getattr(instance, 'target_funcs', None) is None:
        instance.target_funcs = []
    
    # Iterate over targets, acting accordingly:
    for target in targets:
        if target is None:
            continue
        
        # Extract and flatten any proxy sub-module contents:
        if isinstance(target, ProxyModule):
            for mapping in target.__proxies__.maps:
                if mapping not in instance.target_dicts:
                    instance.target_dicts.append(mapping)
            for name in target.__filters__:
                if name not in instance.target_lists:
                    instance.target_lists.append(name)
            for function in target.__proxies__.fallbacks:
                if function not in instance.target_funcs:
                    instance.target_funcs.append(function)
            continue
        
        # Use the module’s “__dict__”, “dir(…)” output,
        # and “__getattr__(…)” function (if any):
        if ismodule(target):
            if target.__dict__ not in instance.target_dicts:
                instance.target_dicts.append(target.__dict__)
                instance.target_lists.append(dir(target))
            if hasattr(target, '__getattr__'):
                if target.__getattr__ not in instance.target_funcs:
                    instance.target_funcs.append(target.__getattr__)
            continue
        
        # Use the mapping itself, a listification of its keys,
        # and “__missing__(…)” method (if any):
        if ismapping(target):
            if target not in instance.target_dicts:
                instance.target_dicts.append(target)
                instance.target_lists.append(list(target.keys()))
            if hasattr(target, '__missing__'):
                if target.__missing__ not in instance.target_funcs:
                    instance.target_funcs.append(target.__missing__)
            continue
        
        # Simply stow any callables as fallback functions:
        if callable(target):
            if target not in instance.target_funcs:
                instance.target_funcs.append(target)
            continue

@export
class ProxyModule(ModuleBase):
    
    """ A ProxyModule is a specific type of module: one that wraps one or
        more other things and surfaces their attributes, as if they are all
        one big unified module.
        
        In this case, “things” can be modules, mappings, or callables – the
        ProxyModule employs a bespoke ChainMap subclass to keep these varied
        targets in order, for idempotent access with deterministic ordering,
        like in a way that ought not surprise or scare anybody.
        
        Callable targets are fallbacks – they are invoked by the “__missing__”
        method of the internal ChainMap, when attribute lookup across all of
        the module and mapping proxy targets is exhaustively unsuccessful.
        
        The ProxyModule is a “pseudo-template” type – you need to specialize
        it with the specific Module types with which you wish to use it.
        In nearly every use-case scenario, this means using one of the Module
        class types you have obtained through calling “initialize_types(…)”
        (as above) – like so:
            
            >>> Module, Finder, Loader = initialize_types(my_appname)
            >>> class myproxy(ProxyModule[Module]):
            >>>     # …etc
        
        Here’s a basic example of a ProxyModule subtype definition:
        
            >>> overrides = dict(…)
            >>> from yodogg.app import base_module
            >>> from yodogg.utils import misc as second_module
            >>> from yodogg.utils.functions import default_factory
            
            >>> class myproxy(ProxyModule[Module]):
            >>>     targets = (overrides, base_module,
            >>>                         second_module,
            >>>                       default_factory)
        
        … which after defining that, you’d use it like so – assuming your app
        is called “yodogg” with a default “app” appspace (see “ModuleBase” for
        more on these terms):
        
            >>> from yodogg.app import myproxy
            >>> myproxy.attrib # searches overrides, base_module and second_module
            >>>                # in sequence, looking for the 'attrib' value
            >>> dir(myproxy)   # returns a list of the union of available stuff,
            >>>                # across the proxy modules’ targets
            >>> myproxy.NOATTR # unknown attributes will be forwarded to each
            >>>                # module-level “__getattr__(…)” function, dictionary
            >>>                # “__missing__(…)” method, or callable target found,
            >>>                # in turn, if the attribute search proves exhaustive
        
        … you can, in the modules’ definition, include other stuff besides the
        class-level “targets” tuple; other elements added to the proxy will
        behave like elements of any other class-based module.
    """
    
    def __new__(cls, name, *targets, doc=None):
        """ Allocate a new tabula-rasa proxy-module instance.
            
            Adds any targets passed in when the constructor was called –
            which that should be like never, except maybe under testing
            or somesuch – for the most part, ProxyModule targets’ll be
            specified as a class-level tuple attribute.
            
            See the main class docstring for the deets.
        """
        # Call up, creating the instance:
        instance = super(ProxyModule, cls).__new__(cls)
        
        # Fill in our “slots” with empty structs:
        instance.__filters__ = []
        instance.__proxies__ = {}
        instance.target_dicts = []
        instance.target_lists = []
        instance.target_funcs = []
        
        # Process any targets with which this instance
        # may have been constructed:
        add_targets(instance, *targets)
        
        # Return the new instance:
        return instance
    
    def __init__(self, name, *targets, doc=None):
        """ Initialize a proxy-module instance.
            
            The signature for initializing a proxy module is the same
            as that for a class-based module – the proxy module class
            derives directly from the application-specific class-based
            module definition – with the optional addition of zero-to-N
            “targets”.
            
            Each target so named can be either a mapping-ish type, a
            module, or a callable. The proxy module will then use the
            list of targets – considerate of order – to construct a
            custom “clu.dicts.ChainMap” instance that pulls, in turn,
            from the target list (and falling back to results from any
            callable targets after exhausting said list).
            
            Attribute lookup on the proxy module instance will follow
            along through the “ChainMap” instances’ internal stack of
            mappings.
        """
        # Super-initialize:
        super(ProxyModule, self).__init__(name, doc=doc)
        
        # Get a reference to the module class:
        cls = type(self)
        
        # Process and strip off a class-level “targets”
        # list attribute – if such a thing exists – and
        # then sequester said “targets” attribute behind
        # an underscore, if necessary:
        if anyattrs(cls, 'targets', '_targets'):
            add_targets(self, *attr(cls, 'targets', '_targets'))
            if hasattr(cls, 'targets'):
                # This type of defensive programming is necessary due to
                # how module “__init__(…)” methods are nondeterministically
                # subject to being called more than once:
                setattr(cls, '_targets', attr(cls, 'targets', '_targets'))
                try:
                    # Fails when “targets” is a superclass attribute:
                    delattr(cls, 'targets')
                except AttributeError:
                    pass
    
    def __execute__(self):
        # Create the internal “clu.dicts.ChainMap” subclass instance,
        # and pre-combine any “__dir__”-value lists we may be using:
        self.__filters__ = tuple(iterchain(self.target_lists))
        self.__proxies__ = ChainModuleMap(*self.target_dicts,
                        fallbacks=tuplize(*self.target_funcs))
        
        # Further unclutter the module namespace:
        delattr(self, 'target_dicts')
        delattr(self, 'target_lists')
        delattr(self, 'target_funcs')
        
        # Call up:
        super().__execute__()
    
    def __dir__(self):
        cls = type(self)
        names = chain(self.__filters__,
                       cls.__dict__.keys())
        return sorted(frozenset(names) - DO_NOT_INCLUDE)
    
    def __getattr__(self, key):
        # N.B. AttributeError typenames (herein “ProxyModule”) must be
        # somehow hardcoded – using “self.name” leads to an infinite
        # recursion kertwang within “__getattr__(…)” – since “name”
        # is a property that uses “nameof(self)” which invariably will
        # attempt to get one or another nonexistant attributes from ‘self’.
        try:
            if not self.__dict__.get('_executed', False):
                raise KeyError(f"Access attempt on uninitialized proxy module: {key}")
            elif key in consts.BUILTINS:
                raise KeyError(f"No builtin access on proxy modules: {key}")
            return self.__proxies__[key]
        except KeyError as exc:
            typename = type(self).__name__
            raise AttributeError(f"‘{typename}’ access failure for «{key}»") from exc

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from clu.naming import moduleof
    from clu.importing import Module
    
    @inline.precheck
    def show_module_from_frame():
        """ Use `inspect.currentframe()` to find the parent module """
        parentframe = inspect.currentframe().f_back.f_back.f_back
        parentname = parentframe.f_code.co_name
        module = inspect.getmodule(parentframe)
        print("Frame:", parentframe)
        print("name:", parentname)
        print("module:", module)
        print("module name:", nameof(module))
        print("qualified module name:", qualified_name(module))
        print("module of module:", moduleof(module))
    
    @inline.precheck
    def show_module_fucking_seriously():
        from clu.exporting import thismodule
        module_from = globals().get('exporter', ExporterBase()).dotpath
        print("module from:", module_from)
        print("module():", thismodule())
    
    @inline
    def test_five():
        """ Proxy-module properties and value resolution """
        
        overrides = dict(APPNAME='yodogg',
                         PROJECT_PATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg/yodogg',
                         BASEPATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg')
        
        class TestOverrideConstsProxy(ProxyModule[Module]):
            targets = (overrides, consts)
        
        from clu.app import TestOverrideConstsProxy as overridden
        
        assert overridden.USER == consts.USER
        assert overridden.BUILTINS == consts.BUILTINS
        assert overridden.APPNAME == 'yodogg'
        assert overridden.PROJECT_PATH.endswith('yodogg')
        assert overridden.BASEPATH.endswith('yodogg')
        
        assert not hasattr(overridden, 'targets')
        assert not hasattr(overridden, 'target_dicts')
        assert hasattr(overridden, '_targets')
    
    @inline
    def test_five_point_five():
        """ Proxy-module fallback callable check """
        
        overrides = dict(APPNAME='yodogg',
                         PROJECT_PATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg/yodogg',
                         BASEPATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg')
        
        def fallback_function(key):
            if key.isupper():
                return f"NO DOGG: {key}"
            raise KeyError(key)
        
        class TestOverrideConstsFallbackProxy(ProxyModule[Module]):
            targets = (overrides, consts, fallback_function)
        
        from clu.app import TestOverrideConstsFallbackProxy as overridden
        
        assert overridden.USER == consts.USER
        assert overridden.BUILTINS == consts.BUILTINS
        assert overridden.APPNAME == 'yodogg'
        assert overridden.PROJECT_PATH.endswith('yodogg')
        assert overridden.BASEPATH.endswith('yodogg')
        
        assert overridden.NOATTR == "NO DOGG: NOATTR"   # uppercase: triggers fallback
        
        assert not hasattr(overridden, 'targets')       # lowercase: fallback raises KeyError
        assert not hasattr(overridden, 'target_dicts')  # lowercase: fallback raises KeyError
        assert hasattr(overridden, '_targets')          # attribute found normally
        
        assert dir(overridden)
    
    @inline
    def test_five_point_eight():
        """ Proxy-module hybrid definition check """
        
        overrides = dict(APPNAME='yodogg',
                         PROJECT_PATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg/yodogg',
                         BASEPATH='/Users/fish/Dropbox/CLU/clu/tests/yodogg')
        
        # Ensure that the definitions in the class-module itself
        # take precedent over all proxied target items:
        class TestOverrideConstsHybridProxy(ProxyModule[Module]):
            targets = (overrides, consts)
            
            APPNAME = 'DOGG-YO'
            BASEPATH = consts.BASEPATH
        
        from clu.app import TestOverrideConstsHybridProxy as overridden
        
        assert overridden.USER == consts.USER                   # value from “consts” target
        assert overridden.BUILTINS == consts.BUILTINS           # value from “consts” target
        assert overridden.BASEPATH == consts.BASEPATH           # value from class-module
        assert overridden.APPNAME == 'DOGG-YO'                  # value from class-module
        assert str(overridden.PROJECT_PATH).endswith('yodogg')  # value from “overrides” target
        assert not str(overridden.BASEPATH).endswith('yodogg')  # NOT the value from “overrides”
        
        assert not hasattr(overridden, 'targets')
        assert not hasattr(overridden, 'target_dicts')
        assert hasattr(overridden, '_targets')
        
        assert dir(overridden)
    
    # Run all tests:
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())