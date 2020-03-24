# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import lru_cache

import sys
import platform

from clu.constants.consts import ENCODING
from clu.constants.polyfills import Enum, unique

onecache = lambda function: lru_cache(maxsize=1, typed=True)(function)

@unique
class System(Enum):
    
    """ An enumeration class for dealing with the name of the
        underlying operating system upon which we are running.
    """
    
    DARWIN = 'Mac'
    WIN32 = 'Windows'
    LINUX = 'Linux'
    LINUX2 = ''
    
    @classmethod
    @onecache
    def determine(cls):
        """ Determine the System value for the current platform """
        if sys.platform.startswith('java'):
            os_name = platform.java_ver()[3][0]
            for system in cls:
                if os_name.startswith(system.os_name):
                    return system
        return cls.from_string(sys.platform)
    
    @classmethod
    def from_string(cls, string):
        """ Retrieve a System value by name (case-insensitively) """
        folded = str(string).casefold()
        for system in cls:
            if system.sys_name == folded:
                return system
        raise ValueError(f"System not found: {string!s}")
    
    @classmethod
    def match(cls, value):
        """ Match a system to a value – the nature of which can be:
                
                • a string (unicode or bytes-type) naming the system;
                • an existing “System” enum-member value; or
                • an arbitrary alternative enum-member value.
            
            … The matched system is returned. If no match is found,
            a ValueError will be raised.
        """
        if type(value) is cls:
            return value
        if Enum in type(value).__mro__:
            return value
        if type(value) in (bytes, bytearray):
            return cls.from_string(str(value, encoding=ENCODING))
        return cls.from_string(value) # Assume string as last resort
    
    @classmethod
    def all(cls):
        """ Get a generator over all System values """
        yield from cls
    
    @classmethod
    def unixes(cls):
        """ Get a generator over the UNIX-based System values """
        for system in cls.all():
            if system.is_unix_based:
                yield system
    
    def to_string(self):
        """ A given System value’s name """
        return str(self.name)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.name, encoding=ENCODING)
    
    def __repr__(self):
        return self.to_string()
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __hash__(self):
        return hash(self.to_string())
    
    @property
    def os_name(self):
        """ A given System value’s “os_name” (as reported when
            running within a java-based environment e.g. Jython)
        """
        return str(self.value)
    
    @property
    def sys_name(self):
        """ A given System value’s name, lowercased """
        return self.to_string().casefold()
    
    @property
    def is_current(self):
        """ A boolean value expressing if a given System value
            represents the current running operating system
        """
        return self is type(self).determine()
    
    @property
    def is_unix_based(self):
        """ A boolean value expressing if a given System value
            represents a UNIX-based operating system
        """
        return self != type(self).WIN32

@unique
class CSIDL(Enum):
    
    """ An enumeration encapsulating Windows CSIDLs. """
    # … which I have no idea WTF those actually are
    
    APPDATA         = ('AppData',        26)
    COMMON_APPDATA  = ('Common AppData', 35)
    LOCAL_APPDATA   = ('Local AppData',  28)
    
    @classmethod
    def for_name(cls, name):
        """ Retrieve a CSIDL by name (case-insensitively) """
        folded = str(name).casefold()
        for csidl in cls:
            if folded in (nm.casefold() for nm in (csidl.name,
                                                   csidl.fullname)):
                return csidl
        raise LookupError(f"No CSIDL found named {name!s}")
    
    def __init__(self, *args):
        self.shell_folder_name, self.const = args
    
    @property
    def fullname(self):
        """ A CSIDL’s “full name” – which is basically of the form “CSIDL_NAME_STRING” """
        return "%s_%s" (type(self).__name__, self.name)
    
    def to_string(self):
        """ A given CSIDL’s full name """
        return str(self.fullname)
    
    def to_int(self):
        """ A given CSIDL’s integer value """
        return int(self.const)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.to_string(), encoding=ENCODING)
    
    def __index__(self):
        return self.to_int()
    
    def __hash__(self):
        return hash(self.to_string())

SYSTEM = System.determine()
