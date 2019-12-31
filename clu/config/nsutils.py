# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain, zip_longest

import sys

from clu.constants.consts import NAMESPACE_SEP, NoDefault
from clu.predicates import tuplize
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# NAMESPACE-MANIPULATION FUNCTION API:

@export
def concatenate_ns(*namespaces):
    """ Return the given namespace(s), concatenated with the
        namespace separator.
    """
    return NAMESPACE_SEP.join(namespaces)

@export
def prefix_for(*namespaces):
    """ Return the prefix string for the given namespace(s) """
    ns = concatenate_ns(*namespaces)
    return ns and f"{ns}{NAMESPACE_SEP}" or ns

@export
def strip_ns(nskey):
    """ Strip all namespace-related prefixing from a namespaced key """
    return nskey.rpartition(NAMESPACE_SEP)[-1]

@export
def startswith_ns(putative, prefix):
    """ Boolean predicate to compare a pair of namespace iterables,
        returning True if the first starts with the second.
        
        Do not confuse this with the helper function “compare_ns(…)”,
        defined below, which returns False if the namespace iterables
        in question aren’t exactly alike.
    """
    putative_ns = concatenate_ns(*putative)
    prefix_ns = concatenate_ns(*prefix)
    return putative_ns.startswith(prefix_ns)

@export
def validate_ns(*namespaces):
    """ Raise a ValueError if any of the given namespaces are invalid. """
    for namespace in namespaces:
        if not namespace.isidentifier():
            raise ValueError(f"Invalid namespace: “{namespace}”")
        if NAMESPACE_SEP in namespace:
            raise ValueError(f"Namespace contains separator: “{namespace}”")

@export
def unpack_ns(nskey):
    """ Unpack a namespaced key into a set of namespaces and a key name.
        
        To wit: if the namespaced key is “yo:dogg:i-heard”, calling “unpack_ns(…)”
        on it will return the tuple ('i-heard', ('yo', 'dogg'));
        
        If the key is not namespaced (like e.g. “wat”) the “unpack_ns(…)”
        call will return the tuple ('wat', tuple()).
    """
    *namespaces, key = nskey.split(NAMESPACE_SEP)
    return key, tuple(namespaces)

@export
def pack_ns(key, *namespaces):
    """ Pack a key and a set of (optional) namespaces into a namespaced key.
        
        To wit: if called as “pack_ns('i-heard, 'yo', 'dogg')” the return
        value will be the string "yo:dogg:i-heard".
        
        If no namespaces are provided (like e.g. “pack_ns('wat')”)
        the return value will be the string "wat".
    """
    return NAMESPACE_SEP.join(chain(namespaces, tuplize(key, expand=False)))

@export
def get_ns(nskey):
    """ Get the namespace portion of a namespaced key as a packed string. """
    return nskey.rpartition(NAMESPACE_SEP)[0]

@export
def compare_ns(iterone, itertwo):
    """ Boolean predicate to compare a pair of namespace iterables, value-by-value """
    for one, two in zip_longest(iterone,
                                itertwo,
                                fillvalue=NoDefault):
        if one != two:
            return False
    return True

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_one():
        pass # INSERT TESTING CODE HERE, pt. I
    
    #@inline
    def test_two():
        pass # INSERT TESTING CODE HERE, pt. II
    
    #@inline.diagnostic
    def show_me_some_values():
        pass # INSERT DIAGNOSTIC CODE HERE
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())

