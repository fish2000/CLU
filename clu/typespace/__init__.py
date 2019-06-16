# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import re

from constants import VERBOTEN, cache_from_source
from .namespace import SimpleNamespace, Namespace

import types as thetypes
types = Namespace()
typed = re.compile(r"^(?P<typename>\w+)(?:Type)$")

# Fill a Namespace with type aliases, minus the fucking 'Type' suffix --
# We know they are types because they are in the fucking “types” module, OK?
# And those irritating four characters take up too much pointless space, if
# you asked me, which you implicitly did by reading the comments in my code,
# dogg.

for typename in dir(thetypes):
    if typename.endswith('Type'):
        setattr(types, typed.match(typename).group('typename'),
        getattr(thetypes, typename))
    elif typename not in VERBOTEN:
        setattr(types, typename, getattr(thetypes, typename))

# Substitute our own SimpleNamespace class, instead of the provided version:
setattr(types, 'Namespace',       Namespace)
setattr(types, 'SimpleNamespace', SimpleNamespace)

# Manually set `types.__file__` and related attributes:
setattr(types, '__file__',        __file__)
setattr(types, '__cached__',      cache_from_source(__file__))
setattr(types, '__package__',     os.path.splitext(
                                  os.path.basename(__file__))[0])

__all__ = ('SimpleNamespace', 'Namespace', 'types')
__dir__ = lambda: list(__all__)