# -*- coding: utf-8 -*-
from __future__ import print_function
from abc import abstractmethod as abstract

import os
import sys

from clu.constants.consts import PROJECT_NAME
from clu.constants.enums import System, SYSTEM
from clu.config.base import AppName, NamespacedMutableMapping
from clu.fs.appdirectories import AppDirs
from clu.fs.filesystem import TemporaryName, Directory
from clu.fs import pypath
from clu.predicates import isiterable, tuplize
from clu.typology import isvalidpath
from clu.exporting import ValueDescriptor, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class FileName(AppName):
    
    @classmethod
    def __init_subclass__(cls, filename=None, **kwargs):
        """ Transform the “filename” class-keyword into “filename” and “filesuffix”
            read-only descriptor values
        """
        super(FileName, cls).__init_subclass__(**kwargs)
        cls.filename = ValueDescriptor(filename)
        cls.filesuffix = ValueDescriptor((filename is not None) and \
                         os.path.splitext(filename)[1].lstrip(os.extsep) or None)
    
    def __init__(self, *args, **kwargs):
        """ Stub __init__(…) method, throwing a lookup error for subclasses
            upon which the “filename” value is None
        """
        if type(self).filename is None:
            raise LookupError("Cannot instantiate a base config class "
                              "(filename is None)")
    
    @staticmethod
    def systems():
        """ Return a set of the valid “clu.constants.enums.System” enum members
            for the current platform
        """
        out = { SYSTEM }
        if SYSTEM is System.DARWIN:
            out |= { System.LINUX2 }
        return out
    
    @staticmethod
    def sys_path_dirs():
        """ Return a tuple of “clu.fs.filesystem.Directory” instances, each
            corresponding to one of the valid entries in the “sys.path” list
        """
        pypath.remove_invalid_paths()
        return tuple(Directory(p) for p in sys.path if os.path.isdir(p))
    
    @classmethod
    def site_dirs(cls):
        """ Return a set of “clu.fs.filesystem.Directory” instances pointing
            to the filesystem locations of site- (aka system-) config directories
        """
        if 'XDG_CONFIG_DIRS' in os.environ:
            xdgs = os.environ.get('XDG_CONFIG_DIRS')
            dirs = (Directory(xdg) for xdg in xdgs.split(os.pathsep))
            sdirs = set(d.subdirectory(cls.appname) for d in dirs)
        else:
            sdirs = set()
        for system in cls.systems():
            appdir = AppDirs(appname=cls.appname, system=system)
            sdirs |= { appdir.site_config }
        return sdirs
    
    @classmethod
    def user_dirs(cls):
        """ Return a set of “clu.fs.filesystem.Directory” instances pointing
            to the filesystem locations of user-configuration directories
        """
        if 'XDG_CONFIG_HOME' in os.environ:
            xdg = os.environ.get('XDG_CONFIG_HOME')
            udirs = set(tuplize(Directory(xdg).subdirectory(cls.appname)))
        else:
            udirs = set()
        for system in cls.systems():
            appdir = AppDirs(appname=cls.appname, system=system)
            udirs |= { appdir.user_config }
        return udirs
    
    @classmethod
    def find_file(cls, filename=None, *, extra_site_dirs=None,
                                         extra_user_dirs=None,
                                         search_sys_path=False):
        """ Search available directories for the named file """
        file_name = filename or cls.filename
        site_dirs = cls.site_dirs()
        user_dirs = cls.user_dirs()
        
        if isiterable(extra_site_dirs):
            site_dirs.update(extra_site_dirs)
        if isiterable(extra_user_dirs):
            user_dirs.update(extra_user_dirs)
        
        root_dir = None
        # Search site directories first:
        for site_dir in site_dirs:
            if site_dir.exists:
                if file_name in site_dir:
                    root_dir = site_dir
                    break
        # Then possibly try “sys.path”:
        if search_sys_path:
            for syspath_dir in cls.sys_path_dirs():
                if syspath_dir.exists:
                    if file_name in syspath_dir:
                        root_dir = syspath_dir
                        break
        # Then search user directories:
        for user_dir in user_dirs:
            if user_dir.exists:
                if file_name in user_dir:
                    root_dir = user_dir
                    break
        if root_dir is None:
            raise FileNotFoundError(f"Couldn’t find config file {file_name}")
        return Directory(root_dir.realpath()).subpath(file_name)

@export
class FileBase(NamespacedMutableMapping, FileName):
    
    """ The FileBase abstract base class furnishes two methods:
        
            • “dump(…)” and
            • “load(…)”;
        
        … and defines two abstract methods that are called by
        the above two definitions:
        
            • “dumps(…)” and
            • “loads(…)”.
        
        … Anyone who has serialized or deserialized anything at
        all with Python – JSON, YAML, TOML, plists, pickles,
        msgpacks, protobufs, bencodes… whatevs – in the last 15
        years, will no doubt recognize these method names and 
        will know immediately what they do. If in case, somehow,
        you don’t know, lookit the docstrings for the methods
        themselves, doggie. Yes.
    """
    
    def __init__(self, filepath=None, *args, **kwargs):
        """ FileBase __init__(…):
            
            Keyword Arguments:
                • filepath          (default: None)*
                • filename          (default: None)
                • extra_site_dirs   (default: None)
                • extra_user_dirs   (default: None)
                • search_sys_path   (default: False)
            
            * The “filepath” arg will be ignored if “FileName.find_file(…)”
              returns a valid path to a file
        """
        filename        = kwargs.pop('filename', None)
        extra_site_dirs = kwargs.pop('extra_site_dirs', None)
        extra_user_dirs = kwargs.pop('extra_user_dirs', None)
        search_sys_path = kwargs.pop('search_sys_path', False)
        
        try:
            super(FileBase, self).__init__(*args, **kwargs)
        except TypeError:
            super(FileBase, self).__init__()
        
        try:
            self.filepath = type(self).find_file(filename=filename,
                                                 extra_user_dirs=extra_user_dirs,
                                                 extra_site_dirs=extra_site_dirs,
                                                 search_sys_path=search_sys_path)
        except FileNotFoundError:
            self.filepath = filepath
        
        if isvalidpath(self.filepath):
            self.load()
    
    def load(self, filepath=None):
        """ Load from a file, either from a specified “filepath,” or
            from the internally-discovered path to the configuration file
        """
        if filepath is None:
            filepath = self.filepath
        if not isvalidpath(filepath):
            raise FileNotFoundError("No valid filepath available for load()")
        
        with open(filepath, "r") as handle:
            loaded = handle.read()
        
        return self.loads(loaded)
    
    @abstract
    def loads(self, text):
        """ Load a datatype-specific namespaced dictionary from
            arbitrary encoded string data
        """
        ...
    
    def dump(self, filepath=None):
        """ Dump to a file, either to the specified “filepath,” or
            to the internally-discovered path to the configuration file
        """
        if filepath is None:
            filepath = self.filepath
        if filepath is None:
            raise FileNotFoundError("No valid filepath available for dump()")
        
        dumped = self.dumps()
        if not dumped:
            return dumped
        
        with TemporaryName(prefix="filebase-dump-",
                           suffix=type(self).filesuffix,
                           randomized=True) as tdmp:
            assert tdmp.write(dumped)
            assert tdmp.copy(filepath)
        
        assert isvalidpath(filepath)
        return dumped
    
    @abstract
    def dumps(self):
        """ Dump a datatype-specific encoded string data out from
            the internal namespaced dictionary
        """
        ...

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
