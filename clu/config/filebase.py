# -*- coding: utf-8 -*-
from __future__ import print_function

import abc
import os

abstract = abc.abstractmethod

from clu.constants.consts import PROJECT_NAME
from clu.constants.enums import System, SYSTEM
from clu.config.base import AppName, NamespacedMutableMapping
from clu.fs.appdirectories import AppDirs
from clu.fs.filesystem import TemporaryName, Directory
from clu.predicates import tuplize
from clu.exporting import ValueDescriptor, Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class FileName(abc.ABC):
    
    @classmethod
    def __init_subclass__(cls, filename=None, **kwargs):
        super(FileName, cls).__init_subclass__(**kwargs)
        cls.filename = ValueDescriptor(filename)
        cls.filesuffix = ValueDescriptor((filename is not None) and \
                         os.path.splitext(filename)[1].lstrip(os.extsep) or None)
    
    def __init__(self, *args, **kwargs):
        if type(self).filename is None:
            raise LookupError("Cannot instantiate a base config class "
                              "(filename is None)")

systems = { SYSTEM }
if SYSTEM is System.DARWIN:
    systems |= { System.LINUX2 }

if 'XDG_CONFIG_DIRS' in os.environ:
    xdgs = os.environ.get('XDG_CONFIG_DIRS')
    dirs = (Directory(xdg) for xdg in xdgs.split(os.pathsep))
    site_dirs = set(d.subdirectory(PROJECT_NAME) for d in dirs)
else:
    site_dirs = set()

if 'XDG_CONFIG_HOME' in os.environ:
    xdg = os.environ.get('XDG_CONFIG_HOME')
    user_dirs = set(tuplize(Directory(xdg).subdirectory(PROJECT_NAME)))
else:
    user_dirs = set()

for system in systems:
    app_dirs = AppDirs(appname=PROJECT_NAME, system=system)
    site_dirs |= { app_dirs.site_config }
    user_dirs |= { app_dirs.user_config }

@export
class FileBase(NamespacedMutableMapping, AppName, FileName):
    
    @classmethod
    def find_file(cls, site_dirs=site_dirs,
                       user_dirs=user_dirs):
        root_dir = None
        # Search site directories first:
        for site_dir in site_dirs:
            if site_dir.exists:
                if cls.filename in site_dir:
                    root_dir = site_dir
                    break
        # Then search user directories:
        for user_dir in user_dirs:
            if user_dir.exists:
                if cls.filename in user_dir:
                    root_dir = user_dir
                    break
        if root_dir is None:
            raise FileNotFoundError(f"Couldn’t find config file {cls.filename}")
        return Directory(root_dir.realpath()).subpath(cls.filename)
    
    def __init__(self, filepath=None, *args, **kwargs):
        try:
            super(FileBase, self).__init__(*args, **kwargs)
        except TypeError:
            super(FileBase, self).__init__()
        try:
            self.filepath = type(self).find_file()
        except FileNotFoundError:
            self.filepath = filepath
        if self.filepath is not None:
            self.load()
    
    def load(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        if filepath is None:
            return
        with open(filepath, "r") as handle:
            filetext = handle.read()
        return self.loads(filetext)
    
    @abstract
    def loads(self, text):
        ...
    
    def dump(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        if filepath is None:
            return ''
        text = self.dumps()
        if not text:
            return text
        with TemporaryName(prefix="filebase-dump-",
                           suffix=type(self).filesuffix,
                           randomized=True) as tdmp:
            assert tdmp.write(text)
            assert tdmp.copy(filepath)
        assert os.path.exists(filepath)
        return text
    
    @abstract
    def dumps(self):
        ...

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from pprint import pprint
    
    print("» SITE DIRS:")
    pprint(site_dirs)
    print()
    
    print("» USER DIRS:")
    pprint(user_dirs)
    print()

if __name__ == '__main__':
    test()
