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
    from clu.config.keymap import Flat
    from pprint import pprint
    import re, textwrap
    
    flat = Flat()
    
    javaprop_re = re.compile(r"^(?P<name>[\w\.]+): “(?P<value>.*)”", re.IGNORECASE | re.MULTILINE)
    java_source = textwrap.dedent("""
    package ost.%s;
    
    import java.util.Enumeration;
    import java.util.Properties;
    
    public class ShowJavaSystemProperties {
    
        public static void main(String... args) {
            Properties properties = System.getProperties();
            Enumeration names = properties.propertyNames();
            while (names.hasMoreElements()) {
                String name = (String) names.nextElement();
                String value = properties.getProperty(name);
                System.out.println(name + ": “" + value + "”");
            }
        }
    
    }
    """ % exporter.dotpath)
    
    @inline.precheck
    def load_java_system_properties():
        """ Load the Java JDK’s system properties """
        from clu.fs.filesystem import back_tick, TemporaryName
        from clu.naming import dotpath_to_prefix
        
        with TemporaryName(prefix="show-java-system-properties-",
                           suffix="java",
                           randomized=True) as java_file:
            java_file.write(java_source)
            java_path = java_file.realpath()
            output = back_tick(f"java {java_path}")
        
        assert not java_file.exists
        
        for line in output.splitlines():
            match = javaprop_re.match(line)
            if match:
                # BEWARE: dotpath_to_prefix(…) does a casefold():
                name = dotpath_to_prefix(match.group('name'),
                                         sep=NAMESPACE_SEP, end='')
                value = match.group('value')
                flat[name] = value
        
        pprint(flat)
    
    @inline.precheck
    def show_java_system_properties():
        """ Show namespaced Java system properties """
        count = flat.namespace_count()
        plural = count == 1 and '' or 's'
        
        print(f"* {count} namespace{plural} total:")
        print()
        
        for namespace in flat.namespaces():
            namespaces = split_ns(namespace)
            print(f"+ {namespace}:")
            for nskey, value in flat.items(*namespaces):
                bare_key = strip_ns(nskey)
                key = nskey.replace(prefix_for(*namespaces), '', 1)
                print(f"    {key} : “{value}”")
                assert key.endswith(bare_key)
            print()
        
        print("- «unprefixed»:")
        pprint(flat.submap(unprefixed=True), indent=4)
    
    @inline
    def test_one():
        """ Validate a Flat keymap’s namespaces """
        for namespace in flat.namespaces():
            assert validate_ns(*split_ns(namespace))
    
    @inline
    def test_two():
        """ Validate a FrozenFlat keymap’s namespaces """
        for namespace in flat.freeze().namespaces():
            assert validate_ns(*split_ns(namespace))
    
    @inline
    def test_three():
        """ Check “validate_ns(…)” error conditions """
        try:
            validate_ns("yo dogg")
        except ValueError as exc:
            assert "invalid namespace" in str(exc)
        
        try:
            validate_ns("yo:dogg")
        except ValueError as exc:
            assert "namespace contains separator" in str(exc)
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())