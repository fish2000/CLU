# -*- coding: utf-8 -*-
from __future__ import print_function

import plistlib
import zict

from constants import ENCODING, NoDefault, System
from constants import KeyValueError
from fs import AppDirs
from predicates import attr
from typology import isstring, isbytes
from exporting import Exporter

exporter = Exporter()
export = exporter.decorator()

@export
class CLUInterface(AppDirs):
    
    def __init__(self, appname='clu'):
        """ Initialize with a fixed “appname” parameter `replenv` """
        # use Linux directory layout
        super(CLUInterface, self).__init__(appname=appname,
                                            system=System.LINUX2)
        
        # Create directory if necessary:
        if not self.user_config.exists:
            self.user_config.makedirs()
        
        # Configure zicts:
        self.zfile = zict.File(str(self.user_config), mode='a')
        self.zutf8 = zict.Func(dump=attr(plistlib, 'dumps', 'writePlistToString'),
                               load=attr(plistlib, 'loads', 'readPlistFromString'),
                               d=self.zfile)
        self.zfunc = zict.Func(dump=lambda value: isstring(value) and value.encode(ENCODING) or value,
                               load=lambda value: isbytes(value) and value.decode(ENCODING) or value,
                               d=self.zutf8)

interface = CLUInterface()

@export
def has(key):
    """ Test if a key is contained in the key-value store. """
    return key in interface.zfunc

@export
def count():
    """ Return the number of items in the key-value store. """
    return len(interface.zfunc)

@export
def get(key, default=NoDefault):
    """ Return a value from the ReplEnv user-config key-value store. """
    if default is NoDefault:
        return interface.zfunc[key]
    try:
        return interface.zfunc[key]
    except KeyError:
        return default

@export
def set(key, value):
    """ Set and return a value in the ReplEnv user-config key-value store. """
    if not key:
        raise KeyValueError("Non-Falsey key required (k: %s, v: %s)" % (key, value))
    if not value:
        raise KeyValueError("Non-Falsey value required (k: %s, v: %s)" % (key, value))
    interface.zfunc[key] = value
    return get(key)

@export
def delete(key):
    """ Delete a value from the ReplEnv user-config key-value store. """
    if not key:
        raise KeyValueError("Non-Falsey key required for deletion (k: %s)" % key)
    del interface.zfunc[key]

@export
def iterate():
    """ Return an iterator for the key-value store. """
    return iter(interface.zfunc)

@export
def keys():
    """ Return an iterable with all of the keys in the key-value store. """
    return interface.zfunc.keys()

@export
def values():
    """ Return an iterable with all of the values in the key-value store. """
    return interface.zfunc.values()

@export
def items():
    """ Return an iterable yielding (key, value) for all items in the key-value store. """
    return interface.zfunc.items()


# NO DOCS ALLOWED:
export(interface,           name='interface')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()