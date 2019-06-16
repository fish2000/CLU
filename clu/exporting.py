# -*- coding: utf-8 -*-
from __future__ import print_function

from constants import SINGLETON_TYPES, Enum, unique

def predicates_for_types(*types):
    """ For a list of types, return a list of “isinstance” predicates """
    predicates = []
    for classtype in frozenset(types):
        predicates.append(lambda thing: isinstance(thing, classtype))
    return tuple(predicates)
