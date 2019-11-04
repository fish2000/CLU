# -*- coding: utf-8 -*-
from __future__ import print_function

import plistlib
import zict # type: ignore

from clu.constants.consts import ENCODING, NoDefault
from clu.constants.enums import System
from clu.constants.exceptions import KeyValueError
from clu.fs.appdirectories import AppDirs
from clu.fs.filesystem import Directory
from clu.predicates import attr
from clu.repr import stringify
from clu.typology import isstring, isbytes
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class CLUInterface(AppDirs):
    
    fields = ('appname',        'system', 
                                'version',
                                'version_info',
                                'datadir',
                                'count',
                                'closed',
              
              'site_config',    'site_data',
              'user_cache',     'user_config',
              'user_data',      'user_log',
              'user_state')
    
    def __init__(self, appname=None,
                       version=None,
                       datadir=None):
        """ Initialize a key-value store with a default “appname” parameter `clu` –
            q.v. ``clu.constants.consts``, the “PROJECT_NAME” constant supra. –
            and set up all required I/O interfaces based on this name:
        """
        # Get CLU’s version, if necessary:
        import clu
        
        # …also, use the Linux directory layout:
        super(CLUInterface, self).__init__(appname=appname or clu.__title__,
                                           version=version or clu.__version__,
                                            system=System.LINUX2)
        
        # Use passed-in “datadir” or “user_config”
        self.datadir = datadir and Directory(datadir) \
                                or self.user_config
        
        # Create the “datadir” directory if necessary:
        if not self.datadir.exists:
            self.datadir.makedirs()
            if self.version is not None:
                self.migrate_from_previous()
        
        # Configure zicts for key-value I/O:
        self.zfile = zict.File(str(self.datadir), mode='a')
        self.zutf8 = zict.Func(dump=attr(plistlib, 'dumps', 'writePlistToString'),
                               load=attr(plistlib, 'loads', 'readPlistFromString'),
                               d=self.zfile)
        self.zfunc = zict.Func(dump=lambda value: isstring(value) and value.encode(ENCODING) or value,
                               load=lambda value: isbytes(value) and value.decode(ENCODING) or value,
                               d=self.zutf8)
        
        # WE ARE *NOT* CLOSED
        self._closed = False
    
    @property
    def is_versioned(self):
        return self.version is not None
    
    def migrate_from(self, version):
        pass
    
    def migrate_from_previous(self):
        pass
    
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
        yield from self.zfunc
    
    def update(self, dictish=NoDefault, **updates):
        """ Update the key-value store with key/value pairs and/or an iterator;
            q.v. `dict.update(…)` docstring supra.
        """
        if dictish is NoDefault:
            return self.zfunc.update(**updates)
        return self.zfunc.update(dictish, **updates)
    
    def keys(self):
        """ Return an iterable with all of the keys in this key-value store. """
        return self.zfunc.keys()
    
    def values(self):
        """ Return an iterable with all of the values in this key-value store. """
        return self.zfunc.values()
    
    def items(self):
        """ Return an iterable yielding (key, value) for all items in this key-value store. """
        return self.zfunc.items()
    
    def as_dict(self):
        """ Return a plain dict with the key-value stores’ contents. """
        out = {}
        for key in self.keys():
            out[key] = self[key]
        return out
    
    def close(self):
        """ Attept to close zicts """
        from zict.common import close as closer # type: ignore
        closer(self.zfunc)
        closer(self.zutf8)
        closer(self.zfile)
        self._closed = True
    
    @property
    def closed(self):
        return getattr(self, '_closed', False)
    
    def to_string(self):
        """ Stringify the CLUInterface instance. """
        return stringify(self, type(self).fields)
    
    def __repr__(self):
        return self.to_string()
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.to_string(), encoding=ENCODING)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        # N.B. return False to throw, True to supress:
        if not self.closed:
            self.close()
        return exc_type is None
    
    def __len__(self):
        return len(self.zfunc)
    
    def __fspath__(self):
        return str(self.datadir.name)
    
    def __bool__(self):
        return len(self) > 0
    
    def __iter__(self):
        yield from self.zfunc
    
    def __contains__(self, key):
        return key in self.zfunc
    
    def __getitem__(self, key):
        return self.zfunc[key]
    
    def __setitem__(self, key, value):
        self.zfunc[key] = value
    
    def __delitem__(self, key):
        del self.zfunc[key]

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
    yield from interface

@export
def update(dictish=NoDefault, **updates):
    """ Update the CLU key-value store with key/value pairs, and/or an iterator """
    if dictish is NoDefault:
        return interface.update(**updates)
    return interface.update(dictish, **updates)

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