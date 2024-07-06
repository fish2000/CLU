# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import chain, zip_longest

import sys

from clu.constants.consts import ENVIRONS_SEP, NAMESPACE_SEP, NoDefault
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
def split_ns(namespaced):
    """ Split a namespaced string into its components """
    return str(namespaced).split(NAMESPACE_SEP)

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
        if NAMESPACE_SEP in namespace:
            raise ValueError(f"namespace contains separator: “{namespace}”")
        if not namespace.isidentifier():
            raise ValueError(f"invalid namespace: “{namespace}”")
    return True

@export
def unpack_ns(nskey):
    """ Unpack a namespaced key into a set of namespaces and a key name.
        
        To wit: if the namespaced key is “yo:dogg:i-heard”, calling “unpack_ns(…)”
        on it will return the tuple ('i-heard', ('yo', 'dogg'));
        
        If the key is not namespaced (like e.g. “wat”) the “unpack_ns(…)”
        call will return the tuple ('wat', tuple()).
    """
    *namespaces, key = split_ns(nskey)
    return key, namespaces

@export
def pack_ns(key, *namespaces):
    """ Pack a key and a set of (optional) namespaces into a namespaced key.
        
        To wit: if called as “pack_ns('i-heard, 'yo', 'dogg')” the return
        value will be the string "yo:dogg:i-heard".
        
        If no namespaces are provided (like e.g. “pack_ns('wat')”)
        the return value will be the string "wat".
    """
    if not namespaces:
        return key
    return NAMESPACE_SEP.join(chain(namespaces, tuplize(key, expand=False)))

@export
def get_ns(nskey):
    """ Get the namespace portion of a namespaced key as a packed string. """
    return nskey.rpartition(NAMESPACE_SEP)[0]

@export
def get_ns_and_key(nskey):
    """ Get the namespace and key portion of a namespaced key, as a packed
        string and a bare key, respectively.
    """
    rpartition = nskey.rpartition(NAMESPACE_SEP)
    return rpartition[0], rpartition[-1]

@export
def compare_ns(iterone, itertwo):
    """ Boolean predicate to compare a pair of namespace iterables, value-by-value """
    for one, two in zip_longest(iterone,
                                itertwo,
                                fillvalue=NoDefault):
        if one != two:
            return False
    return True

# ENVIRONMENT-VARIABLE MANIPULATION API:

@export
def concatenate_env(*namespaces):
    """ Concatenate and UPPERCASE namespaces, per environment variables. """
    return ENVIRONS_SEP.join(namespace.upper() for namespace in namespaces)

@export
def prefix_env(appname, *namespaces):
    """ Determine the environment-variable prefix based on a given
        set of namespaces and the provided “appname” value. Like e.g.,
        for an appname of “YoDogg” and a namespace value of “iheard”,
        the environment variable prefix would work out such that
        a variable with a key value of “youlike” would look like this:
            
            YODOGG_IHEARD_YOULIKE
                                 
            ^^^^^^ ^^^^^^ ^^^^^^^
               |      |      |
               |      |      +––––– mapping key (uppercased)
               |      +–––––––––––– namespaces (uppercased, one value)
               +––––––––––––––––––– app name (uppercased)
    """
    if not appname and not namespaces:
        return ''
    if not appname:
        return concatenate_env(*namespaces) + ENVIRONS_SEP
    if not namespaces:
        return appname.upper() + ENVIRONS_SEP
    return appname.upper() + ENVIRONS_SEP + concatenate_env(*namespaces) + ENVIRONS_SEP

@export
def pack_env(appname, key, *namespaces):
    """ Transform a mapping key, along with optional “namespaces”
        values and the provided “appname” value, into an environment-
        variable name. Like e.g., for an appname of “YoDogg” and
        a namespace value of “iheard”, the environment variable
        prefix would work out such that a variable with a key value
        of “youlike” would look like this:
            
            YODOGG_IHEARD_YOULIKE
                                 
            ^^^^^^ ^^^^^^ ^^^^^^^
               |      |      |
               |      |      +––––– mapping key (uppercased)
               |      +–––––––––––– namespaces (uppercased, one value)
               +––––––––––––––––––– app name (uppercased)
    """
    prefix = prefix_env(appname, *namespaces)
    return f"{prefix}{key.upper()}"

