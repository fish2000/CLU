# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple
from functools import lru_cache

import collections.abc
import clu.abstract
import clu.dicts
import clu.all
import importlib
import pickle
import sys

from clu.constants import consts
from clu.typespace import types
from clu.predicates import (ispyname,
                            negate,
                            lowers)

from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

cache       = lambda function: export(lru_cache(maxsize=128, typed=True)(function))

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
                clu.abstract.ReprWrapper,
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
        self.module = getattr(module, 'module', module)
        self.reload(reload_module=False)
    
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
        except AttributeError as exc:
            raise KeyError(key) from exc
        return out
    
    def __len__(self):
        return len(self.dir)
    
    def keys(self):
        return clu.dicts.OrderedKeysView(self)
    
    def values(self):
        return clu.dicts.OrderedValuesView(self)
    
    def items(self):
        return clu.dicts.OrderedItemsView(self)
    
    def reload(self, reload_module=True):
        if reload_module:
            self.module = importlib.reload(self.module)
        self.dir = tuple(sorted(filter(notpyname, dir(self.module)), key=lowers))
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
    
    def inner_repr(self):
        return repr(dict(self))

clu_importall = clu.all.import_all_modules

@cache
def compare_module_lookups_for_all_things(*modules,
                                           module_function=clu_importall,
                                         **options):
    """ Iterate through each exported item, for each exported module,
        and look up the original module of the exported item with both:
            
            1) “pickle.whichmodule(…)” and
            2) “clu.naming.moduleof(…)”
        
        … comparing the results of the two search functions and computing
        the overall results.
    """
    from clu.naming import nameof, moduleof
    
    # N.B. This is not yet properly paramatrized,
    # as it is using CLU’s exporter class, by fiat –
    # it will need the “clu.application” stuff to
    # be up and running to get around that, methinks
    
    basepath      = options.get('basepath',      consts.BASEPATH)
    appname       = options.get('appname',       consts.APPNAME)
    exporter_name = options.get('exporter_name', consts.EXPORTER_NAME)
    
    total = 0
    item_idx = 0
    module_idx = 0
    mismatch_idx = 0
    mismatches = []
    results = []
    
    clumodules = module_function(basepath, appname, exporter_name)
    assert clumodules
    
    modulenames = tuple(modules or Exporter.modulenames())
    
    for modulename in modulenames:
        exports = Exporter[modulename].exports()
        total += len(exports)
        results.append(Result(modulename,
                        tuple(exports.keys()),
                        module_idx))
        
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
                                           mismatch_idx))
                mismatch_idx += 1
            item_idx += 1
        module_idx += 1
    
    # In practice the failure rate seemed to be around 7.65 %
    failure_rate = 100 * (float(mismatch_idx) / float(total))
    assert failure_rate < 10.0 # percent
    
    return Results(item_idx,  modulenames, tuple(results)), \
           Mismatches(mismatch_idx,        tuple(mismatches),
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
        modules = ('predicates', 'typology', 'mathematics', 'naming',
                   'exporting', 'extending', 'all', 'enums')
        prefixd = tuple(f"clu.{nm}" for nm in modules)
        return prefixd
    
    @inline
    def test_compare_all():
        """ Basic checks for compare_module_lookups_for_all_things(…) """
        results, mismatches = compare_module_lookups_for_all_things()
        
        for idx, result in enumerate(results.result_records):
            assert result.idx == idx
        
        assert results.total > 100
        assert mismatches.total > 0
        assert mismatches.failure_rate < 10.0
    
    @inline
    def test_compare_all_with_varargs():
        """ With-vararg checks for compare_module_lookups_for_all_things(…) """
        results, mismatches = compare_module_lookups_for_all_things(
                             *predicate_modules())
        
        for idx, result in enumerate(results.result_records):
            assert result.idx == idx
        
        assert results.total > 100
        assert mismatches.total > 0
        assert mismatches.failure_rate < 10.0
    
    @inline
    def test_modulemap_with_clu_consts():
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
        
        # Try reloading:
        constmap.reload()
        assert constmap.reload() == len(constmap)
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())

