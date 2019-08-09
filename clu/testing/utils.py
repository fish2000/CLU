# -*- coding: utf-8 -*-
from __future__ import print_function

def countfiles(directory):
    """  """
    count = 0
    for root, dirs, files in directory.walk(followlinks=True):
        count += len(files)
    return count
