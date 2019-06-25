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
            print("[ERROR] Child failed to umask: %s" % str(exc))
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
        # umask_value = int(str(handle.read(), encoding=ENCODING))
        umask_value = int(handle.read())
    
    # Kill the kid:
    pid, status = os.waitpid(pid, 0)
    
    # What happened?
    print("Child [pid %s] exited, status: %s, umask: %s" % (pid,
                                                            status,
                                                            umask_value))
    
    return umask_value, octalize(umask_value)

def test():
    print("About to fork…")
    mask, octmask = current_umask()
    
    print("Fork is over, value returned is %i [%s]" % (mask, octmask))

if __name__ == '__main__':
    test()
