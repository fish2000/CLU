# -*- coding: utf-8 -*-
from __future__ import print_function

import plistlib
import zict

from constants import ENCODING, PROJECT_NAME
from constants import NoDefault, System
from constants import KeyValueError
from fs import AppDirs, Directory
from predicates import attr
from typology import isstring, isbytes
from exporting import Exporter

exporter = Exporter()
export = exporter.decorator()

@export
class CLUInterface(AppDirs):
    
    def __init__(self, appname=PROJECT_NAME,
                       datadir=None):
        """ Initialize a key-value store with a default “appname” parameter `clu` –
            q.v. ``clu.constants.consts``, the “PROJECT_NAME” constant supra. –
            and set up all required I/O interfaces based on this name:
        """
        # …also, use the Linux directory layout:
        super(CLUInterface, self).__init__(appname=appname,
                                            system=System.LINUX2)
        
        # Use passed-in “datadir” or “user_config”
        self.datadir = datadir and Directory(datadir) \
                                or self.user_config
        
        # Create the “datadir” directory if necessary:
        if not self.datadir.exists:
            self.datadir.makedirs()
        
        # Configure zicts for key-value I/O:
        self.zfile = zict.File(str(self.datadir), mode='a')
        self.zutf8 = zict.Func(dump=attr(plistlib, 'dumps', 'writePlistToString'),
                               load=attr(plistlib, 'loads', 'readPlistFromString'),
                               d=self.zfile)
        self.zfunc = zict.Func(dump=lambda value: isstring(value) and value.encode(ENCODING) or value,
                               load=lambda value: isbytes(value) and value.decode(ENCODING) or value,
                               d=self.zutf8)
    
    def get_datadir(self):
        return getattr(self, 'datadir', None)
    
    def has(self, key):
        """ Test if a key is contained in this key-value store. """
        return key in self.zfunc
    
    def count(self):
        """ Return the number of items in this key-value store. """
        return len(self.zfunc)
    
    def get(self, key, default=NoDefault):
        """ Return a value from this key-value store. """
        if default is NoDefault:
            return self.zfunc[key]
        try:
            return self.zfunc[key]
        except KeyError:
            return default
    
    def set(self, key, value):
        """ Set and return a value in this key-value store. """
        if not key:
            raise KeyValueError("Non-Falsey key required (k: %s, v: %s)" % (key, value))
        if not value:
            raise KeyValueError("Non-Falsey value required (k: %s, v: %s)" % (key, value))
        self.zfunc[key] = value
        return self.get(key)
    
    def delete(self, key):
        """ Delete a value from this key-value store. """
        if not key:
            raise KeyValueError("Non-Falsey key required for deletion (k: %s)" % key)
        del self.zfunc[key]
    
    def iterate(self):
        """ Return an iterator for this key-value store. """
        return iter(self.zfunc)
    
    def keys(self):
        """ Return an iterable with all of the keys in this key-value store. """
        return self.zfunc.keys()
    
    def values(self):
        """ Return an iterable with all of the values in this key-value store. """
        return self.zfunc.values()
    
    def items(self):
        """ Return an iterable yielding (key, value) for all items in this key-value store. """
        return self.zfunc.items()
    
    def __len__(self):
        return len(self.zfunc)
    
    def __fspath__(self):
        return str(self.datadir.name)
    
    def __bool__(self):
        return len(self) > 0
    
    def __iter__(self):
        return iter(self.zfunc)
    
    def __contains__(self, key):
        return key in self.zfunc
    
    def __getitem__(self, key):
        return self.zfunc[key]

# Module-local singleton key-value instance:
interface = CLUInterface()

@export
def has(key):
    """ Test if a key is contained in the key-value store. """
    return interface.has(key)

@export
def count():
    """ Return the number of items in the key-value store. """
    return interface.count()

@export
def get(key, default=NoDefault):
    """ Return a value from the CLU user-config key-value store. """
    if default is NoDefault:
        return interface.get(key)
    return interface.get(key, default=default)

@export
def set(key, value):
    """ Set and return a value in the CLU user-config key-value store. """
    return interface.set(key, value)

@export
def delete(key):
    """ Delete a value from the CLU user-config key-value store. """
    return interface.delete(key)

@export
def iterate():
    """ Return an iterator for the key-value store. """
    return interface.iterate()

@export
def keys():
    """ Return an iterable with all of the keys in the key-value store. """
    return interface.keys()

@export
def values():
    """ Return an iterable with all of the values in the key-value store. """
    return interface.values()

@export
def items():
    """ Return an iterable yielding (key, value) for all items in the key-value store. """
    return interface.items()


# NO DOCS ALLOWED:
export(interface,           name='interface')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()