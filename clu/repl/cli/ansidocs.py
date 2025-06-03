#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import shlex

from clu.repl.ansi import DocFormat
ansidocs = DocFormat()

def actually_print_ansidocs(dotpath):
    """ This function prints the ANSI docs directly to standard output,
        formatting accordingly (as in, no ANSI if we can’t ANSI)
    """
    from clu.naming import qualified_import
    from importlib import import_module
    
    # Attempt to import it:
    try:
        thing = qualified_import(dotpath, recurse=True)
    except ValueError:
        thing = qualified_import(dotpath)
    except AttributeError as error:
        error_string = str(error)
        print(f"[ERROR] {error_string}", file=ansidocs.iohandle)
        sys.exit(os.EX_CONFIG)
    
    # This goes directly to stdout:
    ansidocs(thing)

def ansidocs_command():
    """ Print out the ANSI-ified docstring for the given thing(s) """
    from clu.constants import consts
    
    command = " ".join(sys.argv)
    executable, *dotpaths = shlex.split(command)
    
    # If we’re debuggin’ lets’s talk about what we got:
    if consts.DEBUG:
        alldotpaths = " ".join(dotpaths)
        print(f"EXECUTABLE: {executable}")
        print(f"DOTPATHS: {alldotpaths}")
        print()
    
    # The actual dirty work
    for dotpath in dotpaths:
        actually_print_ansidocs(dotpath)
    
    # Return nice-nice for my POSI(X)ES:
    return os.EX_OK

if __name__ == '__main__':
    sys.exit(ansidocs_command())