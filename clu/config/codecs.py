# -*- coding: utf-8 -*-
from __future__ import print_function
import json

from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class Encoder(json.JSONEncoder):
    
    def default(self, obj):
        return super().default(self, obj)

@export
class Decoder(json.JSONDecoder):
    
    def object_hook(self, obj):
        pass

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
