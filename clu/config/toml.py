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
class TomlFile(FileBase, appname=PROJECT_NAME, filename=f'{PROJECT_NAME}-config.toml'):
    
    def loads(self, text):
        pass
    
    def dumps(self):
        pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    from pprint import pprint
    
    # print("» SITE DIRS:")
    # pprint(site_dirs)
    # print()
    
    TomlFile.find_file(user_dirs=set())
    

if __name__ == '__main__':
    test()
