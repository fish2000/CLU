# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants import consts
from clu.predicates import isiterable, isnormative
from clu.typology import isnumber, isbytes, ispath
from clu.repl.modules import ModuleMap

def show():
    """ Print out all of the constant variables defined in consts.py,
        only nice-looking, and with ANSI
    """
    from clu.naming import qualified_name
    from clu.scripts import ansicolors as colors
    from clu.repl.ansi import (print_ansi_centered as center,
                               print_ansi_name_value as keyval)
    import os
    
    # Mapping interface to the consts module:
    C = ModuleMap(consts)
    
    # Header + footer:
    length = len(C)
    mdname = qualified_name(consts)
    header = f'CONSTS MODULE ({length} consts defined)'
    footer = f'Module: {mdname} » {length} definitions'
    
    # Print header:
    center(filler='–', color=colors.gray)
    center(header,     color=colors.yellow)
    print()
    
    # Calculate the longest constant name,
    # used to align multi-line name-value pairs:
    most = C.most()
    rest = consts.SEPARATOR_WIDTH - (most + 8)
    
    # Calculate the item separator for multi-item consts:
    SEP = ",\n" + (" " * (most + 5))
    
    # Inline function to truncate long members:
    def truncate(iterable): # pragma: no cover
        for item in (str(itx) for itx in iterable):
            if len(item) > rest:
                yield f"“{item[:rest]}…”"
            else:
                yield f"“{item}”"
    
    # Main printing loop:
    for const_name in C:
        const_value = C[const_name]
        
        if isnormative(const_value):
            
            if isbytes(const_value):
                const_value = str(const_value, encoding=consts.ENCODING)
            elif ispath(const_value):
                const_value = os.fspath(const_value)
            
            if const_name.endswith('PATH') and os.pathsep in const_value:
                keyval(const_name, SEP.join(truncate(const_value.split(os.pathsep))),
                                   most=most)
            else:
                keyval(const_name, f"“{const_value}”",
                                   most=most)
        
        elif isiterable(const_value):
            keyval(const_name, SEP.join(truncate(const_value)),
                               most=most)
        
        elif isnumber(const_value):
            keyval(const_name, f"«{const_value!r}»",
                               most=most)
        
        else:
            keyval(const_name, const_value,
                               most=most)
    
    # Print footer:
    print()
    center(footer,     color=colors.cyan)
    center(filler='–', color=colors.gray)

def main():
    """ Main CLI entry point """
    import os
    
    show()
    if consts.DEBUG:
        print()
        print(f"")
    
    return os.EX_OK

if __name__ == '__main__':
    import sys
    sys.exit(main())
