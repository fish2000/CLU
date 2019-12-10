# -*- coding: utf-8 -*-
from __future__ import print_function

import toml

from clu.constants.consts import PROJECT_NAME
from clu.config.defg import FrozenNested
from clu.config.filebase import FileBase
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class TomlFileBase(FileBase, FrozenNested):
    
    """ The base class for “clu.config.tomlfile.TomlFile”. Override this
        class in your own project to use TOML file data in your Schema
        pipelines as a NamespacedMutableMapping – q.v. the docstring for
        “clu.config.tomlfile.TomlFile” sub.
        
        This class uses two mixins: both “clu.config.base.AppName” and
        “clu.config.filebase.FileName” are part of its inheritance chain.
        The “AppName” mixin acts on the “appname” class keyword, and the
        “FileName” mixin acts on the “filename” class keyword (furnishing
        many related class methods). 
    """
    
    def loads(self, loaded):
        """ Load nested namespaced dictionary data from a TOML-encoded string """
        self.tree = toml.loads(loaded)
    
    def dumps(self):
        """ Dump a TOML-encoded string from nested namespaced dictionary data """
        return toml.dumps(self.tree)

toml_appname  = PROJECT_NAME
toml_filename = f'{PROJECT_NAME}-config.toml'

@export
class TomlFile(TomlFileBase, appname=toml_appname,
                            filename=toml_filename):
    
    """ A representation of a TOML file’s data as a NamespacedMutableMapping.
        
        This class is specifically germane to the CLU project – note
        that the “appname” and “filename” class keywords are used to
        assign values that are CLU-specific.
        
        CLU users who wish to use TOML files as NamespacedMutableMappings
        in their own projects should create a subclass of TomlFileBase of
        their own. Like this one, it needs to assign both the “appname”
        and the “filename” class keywords; it is unnecessary (but OK!) to
        define further methods, properties, class constants, and whatnot.
    """
    pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from clu.constants import consts
    from clu.repl.columnize import columnize
    from clu.fs.filesystem import Directory
    from clu.predicates import tuplize
    from pprint import pformat
    # import sys
    
    # print(toml.__file__)
    # sys.exit()
    
    WIDTH = consts.TEXTMATE and max(consts.SEPARATOR_WIDTH, 125) \
                                 or consts.SEPARATOR_WIDTH
    
    project_path = Directory(consts.PROJECT_PATH)
    tests = project_path.parent().subdirectory('tests')
    cfgs = tests.subdirectory('data').subdirectory('config')
    
    toml_file = TomlFile(extra_user_dirs=tuplize(cfgs))
    
    print()
    
    print("» TOML FILE INSTANCE ATTRIBUTES:")
    # pprint(dir(toml_file))
    print()
    print(columnize(dir(toml_file), displaywidth=WIDTH))
    # print()
    
    print(f"»        cls.appname = {toml_file.appname}")
    print(f"»       cls.filename = {toml_file.filename}")
    print()
    
    print(f"»          self.tree = {pformat(toml_file.tree)}")
    print(f"»      self.filepath = {toml_file.filepath}")
    print(f"»    self.filesuffix = {toml_file.filesuffix}")
    print()
    
    # TomlFile.find_file(user_dirs=set())

if __name__ == '__main__':
    test()
