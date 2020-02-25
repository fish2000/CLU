# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple

import collections.abc
import clu.abstract
import clu.dicts
import pickle
import sys

from clu import all
from clu.constants import consts
from clu.predicates import ispyname, negate
from clu.typespace import types
from clu.typology import iterlen
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

notpyname   = negate(ispyname)
isplural    = lambda integer: integer != 1 and 's' or ''

Mismatch    = NamedTuple('Mismatch',    ('which',
                                         'determine',
                                         'modulename',
                                         'thingname',
                                         'idx'))

Mismatches  = NamedTuple('Mismatches',  ('total',
                                         'mismatch_records',
                                         'failure_rate'))

Result      = NamedTuple('Result',      ('modulename',
                                         'thingnames',
                                         'idx'))

Results     = NamedTuple('Results',     ('total',
                                         'modulenames',
                                         'result_records'))

@export
class ModuleMap(collections.abc.Mapping,
                collections.abc.Reversible,
                clu.abstract.Cloneable,
                metaclass=clu.abstract.Slotted):
    
    """ An adaptor class, wrapping a module and providing access to
        that modules’ non-dunder-named exports through an implementation
        of the “collections.abc.Mapping” interface.
    """
    
    __slots__ = ('module', 'dir')
    
    def __init__(self, module):
        """ Initialize a ModuleMap with a single module-type argument. """
        if not module:
            raise TypeError("valid module required")
        if not isinstance(module, (type(self), types.Module)):
            raise TypeError("module instance required")
        if isinstance(module, type(self)):
            self.module = getattr(module, 'module')
        else:
            self.module = module
        self.reload()
    
    def __iter__(self):
        yield from self.dir
    
    def __reversed__(self):
        yield from reversed(self.dir)
    
    def __contains__(self, key):
        return key in self.dir
    
    def __getitem__(self, key):
        if ispyname(key):
            raise KeyError(key)
        try:
            out = getattr(self.module, key)
        except AttributeError:
            raise KeyError(key)
        return out
    
    def __len__(self):
        return iterlen(self.dir)
    
    def keys(self):
        return clu.dicts.OrderedKeysView(self)
    
    def values(self):
        return clu.dicts.OrderedValuesView(self)
    
    def items(self):
        return clu.dicts.OrderedItemsView(self)
    
    def reload(self):
        self.dir = tuple(filter(notpyname, dir(self.module)))
        length = len(self.dir)
        if length < 1:
            raise ValueError("module instance must export one or more things")
        return length
    
    def most(self):
        """ Return the string-length of the longest item name in the module """
        return max(len(name) for name in self.dir)
    
    def clone(self, deep=False, memo=None):
        """ Return a cloned copy of the ModuleMap instance """
        # N.B. since we can’t readily deep-clone a module,
        # all cloned instances are shallow:
        return type(self)(self)

@export
def compare_module_lookups_for_all_things(*modules, **options):
    """ Iterate through each exported item, for each exported module,
        and look up the original module of the exported item with both:
            
            1) “pickle.whichmodule(…)” and
            2) “clu.naming.moduleof(…)”
        
        … comparing the results of the two search functions and computing
        the overall results.
    """
    from clu.naming import nameof, moduleof
    
    idx = 0
    total = 0
    mismatch_count = 0
    mismatches = []
    results = []
    
    clumodules = all.import_all_modules(consts.BASEPATH,
                                        consts.APPNAME,
                                        consts.EXPORTER_NAME)
    assert clumodules
    
    modulenames = tuple(modules or Exporter.modulenames())
    
    for modulename in modulenames:
        exports = Exporter[modulename].exports()
        total += len(exports)
        results.append(Result(modulename, tuple(exports.keys()), idx))
        
        for name, thing in exports.items():
            whichmodule = pickle.whichmodule(thing, None)
            determination = moduleof(thing)
            try:
                assert determination == whichmodule
            except AssertionError:
                mismatches.append(Mismatch(whichmodule,
                                           determination,
                                           modulename,
                                           nameof(thing),
                                           mismatch_count))
                mismatch_count += 1
            idx += 1
    
    # In practice the failure rate seemed to be around 7.65 %
    failure_rate = 100 * (float(mismatch_count) / float(total))
    assert failure_rate < 10.0 # percent
    
    return Results(idx, modulenames, tuple(results)), \
           Mismatches(total,         tuple(mismatches),
                                           failure_rate)

export(notpyname,                   name='notpyname',       doc="notpyname(string) → boolean predicate, returns True unless string is a __dunder__ name, when it returns False")
export(isplural,                    name='isplural',        doc="isplural(integer) → returns an 's' unless the integer argument is 1, in which case it returns an empty string")

export(Mismatch,                    name='Mismatch')
export(Mismatches,                  name='Mismatches')
export(Result,                      name='Result')
export(Results,                     name='Results')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline.fixture
    def predicate_modules():
        modules = ('predicates', 'typology', 'mathematics', 'naming')
        prefixd = tuple(f"clu.{nm}" for nm in modules)
        return prefixd
    
    @inline
    def test_one():
        """ Basic checks for compare_module_lookups_for_all_things(…) """
        results, mismatches = compare_module_lookups_for_all_things()
        
        assert results.total > 100
        assert mismatches.total > 0
        assert mismatches.failure_rate < 10.0
    
    @inline
    def test_two():
        """ With-vararg checks for compare_module_lookups_for_all_things(…) """
        results, mismatches = compare_module_lookups_for_all_things(
                             *predicate_modules())
        
        assert results.total > 100
        assert mismatches.total > 0
        assert mismatches.failure_rate < 10.0
    
    @inline
    def test_three():
        """ Basic checks for ModuleMap adapter """
        constmap = ModuleMap(consts)
        
        assert len(constmap) == len(consts.__all__)
        
        assert 'BASEPATH' in constmap
        assert 'APPNAME' in constmap
        assert 'EXPORTER_NAME' in constmap
        
        assert consts.BASEPATH == constmap['BASEPATH']
        assert consts.APPNAME == constmap['APPNAME']
        assert consts.EXPORTER_NAME == constmap['EXPORTER_NAME']
        
        frozenconsts = frozenset(consts.__all__)
        
        # These next two only work if the “consts” module
        # doesn’t export any dunder-named things:
        assert frozenconsts.issuperset(constmap.keys())
        assert frozenconsts.issubset(constmap.keys())
    
    return inline.test(50)

if __name__ == '__main__':
    sys.exit(test())

