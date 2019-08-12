# -*- coding: utf-8 -*-
from __future__ import print_function

def countfiles(target):
    """ Return a count of all files in the target directory,
        including all subdirectories.
    """
    count = 0
    for root, dirs, files in target.walk(followlinks=True):
        count += len(files)
    return count
