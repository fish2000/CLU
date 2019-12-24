# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import platform

from clu.constants.consts import ENCODING
from clu.constants.polyfills import Enum, unique

@unique
class System(Enum):
    
    """ An enumeration class for dealing with system names """
    
    DARWIN = 'Mac'
    WIN32 = 'Windows'
    LINUX = 'Linux'
    LINUX2 = ''
    
    @classmethod
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
        for system in cls:
            if system.sys_name == string.casefold():
                return system
        raise ValueError(f"System not found: {string}")
    
    @classmethod
    def match(cls, value):
        if type(value) is cls:
            return value
        if Enum in type(value).__mro__:
            return value
        if type(value) in (bytes, bytearray):
            return cls.from_string(str(value, encoding=ENCODING))
        return cls.from_string(value) # Assume string as last resort
    
    def to_string(self):
        """ A given System value’s name """
        return str(self.name)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.name, encoding=ENCODING)
    
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

@unique
class CSIDL(Enum):
    
    """ An enumeration encapsulating Windows CSIDLs """
    # … which I have no idea WTF those actually are
    
    APPDATA         = ('AppData',        26)
    COMMON_APPDATA  = ('Common AppData', 35)
    LOCAL_APPDATA   = ('Local AppData',  28)
    
    @classmethod
    def for_name(cls, name):
        string_name = str(name)
        for csidl in cls:
            if csidl.name == string_name:
                return csidl
            elif csidl.fullname == string_name:
                return csidl
        raise LookupError(f"No CSIDL found named {string_name}")
    
    def __init__(self, *args):
        self.shell_folder_name, self.const = args
    
    @property
    def fullname(self):
        return "%s_%s" (type(self).__name__, self.name)
    
    def to_string(self):
        return str(self.fullname)
    
    def to_int(self):
        return int(self.const)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.to_string(), encoding=ENCODING)
    
    def __index__(self):
        return self.to_int()

SYSTEM = System.determine()
