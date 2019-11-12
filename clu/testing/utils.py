# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import wraps

from clu.constants.consts import (QUALIFIER,
                                  SEPARATOR_WIDTH,
                                  TEXTMATE)
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
def countfiles(target, suffix=None):
    """ Return a count of all files in the target directory,
        including those found in all subdirectories.
        
        Optionally pass a “suffix” argument to only count files
        matching a specific suffix.
    """
    from clu.fs.misc import suffix_searcher
    from clu.constants.polyfills import walk
    import os
    count = 0
    searcher = suffix_searcher(suffix)
    for root, dirs, files in walk(os.fspath(target)):
        count += len(tuple(filter(searcher, files)))
    return count

WIDTH = TEXTMATE and max(SEPARATOR_WIDTH, 100) or SEPARATOR_WIDTH
asterisks = lambda filler='*': print(filler * WIDTH)
printout = lambda name, value: print("» %25s : %s" % (name, value))

@export
def inline(function):
    """ Function decorator for an individual inline test. Example usage:
            
            def test():
                
                @inline
                def test_one():
                    # ...
                
                @inline
                def test_two():
                    # ...
            
            test_one()
            test_two()
            
            if __name__ == '__main__':
                test()
    """
    from clu.naming import nameof
    from pprint import pprint
    import time
    
    # Get the name of the decorated function:
    name = nameof(function, default='<unnamed>')
    
    @wraps(function)
    def test_wrapper(*args, **kwargs):
        # Print header:
        print()
        print(f"TESTING: “{name}”")
        asterisks('-')
        print()
        
        # Run the wrapped function, timing it:
        t1 = time.time()
        out = function(*args, **kwargs)
        t2 = time.time()
        dt = str((t2 - t1) * 1.00)
        dtout = dt[:(dt.find(QUALIFIER) + 4)]
        
        # Print the results and execution time:
        asterisks('-')
        if out is not None:
            print("RESULTS:")
            pprint(out)
            asterisks('-')
        print(f"Test function “{name}” ran in {dtout}s")
        asterisks('=')
        
        # Return as per the decorated function:
        return out
    
    # Return the test wrapper function:
    return test_wrapper

@export
def stdpout():
    """ Switch the default output stream used by the “pout” module
        to “sys.stdout” from “sys.stderr” using the “logging”
        module internals.
    """
    # N.B. I fucking hate this Javaesque boilerplate-tastic shit
    import logging, pout, sys
    
    # If we’ve been here before we don’t need to bother:
    if not getattr(pout, '__WTF_HAX__', False):
        
        # Step one: pop off the old stderr-bound handler:
        pout.stream.logger.handlers.pop()
        
        # Step two: set up a new logging StreamHandler:
        loghandler = logging.StreamHandler(stream=sys.stdout)
        loghandler.setFormatter(logging.Formatter('%(message)s'))
        pout.stream.logger.addHandler(loghandler)
        pout.stream.logger.propagate = False
        
        # Step three: instantiate a “pout.StderrStream” and root
        # around with that shit to use `sys.stdout`:
        streamy = pout.StderrStream()
        streamy.logger = pout.stream.logger
        streamy.logger.setLevel(logging.DEBUG)
        streamy.logger.handlers[0].setStream(sys.stdout)
        streamy.logger.handlers[0].set_name('stderr')
        streamy.logger.handlers[0].setLevel(logging.DEBUG)
        
        # Step four DONT CROSS THE STREAMS WHATEVER YOU DO
        stdpout.oldstreamy = pout.stream
        pout.stream = streamy
        
        # Step five: doctor the “pout” module reflecting our change:
        pout.__WTF_HAX__ = True
    
    # Step six: return the “pout” module object:
    return pout

def __getattr__(key):
    """ Module __getattr__(…) patches the “pout” module on-demand """
    if key == 'pout':
        return stdpout()
    raise AttributeError(f"module {__name__} has no attribute {key}")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir('pout')