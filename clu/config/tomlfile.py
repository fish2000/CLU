# -*- coding: utf-8 -*-
from __future__ import print_function

import toml

from clu.constants.consts import PROJECT_NAME
from clu.config.base import Flat, Nested
from clu.config.filebase import FileBase
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class TomlFileBase(FileBase, Nested):
    
    def loads(self, text):
        """ Load nested namespaced dictionary data from a TOML-encoded string """
        self.tree = toml.loads(text)
    
    def dumps(self):
        """ Dump a TOML-encoded string from nested namespaced dictionary data """
        return toml.dumps(self.tree)

toml_appname  = PROJECT_NAME
toml_filename = f'{PROJECT_NAME}-config.toml'

@export
class TomlFile(TomlFileBase, appname=toml_appname,
                            filename=toml_filename):
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
