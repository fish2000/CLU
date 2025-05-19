#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import shlex

def actually_print_ansidocs(dotpath):
    """ This function prints the ANSI docs directly to standard output,
        formatting accordingly (as in, no ANSI if we can’t ANSI)
    """
    from clu.naming import qualified_import
    from clu.repl.ansi import DocFormat
    from importlib import import_module
    ansidocs = DocFormat()
    
    # Attempt to import it:
    try:
        thing = qualified_import(dotpath)
    except ValueError:
        thing = import_module(dotpath)
    except AttributeError as error:
        error_string = str(error)
        print(f"[ERROR] {error_string}", file=ansidocs.iohandle)
        sys.exit(os.EX_CONFIG)
    
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
    # sys.argv.append('clu.exporting.Exporter')
    # sys.argv.append('clu.repl.ansi.Text')
    sys.argv.append('numpy.puke')
    sys.exit(ansidocs_command())