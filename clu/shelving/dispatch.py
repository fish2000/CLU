# -*- coding: utf-8 -*-
from __future__ import print_function

import atexit
import signal

from clu.config.abc import functional_and
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# The master list of exit-handle functions:
exithandles = []

# The list of signals to which we’ll be listening:
signals = (signal.SIGTERM,
           signal.SIGHUP,
           signal.SIGINT)

def bindhandles():
    """ Freshly bind all exit handles listed in “clu.shelving.dispatch.exithandles” """
    # If there’s a handle set already registered with “atexit”,
    # unregister it first:
    if callable(bindhandles.last):
        atexit.unregister(bindhandles.last)
    
    # Create a new callable handle set from the function list:
    handles = functional_and(*exithandles)
    
    # Register the handle set with “atexit”:
    atexit.register(handles, signal.SIGQUIT, None)
    
    # Register the handle set with all specified signals:
    for sig in signals:
        signal.signal(sig, handles)
    
    # Stow the handle set instance for possible unregistration:
    bindhandles.last = handles

# The handle-set memo:
bindhandles.last = None

@export
def exithandle(function):
    """ Register a function with “atexit” and various program-exit signals """
    if function not in exithandles:
        exithandles.append(function)
        bindhandles()
    return function

@export
def unregister(function):
    """ Unregister a previously-registered exit handle function """
    if function in exithandles:
        exithandles.remove(function)
        bindhandles()
    return function

@export
def unregister_all():
    """ Unregister *all* previously-registered exit handle functions """
    global exithandles
    exithandles = []
    bindhandles()

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
