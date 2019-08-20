# -*- coding: utf-8 -*-
from __future__ import print_function

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
class TomlFile(FileBase, Flat, appname=toml_appname, filename=toml_filename):
    
    def loads(self, text):
        self.dictionary = toml.loads(text)
    
    def dumps(self):
        return toml.dumps(self.dictionary)

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
    
    print(f"»    self.dictionary = {toml_file.dictionary}")
    print(f"»      self.filepath = {toml_file.filepath}")
    print(f"»    self.filesuffix = {toml_file.filesuffix}")
    print()
    
    # TomlFile.find_file(user_dirs=set())

if __name__ == '__main__':
    test()
