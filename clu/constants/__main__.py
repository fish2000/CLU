# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants import consts
from clu.predicates import isiterable, isnormative
from clu.typology import isnumber, isbytes, ispath
from clu.repl import ansi

from clu.scripts import ansicolors as colors

def show():
    """ Print out all of the constant variables defined in consts.py,
        only nice-looking, and with ANSI
    """
    from clu.naming import qualified_name
    import os
    
    # Header + footer:
    length = len(consts.__all__)
    mdname = qualified_name(consts)
    header = f'CONSTS MODULE ({length} consts defined)'
    footer = f'Module: {mdname}'
    
    # Print header:
    ansi.print_ansi_centered(filler='–', color=colors.gray)
    ansi.print_ansi_centered(header,     color=colors.yellow)
    print()
    
    # Calculate the longest constant name,
    # used to align multi-line value outputs and name-value pairs:
    most = max(len(name) for name in consts.__all__)
    
    G = vars(consts)
    SEP = ",\n" + (" " * (most + 5))
    
    for const_name in consts.__all__:
        const_value = G[const_name]
        if isnormative(const_value):
            if isbytes(const_value):
                const_value = str(const_value, encoding=consts.ENCODING)
            elif ispath(const_value):
                const_value = os.fspath(const_value)
            if const_name.endswith('PATH') and os.pathsep in const_value:
                ansi.print_ansi_name_value(const_name, const_value.replace(os.pathsep, SEP), most=most)
            else:
                ansi.print_ansi_name_value(const_name, f"“{const_value}”", most=most)
        elif isiterable(const_value):
            ansi.print_ansi_name_value(const_name, SEP.join(f"“{value!s}”" for value in const_value), most=most)
        elif isnumber(const_value):
            ansi.print_ansi_name_value(const_name, f"«{const_value!r}»", most=most)
        else:
            ansi.print_ansi_name_value(const_name, const_value, most=most)
    
    # Print footer:
    print()
    ansi.print_ansi_centered(footer,     color=colors.cyan)
    ansi.print_ansi_centered(filler='–', color=colors.gray)

def main():
    """ Main CLI entry point """
    import os
    
    if consts.TEXTMATE:
        # Textmate: delegate to “consts.print_all()”:
        consts.print_all()
    else:
        # Show ’em and weep:
        show()
        if consts.DEBUG:
            print()
            print(f"")
    
    return os.EX_OK

if __name__ == '__main__':
    import sys
    sys.exit(main())
