#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

octalize = lambda integer: "0o%04o" % integer

def current_umask():
    """ Use a forked child process to retrieve the umask without
        mutating the value held by the current (parent) process.
    """
    
    def umask():
        """ Get the current umask value. """
        mask = os.umask(0)
        os.umask(mask)
        return int(mask)
    
    forkin, forkout = os.pipe()
    pid = os.fork()
    
    if not pid:
        # Child fork:
        
        try:
            os.close(forkin)
            devnull = os.open("/dev/null", os.O_RDONLY)
            
            # Redirect std{in,out,err}:
            os.dup2(devnull, 0) # stdin
            os.dup2(forkout, 1) # stdout
            os.dup2(forkout, 2) # stderr
            
            # Do what we came here to do:
            maskval = b"%i" % umask()
            os.write(1, maskval)
            
        except OSError as exc:
            print(f"[ERROR] Child failed to umask: {exc!s}")
            os._exit(os.EX_OSERR)
        
        finally:
            # Exit without exiting:
            os._exit(os.EX_OK)
    
    # Parent fork:
    os.close(forkout)
    
    # Prepare umask value:
    umask_value = 0
    
    # Reading from forkin yields strings:
    with os.fdopen(forkin) as handle:
        # nonlocal umask_value
        umask_value = int(handle.read())
    
    # Kill the kid:
    pid, status = os.waitpid(pid, 0)
    
    # What happened?
    print(f"Child [pid {pid}] exited, status: {status}, umask: {umask_value}")
    
    return umask_value, octalize(umask_value)

def test():
    print("About to fork…")
    mask, octmask = current_umask()
    
    print(f"Fork is over, value returned is {mask!s} [{octmask}]")

if __name__ == '__main__':
    test()
