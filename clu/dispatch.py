# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

import atexit
import signal
import sys

from clu.config.abc import functional_and
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# The master list of exit-handle functions:
exithandles = []

# The list of signals to which we’ll be listening:
signals = (signal.SIGHUP,
           signal.SIGQUIT,
           signal.SIGTERM)

def wraphandler(function):
    """ Wrap a signal handler in a system-exit function """
    @wraps(function)
    def wrapper(*args): # pragma: no cover
        atexit.unregister(function)
        out = not function(*args)
        sys.exit(int(out))
    return wrapper

def bindhandles():
    """ Freshly bind all exit handles listed in “clu.dispatch.exithandles” """
    # If there’s a handle set already registered with “atexit”,
    # unregister it first:
    if callable(bindhandles.last):
        atexit.unregister(bindhandles.last)
    
    # Create a new callable handle set from the function list:
    handles = functional_and(*exithandles)
    
    # Register the handle set with “atexit”:
    atexit.register(handles, signal.SIGSTOP, None)
    
    # Register the handle set with all specified signals:
    for sig in signals:
        signal.signal(sig, wraphandler(handles))
    
    # Stow the handle set instance for possible unregistration:
    bindhandles.last = handles

# The handle-set memo:
bindhandles.last = None

@export
def signal_for(signum):
    """ Return the signal enum value for a given signal number """
    for sig in signal.Signals:
        if sig.value == int(signum):
            return sig
    return signal.SIG_DFL

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
    local_exithandles = list(exithandles)
    for function in local_exithandles:
        exithandles.remove(function)
    if len(local_exithandles) > 0:
        bindhandles()

@export
def nhandles():
    """ Return the number of registered exit-handle functions """
    return len(exithandles)

@export
def trigger(send=signal.SIGSTOP, frame=None):
    """ Run and unregister all exit handle functions without exiting """
    if bindhandles.last is None:
        return False
    handles = bindhandles.last.clone()
    unregister_all()
    out = True
    for handle in handles:
        try:
            out &= handle(send, frame)
        except SystemExit: # pragma: no cover
            pass
    return out

@export
def shutdown(send=signal.SIGSTOP, frame=None):
    """ Run all exit handles, and commence an orderly shutdown """
    atexit.unregister(bindhandles.last)
    out = not trigger(send, frame)
    sys.exit(int(out))

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    assert not trigger()
    assert signal_for(-666) == signal.SIG_DFL
    
    @exithandle
    def xhandle0(signum, frame=None):
        print("Entering xhandle0")
        sig = signal_for(signum)
        print(f"Received signal: {sig.name} ({sig.value})")
        return True
    
    @exithandle
    def xhandle1(signum, frame=None):
        print("Entering xhandle1")
        sig = signal_for(signum)
        print(f"Received signal: {sig.name} ({sig.value})")
        return True
    
    @exithandle
    def xhandle2(signum, frame=None): # pragma: no cover
        print("Entering xhandle1")
        sig = signal_for(signum)
        print(f"Received signal: {sig.name} ({sig.value})")
        return True
    
    # unregister:
    assert unregister(xhandle2) is xhandle2
    
    # Won’t register an already-registered handle:
    exithandle(xhandle1)
    
    global exithandles
    assert len(exithandles) == 2
    
    print("Triggering…")
    assert trigger()
    assert len(exithandles) == 0
    
    @exithandle
    def xhandleX(signum, frame=None):
        print("Entering xhandleX")
        sig = signal_for(signum)
        print(f"Received signal: {sig.name} ({sig.value})")
        return True
    
    assert len(exithandles) == 1
    print("About to exit function test()…")
    return 0

if __name__ == '__main__':
    assert test() == 0
    shutdown()