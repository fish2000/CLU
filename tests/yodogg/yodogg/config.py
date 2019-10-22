# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime

from clu.config.env import EnvBase
from clu.config.fieldtypes import fields
from clu.config.formats import JsonFileBase, TomlFileBase
from clu.config.settings import Schema
from clu.importing import initialize_types

from .exporting import Exporter

import sys
from pprint import pprint
pprint(sys.path)

appname = 'yodogg'
Module, Finder, Loader = initialize_types(appname, 'modules')

pprint(sys.meta_path)

exporter = Exporter(path=__file__)
export = exporter.decorator()
 
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
        
        releasedate = fields.DateTime(default=datetime.utcnow)
        
        author = fields.String("Alexander Böhn")
        copyright = fields.String(f"{title.default} © {releasedate.default} {author.default}")
        considerations = fields.String()
    
    with fields.ns('yodogg'):
        
        iheard = fields.String("…I heard")
        youlike = fields.String("you like:")
        andalso = fields.Tuple(value=fields.String("«also»", allow_none=False))

export(Module, name='Module')
export(Finder, name='Finder')
export(Loader, name='Loader')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
