# -*- coding: utf-8 -*-
from __future__ import print_function

import plistlib
import zict

from constants import ENCODING, NoDefault, System
from fs import AppDirs
from fs.appdirectories import test
from predicates import attr
from typology import isstring, isbytes
# from replutilities import Exporter

# exporter = Exporter()
# export = exporter.decorator()

# UTILITY STUFF: Exceptions

# @export
class KeyValueError(ValueError):
    pass

# UTILITY STUFF: AppDirs wrapper

# @export
class ReplEnvDirs(AppDirs):
    
    def __init__(self):
        """ Initialize with a fixed “appname” parameter `replenv` """
        # use Linux directory layout
        super(ReplEnvDirs, self).__init__(appname='replenv',
                                          system=System.LINUX2)

renvdirs = ReplEnvDirs()

if not renvdirs.user_config.exists:
    renvdirs.user_config.makedirs()

zfile = zict.File(str(renvdirs.user_config), mode='a')
zutf8 = zict.Func(dump=attr(plistlib, 'dumps', 'writePlistToString'),
                  load=attr(plistlib, 'loads', 'readPlistFromString'),
                  d=zfile)
zfunc = zict.Func(dump=lambda value: isstring(value) and value.encode(ENCODING) or value,
                  load=lambda value: isbytes(value) and value.decode(ENCODING) or value,
                  d=zutf8)

# @export
def has(key):
    """ Test if a key is contained in the key-value store. """
    return key in zfunc

# @export
def count():
    """ Return the number of items in the key-value store. """
    return len(zfunc)

# @export
def get(key, default=NoDefault):
    """ Return a value from the ReplEnv user-config key-value store. """
    if default is NoDefault:
        return zfunc[key]
    try:
        return zfunc[key]
    except KeyError:
        return default

# @export
def set(key, value):
    """ Set and return a value in the ReplEnv user-config key-value store. """
    if not key:
        raise KeyValueError("Non-Falsey key required (k: %s, v: %s)" % (key, value))
    if not value:
        raise KeyValueError("Non-Falsey value required (k: %s, v: %s)" % (key, value))
    zfunc[key] = value
    return get(key)

# @export
def delete(key):
    """ Delete a value from the ReplEnv user-config key-value store. """
    if not key:
        raise KeyValueError("Non-Falsey key required for deletion (k: %s)" % key)
    del zfunc[key]

# @export
def iterate():
    """ Return an iterator for the key-value store. """
    return iter(zfunc)

# @export
def keys():
    """ Return an iterable with all of the keys in the key-value store. """
    return zfunc.keys()

# @export
def values():
    """ Return an iterable with all of the values in the key-value store. """
    return zfunc.values()

# @export
def items():
    """ Return an iterable yielding (key, value) for all items in the key-value store. """
    return zfunc.items()


# export(pytuple,         name='pytuple',         doc="")

# NO DOCS ALLOWED:
# export(Directory)
# export(ENCODING,        name='ENCODING')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
# __all__, __dir__ = exporter.all_and_dir()

# Private (un-exported) inline test function:
# def test():
#     exporter.print_diagnostics(__all__, __dir__)
#
if __name__ == '__main__':
    test()

