# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import lru_cache

import sys, re

from clu.constants import consts
from clu.predicates import tuplize, typeof
from clu.typology import ismapping
from clu.exporting import Exporter, sysmods, itermodule

exporter = Exporter(path=__file__)
export = exporter.decorator()

cache = lambda function: export(lru_cache(maxsize=16, typed=False)(function))

@export
def issimplemap(mapping):
    if not ismapping(mapping):
        return False
    if not mapping:
        return False
    out = True
    for nskey, value in mapping.items():
        out &= (not ismapping(value))
        out &= (not consts.NAMESPACE_SEP in nskey)
        if out is False:
            return out
    return out

@export
def isflatmap(mapping):
    """ Boolean predicate for determining if a mapping is flat –
        that is to say, if it has no sub-mappings as top-level
        tree values.
        
        N.B. We should enhance this to work recursively
    """
    if not ismapping(mapping):
        return False
    if not mapping:
        return False
    if any(consts.NAMESPACE_SEP in nskey for nskey in mapping):
        # We have at least one top:level:namespaced:key →
        if any(ismapping(value) for value in mapping.values()):
            # We have, it would seem, both a namespaced key
            # and a nested value at top level. What???
            return False
        return True
    # we have no namespaced keys at the top level
    if any(ismapping(value) for value in mapping.values()):
        # We have a nested value amongst flat keys
        return False
    return True

@export
def isnestedmap(mapping):
    """ Boolean predicate for determining if a mapping is nested –
        that is to say, if contains sub-mappings at the top-level.
        
        N.B. We should enhance this to work recursively
    """
    if not ismapping(mapping):
        return False
    if not mapping:
        return False
    if any(consts.NAMESPACE_SEP in nskey for nskey in mapping):
        # We have at least one top:level:namespaced:key →
        # if any(ismapping(value) for value in mapping.values()):
        #     # We have, it would seem, both a namespaced key
        #     # and a nested value at top level. What???
        #     return False # WTF HAX
        return False
    # we have no namespaced keys at the top level
    if any(ismapping(value) for value in mapping.values()):
        # We have a nested value amongst flat keys
        return True
    return False

frozen_re = re.compile(r"^[Ff]rozen")

@cache
def thaw_name(name):
    """ Private function, to cache “thawed” class names """
    return frozen_re.sub('', name)

@cache
def freeze_name(name):
    """ Private function, to cache “frozen” class names """
    if name.startswith("rozen", 1):
        return name
    if name.islower():
        return f"frozen{name}"
    return f"Frozen{name}"

@cache
def thaw_class(cls):
    """ Private function, to “thaw” a possibly frozen –
        otherwise known as “immutable” – class, based
        on its name and module.
    """
    from clu.naming import dotpath_join, moduleof, qualified_import
    clsname = cls.__name__
    if clsname.startswith("rozen", 1):
        # try to import the non-frozen version:
        putative = dotpath_join(moduleof(cls), thaw_name(clsname))
        melted = qualified_import(putative, recurse=True)
        frozen = cls
        cls = melted
    else:
        frozen = melted = cls
    return melted

@cache
def freeze_class(cls):
    """ Private function, to “freeze” a mutable class, based
        on its name and module.
    """
    from clu.naming import dotpath_join, moduleof, qualified_import
    putative = dotpath_join(moduleof(cls), freeze_name(cls.__name__))
    return qualified_import(putative, recurse=True)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from pprint import pprint
    
    @inline
    def test_thaw_name():
        pass
    
    @inline
    def test_thaw_class():
        pass
    
    @inline
    def test_freeze_name():
        pass
    
    @inline
    def test_freeze_class():
        pass
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())