@export
def unpack_env(envkey):
    """ Unpack the appname, possible namespaces, and the key from an environment
        variable key name.
    """
    appname, *namespaces, key = envkey.casefold().split(ENVIRONS_SEP)
    return appname, key, namespaces

@export
def nskey_from_env(envkey):
    """ Repack an environment-variable key name as a packed namespace key. """
    appname, *namespaces, key = envkey.casefold().split(ENVIRONS_SEP)
    return appname, pack_ns(key, *namespaces)

@export
def nskey_to_env(appname, nskey):
    """ Repack a packed namespace key, with a given appname, as an environment
        variable key name.
    """
    key, namespaces = unpack_ns(nskey)
    return pack_env(appname, key, *namespaces)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    from clu.config.keymap import Flat, Nested
    from clu.config.keymap import nestedmaps, flatdict, arbitrary
    from clu.fs.filesystem import which
    from pprint import pprint
    import os, re, textwrap
    
    flat = Flat(flatdict())
    nested = Nested(nestedmaps())
    
    @inline
    def test_flat_validate_ns():
        """ Validate a Flat keymap’s namespaces """
        for namespace in flat.namespaces():
            assert validate_ns(*split_ns(namespace))
    
    @inline
    def test_frozenflat_validate_ns():
        """ Validate a FrozenFlat keymap’s namespaces """
        for namespace in flat.freeze().namespaces():
            assert validate_ns(*split_ns(namespace))
    
    @inline
    def test_nested_validate_ns():
        """ Validate a Nested keymap’s namespaces """
        for namespace in nested.namespaces():
            assert validate_ns(*split_ns(namespace))
    
    @inline
    def test_frozennested_validate_ns():
        """ Validate a FrozenNested keymap’s namespaces """
        for namespace in nested.freeze().namespaces():
            assert validate_ns(*split_ns(namespace))
    
    @inline
    def test_validate_ns_errors():
        """ Check “validate_ns(…)” error conditions """
        try:
            validate_ns("yo dogg")
        except ValueError as exc:
            assert "invalid namespace" in str(exc)
        
        try:
            validate_ns("yo:dogg")
        except ValueError as exc:
            assert "namespace contains separator" in str(exc)
    
    namespaces = ('yo', 'dogg')
    key = 'iheard'
    nskey = "yo:dogg:iheard"
    value = "you like this sort of thing"
    
    @inline
    def test_concatenate_ns():
        assert concatenate_ns(*namespaces) == "yo:dogg"
    
    @inline
    def test_prefix_for():
        assert prefix_for(*namespaces) == "yo:dogg:"
    
    @inline
    def test_strip_ns():
        assert strip_ns(nskey) == "iheard"
    
    @inline
    def test_split_ns():
        assert tuple(split_ns(nskey)) == ('yo', 'dogg', 'iheard')
    
    @inline
    def test_startswith_ns():
        assert startswith_ns(namespaces, ('yo', 'dogg'))
    
    @inline
    def test_unpack_ns():
        assert unpack_ns(nskey) == ('iheard', ['yo', 'dogg'])
    
    @inline
    def test_pack_ns():
        assert pack_ns(key, *namespaces) == "yo:dogg:iheard"
    
    @inline
    def test_get_ns():
        assert get_ns(nskey) == "yo:dogg"
    
    @inline
    def test_get_ns_and_key():
        assert get_ns_and_key(nskey) == ("yo:dogg", 'iheard')
    
    @inline
    def test_compare_ns():
        assert compare_ns(namespaces, ('yo', 'dogg'))
    
    appname = 'testing'
    envkey = "TESTING_YO_DOGG_IHEARD"
    
    @inline
    def test_concatenate_env():
        assert concatenate_env(*namespaces) == "YO_DOGG"
    
    @inline
    def test_prefix_env():
        assert prefix_env(appname, *namespaces) == "TESTING_YO_DOGG_"
    
    @inline
    def test_pack_env():
        assert pack_env(appname, key, *namespaces) == "TESTING_YO_DOGG_IHEARD"
    
    @inline
    def test_unpack_env():
        assert unpack_env(envkey) == (appname, key, list(namespaces))
    
    @inline
    def test_nskey_from_env():
        assert nskey_from_env(envkey) == (appname, pack_ns(key, *namespaces))
    
    @inline
    def test_nskey_to_env():
        assert nskey_to_env(appname, nskey) == "TESTING_YO_DOGG_IHEARD"
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())