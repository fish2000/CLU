# -*- coding: utf-8 -*-
from __future__ import print_function

from .exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def youlike():
    return "registries"

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
