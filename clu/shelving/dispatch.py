# -*- coding: utf-8 -*-
from __future__ import print_function

import atexit
import signal

from clu.config.fieldtypes import functional_and
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

exithandles = []
signals = (signal.SIGTERM,
           signal.SIGHUP,
           signal.SIGINT)

def bindhandles():
    if callable(bindhandles.last):
        atexit.unregister(bindhandles.last)
    handles = functional_and(*exithandles)
    atexit.register(handles, signal.SIGQUIT, None)
    for sig in signals:
        signal.signal(sig, handles)
    bindhandles.last = handles
    return handles

bindhandles.last = None

@export
def exithandle(function):
    """ Register a function with “atexit” and various program-exit signals """
    if function not in exithandles:
        exithandles.append(function)
        bindhandles()
    return function

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
