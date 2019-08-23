# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime

from clu.config.env import EnvBase
from clu.config.fieldtypes import fields
from clu.config.formats import JsonFileBase, TomlFileBase
from clu.config.settings import Schema

import sys
from pprint import pprint
pprint(sys.path)

from .exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()
 
appname = 'yodogg'
filename_base = f"{appname}."
json_filename = filename_base + "json"
toml_filename = filename_base + "toml"

@export
class Env(EnvBase, appname=appname):
    pass

@export
class JsonFile(JsonFileBase, appname=appname, filename=json_filename):
    pass

@export
class TomlFile(TomlFileBase, appname=appname, filename=toml_filename):
    pass

@export
class MySchema(Schema):
    
    title = fields.String("YoDoggApp",  allow_none=False)
    version = fields.Int(1,             allow_none=False)
    appversion = fields.Float(0.1,      allow_none=False)
    
    with fields.ns('metadata'):
        
        releasedate = fields.DateTime(default=datetime.utcnow,
                                      allow_none=False)
        
        author = fields.String("Alexander Böhn")
        copyright = fields.String(f"{title.default} © {releasedate.default} {author.default}")
        considerations = fields.String()
    
    with fields.ns('yodogg'):
        
        yodogg = fields.String("Yo dogg,")
        iheard = fields.String("I heard")
        andalso = fields.String(f"and: {title.default}")



# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
