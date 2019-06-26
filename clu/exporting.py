# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import warnings

# from constants import DEBUG, SINGLETON_TYPES, Enum, unique
from constants import LAMBDA, PY3, SEPARATOR_WIDTH
from constants import Counter, MutableMapping, NoDefault, OrderedDict
from constants import ExportError, ExportWarning
from predicates import pytuple, case_sort
from naming import doctrim, determine_name
from naming import thingname_search, thingname_search_by_id
from repl import print_separator

def predicates_for_types(*types):
    """ For a list of types, return a list of “isinstance” predicates """
    predicates = []
    for classtype in frozenset(types):
        predicates.append(lambda thing: isinstance(thing, classtype))
    return tuple(predicates)

class Exporter(MutableMapping):
    
    """ A class representing a list of things for a module to export. """
    __slots__ = pytuple('exports', 'clades')
    
    def __init__(self):
        self.__exports__ = {}
        self.__clades__ = Counter()
    
    def exports(self):
        """ Get a new dictionary instance filled with the exports. """
        out = {}
        out.update(self.__exports__)
        return out
    
    def clade_histogram(self):
        """ Return the histogram of clade counts. """
        return Counter(self.__clades__)
    
    messages = {
        'docstr'    : "Can’t set the docstring for thing “%s” of type %s:",
        'xclade'    : "Can’t determine a clade for thing “%s” of type %s",
        'noname'    : "Can’t determine a name for lambda: 0x%0x"
    }
    
    # def classify(self, thing, named):
    #     """ Attempt to classify a thing to a clade.
    #         Returns a member of the Clade enum.
    #     """
    #     clade = Clade.of(thing, name_hint=named)
    #     if DEBUG:
    #         print("••• \tthing: %s" % str(thing))
    #         print("••• \tnamed: %s" % str(named))
    #         print("••• \tclade: %s" % repr(clade))
    #         print()
    #     return clade
    
    def increment_for_clade(self, thing, named, increment=1):
        # clade = self.classify(thing, named=named)
        # self.__clades__[clade] += int(increment)
        # return clade
        pass
    
    def decrement_for_clade(self, thing, named, decrement=-1):
        # clade = self.classify(thing, named=named)
        # self.__clades__[clade] += int(decrement)
        # return clade
        pass
    
    def keys(self):
        """ Get a key view on the exported items dictionary. """
        return self.__exports__.keys()
    
    def values(self):
        """ Get a value view on the exported items dictionary. """
        return self.__exports__.values()
    
    def get(self, key, default=NoDefault):
        if default is NoDefault:
            return self.__exports__.get(key)
        return self.__exports__.get(key, default)
    
    def pop(self, key, default=NoDefault):
        if key in self.__exports__:
            self.decrement_for_clade(self[key], named=key)
        if default is NoDefault:
            return self.__exports__.pop(key)
        return self.__exports__.pop(key, default)
    
    def export(self, thing, name=None, doc=None):
        """ Add a function -- or any object, really -- to the export list.
            Exported items will end up wih their names in the modules’
           `__all__` tuple, and will also be named in the list returned
            by the modules’ `__dir__()` function.
            
            It looks better if this method is decoupled from its parent
            instance, to wit:
            
                exporter = Exporter()
                export = exporter.decorator() # q.v. “decorator()” sub.
            
            Use `export` as a decorator to a function definition:
                
                @export
                def yo_dogg(i_heard=None):
                    …
                
            … or manually, to export anything that doesn’t have a name:
                
                yo_dogg = lambda i_heard=None: …
                dogg_heard_index = ( ¬ ) 
                
                export(yo_dogg,             name="yo_dogg")
                export(dogg_heard_index,    name="dogg_heard_index")
            
        """
        # No explict name was passed -- try to determine one:
        named = determine_name(thing, name=name)
        
        # Double-check our determined name and item before stowing:
        if named is None:
            raise ExportError("can’t export an unnamed thing")
        if named in self.__exports__:
            raise ExportError("can’t re-export name “%s”" % named)
        if thing is self.__exports__:
            raise ExportError("can’t export the __exports__ dict directly")
        if thing is self:
            raise ExportError("can’t export an exporter instance directly")
        
        # Attempt to classify the item to a clade:
        try:
            self.increment_for_clade(thing, named=named)
        except ValueError:
            # no clade found
            typename = determine_name(type(thing))
            warnings.warn(type(self).messages['xclade'] % (named, typename),
                          ExportWarning, stacklevel=2)
        
        # At this point, “named” is valid -- if we were passed
        # a lambda, try to rename it with either our valid name,
        # or the result of an ID-based search for that lambda:
        if callable(thing):
            if getattr(thing, '__name__', '') == LAMBDA:
                if named == LAMBDA:
                    named = thingname_search(thing)
                if named is None:
                    raise ExportError(type(self).messages['noname'] % id(thing))
                thing.__name__ = thing.__qualname__ = named
                thing.__lambda_name__ = LAMBDA # To recall the lambda’s genesis
        
        # If a “doc” argument was passed in, attempt to assign
        # the __doc__ attribute accordingly on the item -- note
        # that this won’t work for e.g. slotted, builtin, or C-API
        # types that lack mutable __dict__ internals (or at least
        # a settable __doc__ slot or established attribute).
        if doc is not None:
            try:
                thing.__doc__ = doctrim(doc)
            except (AttributeError, TypeError):
                typename = determine_name(type(thing))
                warnings.warn(type(self).messages['docstr'] % (named, typename),
                              ExportWarning, stacklevel=2)
        
        # Stow the item in the global __exports__ dict:
        self.__exports__[named] = thing
        
        # Return the thing, unchanged (that’s how we decorate).
        return thing
    
    def decorator(self):
        """ Return a reference to this Exporter instances’ “export”
            method, suitable for use as a decorator, e.g.:
            
                export = exporter.decorator()
                
                @export
                def yodogg():
                    ''' Yo dogg, I heard you like exporting '''
                    …
            
            … This should be done near the beginning of a module,
            to facilitate marking functions and other objects to be
            exported – q.v. the “all_and_dir()” method sub.
        """
        return self.export
    
    def __call__(self):
        """ Exporter instances are callable, for use in `__all__` definitions """
        return tuple(self.keys())
    
    def dir_function(self):
        """ Return a list containing the exported module names. """
        return list(self.keys())
    
    def all_and_dir(self):
        """ Assign a modules’ __all__ and __dir__ values, e.g.:
            
                __all__, __dir__ = exporter.all_and_dir()
            
            … This should be done near the end of a module, after
            all calls to `exporter.export(…)` (aka @export) have
            been made – q.v. the “decorator()” method supra.
        """
        return self(), self.dir_function
    
    def dir_and_all(self):
        """ Assign a modules’ __dir__ and __all__ values, e.g.:
            
                __dir__, __all__ = exporter.dir_and_all()
            
            … This should be done near the end of a module, after
            all calls to `exporter.export(…)` (aka @export) have
            been made – q.v. the “decorator()” method supra.
        """
        return self.dir_function, self() # OPPOSITE!
    
    def cache_info(self):
        """ Shortcut to get the CacheInfo namedtuple from the
            cached internal `thingname_search_by_id(…)` function,
            which is used in last-resort name lookups made by
            `determine_name(…)` during `export(…)` calls.
        """
        return thingname_search_by_id.cache_info()
    
    def _print_export_list(self):
        """ Print out a prettified (IMHO at any rate) representation of
            the current module export list.
            
            N.B. This function is a fucking illegible mess at the moment
        """
        from pprint import pformat
        exports = self.exports()
        keys = sorted(exports.keys(), key=case_sort, reverse=True)
        vals = (exports[key] for key in keys)
        print_separator()
        print("≠≠≠ EXPORTS: (length = %i)" % len(keys))
        print()
        od = OrderedDict.fromkeys(keys)
        od.update(zip(keys, vals))
        for idx, (key, value) in enumerate(reversed(od.items())):
            prelude = "%03d → [ %24s ] →" % (idx, key)
            print(prelude, " %s" % re.subn(r'\n', '\n' + " " * (len(prelude) + 2),
                                                                pformat(value,
                                                                        width=SEPARATOR_WIDTH,
                                                                        compact=True), flags=re.MULTILINE)[0])
    
    def _print_clade_histogram(self):
        """ Print out a bar graph of the current clade histogram.
            Like e.g. this:
            
            ---------------------------------------------------------------------------------
            ≠≠≠ CLASSIFICATION HISTOGRAM
            ≠≠≠ Clades: 8 (of 12)
            ≠≠≠ Things: 102 total, 0 unclassified
            
            00 → [       LAMBDA ] → 46 • 45% ••••••••••••••••••••••••••••••••••••••••••••••
            01 → [     FUNCTION ] → 28 • 27% ••••••••••••••••••••••••••••
            02 → [     SEQUENCE ] → 10 •  9% ••••••••••
            03 → [        CLASS ] →  8 •  7% ••••••••
            04 → [    SINGLETON ] →  3 •  2% •••
            05 → [       STRING ] →  3 •  2% •••
            06 → [   DICTIONARY ] →  2 •  1% ••
            07 → [       NUMBER ] →  2 •  1% ••
            
            ≠≠≠ 4 leaf clades:
            ≠≠≠ instance, iterable, metaclass, set
            
            ---------------------------------------------------------------------------------
        """
        clade_histogram = self.clade_histogram()
        total = sum(clade_histogram.values())
        unclassified = len(self) - total
        print_separator()
        print("≠≠≠ CLASSIFICATION HISTOGRAM")
        # print("≠≠≠ Clades: %i (of %i)" % (len(clade_histogram), len(Clade)))
        print("≠≠≠ Things: %i total, %i unclassified" % (total, unclassified))
        print()
        for idx, (clade, count) in enumerate(sorted(clade_histogram.items(),
                                                    key=lambda item: item[1],
                                                    reverse=True)):
            prelude = "%02d → [ %12s ] → %2i • %s%%" % (idx,
                                                        clade.name,
                                                        count,
                                                        str(int((count / total) * 100)).rjust(2)) # percent
            print(prelude, "•" * count) # ASCII histogram bar graph
        print()
        # leafclades = frozenset(Clade) - frozenset(clade_histogram.keys())
        # if len(leafclades) > 0:
        #     print("≠≠≠ %i leaf clades:" % len(leafclades))
        #     print("≠≠≠ %s" % ", ".join(sorted(clade.to_string() for clade in leafclades)))
        #     print()
    
    def _print_cache_info(self):
        """ Print out the “CacheInfo” namedtuple from the search-by-ID
            cached thingname function (q.v. “cache_info()” method supra.)
        """
        from pprint import pprint
        print_separator()
        print("≠≠≠ THINGNAME SEARCH-BY-ID CACHE INFO:")
        print()
        pprint(self.cache_info())
    
    def print_diagnostics(self, module_all, module_dir):
        """ Pretty-print the current list of exported things """
        # Sanity-check the modules’ __dir__ and __all__ attributes
        exports = self.exports()
        
        assert list(module_all) == module_dir()
        assert len(module_all) == len(module_dir())
        assert len(module_all) == len(exports)
        
        # Pretty-print the export list
        self._print_export_list()
        
        # Pretty-print the clade histogram
        # self._print_clade_histogram()
        
        # Print the cache info
        if PY3:
            self._print_cache_info()
        
        # Print closing separators
        print_separator()
        print()
    
    def __iter__(self):
        return iter(self.__exports__.keys())
    
    def __len__(self):
        return len(self.__exports__)
    
    def __contains__(self, key):
        return key in self.__exports__
    
    def __getitem__(self, key):
        return self.__exports__[key]
    
    def __setitem__(self, key, value):
        if key in self.__exports__:
            self.decrement_for_clade(self[key], named=key)
        self.increment_for_clade(value, named=key)
        self.__exports__[key] = value
    
    def __delitem__(self, key):
        self.decrement_for_clade(self[key], named=key)
        del self.__exports__[key]
    
    def __bool__(self):
        return len(self.__exports__) > 0

exporter = Exporter()
export = exporter.decorator()

__all__ = ('Exporter', 'exporter', 'export')
__dir__ = lambda: list(__all__)