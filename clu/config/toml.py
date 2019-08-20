# -*- coding: utf-8 -*-
from __future__ import print_function

import copy
import toml

from clu.constants.consts import PROJECT_NAME
from clu.config.base import Flat, Nested
from clu.config.filebase import FileBase
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

toml_appname  = PROJECT_NAME
toml_filename = f'{PROJECT_NAME}-config.toml'

@export
class TomlFile(FileBase, Nested, appname=toml_appname, filename=toml_filename):
    
    # def __init__(self, *args, **kwargs):
    #     try:
    #         super(TomlFile, self).__init__(*args, **kwargs)
    #     except TypeError:
    #         super(TomlFile, self).__init__()
    #     for arg in args:
    #         if isinstance(arg, Nested):
    #             self.tree = copy.copy(arg.tree)
    
    def loads(self, text):
        """ Load nested namespaced dictionary data from a TOML-encoded string """
        self.tree = toml.loads(text)
    
    def dumps(self):
        """ Dump a TOML-encoded string from nested namespaced dictionary data """
        return toml.dumps(self.tree)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from clu.constants import consts
    from clu.repl.columnize import columnize
    # from pprint import pprint
    
    WIDTH = consts.TEXTMATE and max(consts.SEPARATOR_WIDTH, 125) \
                                 or consts.SEPARATOR_WIDTH
    
    toml_file = TomlFile()
    
    print()
    
    print("» TOML FILE INSTANCE ATTRIBUTES:")
    # pprint(dir(toml_file))
    print()
    print(columnize(dir(toml_file), displaywidth=WIDTH))
    # print()
    
    print(f"»        cls.appname = {toml_file.appname}")
    print(f"»       cls.filename = {toml_file.filename}")
    print()
    
    print(f"»          self.tree = {toml_file.tree}")
    print(f"»      self.filepath = {toml_file.filepath}")
    print(f"»    self.filesuffix = {toml_file.filesuffix}")
    print()
    
    # TomlFile.find_file(user_dirs=set())

if __name__ == '__main__':
    test()
