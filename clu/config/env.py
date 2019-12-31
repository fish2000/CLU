# -*- coding: utf-8 -*-
from __future__ import print_function

import clu.abstract
import os

from clu.constants.consts import ENVIRONS_SEP, NAMESPACE_SEP, PROJECT_NAME, NoDefault
from clu.config.base import NamespacedMutableMapping
from clu.predicates import tuplize
from clu.typology import iterlen
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    pass

if __name__ == '__main__':
    test()
