# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.stdio import TermSize, linebreak
from clu.repl.modules import compare_module_lookups_for_all_things
from clu.repl.modules import isplural
from clu.repl.columnize import columnize
from clu.repl import ansi

from clu.scripts import ansicolors as colors

def show():
    """ Prettyprint the module lookup results """
    results, mismatches = compare_module_lookups_for_all_things()
    
    most = max(len(result.modulename) for result in results.result_records)
    width = TermSize().width
    
    header0 = f'MODULE LOOKUPS ({results.total} performed)'
    header1 = f'MISMATCHES FOUND (of {mismatches.total} total)'
    footer0 = f'MISMATCHES: {len(mismatches.mismatch_records)} (of {mismatches.total} total)'
    footer1 = f'FAILURE RATE: {mismatches.failure_rate}'
    
    ansi.print_ansi_centered(filler='–', color=colors.gray)
    ansi.print_ansi_centered(header0,    color=colors.yellow)
    linebreak()
    
    for result in results.result_records:
        thinglength = len(result.thingnames)
        columns = columnize(result.thingnames, display_width=width,
                                               ljust=True)
        ansi.print_ansi_name_value(f"{result.modulename}",
                                   f"{thinglength} exported thing{isplural(thinglength)}",
                                         most=most)
        linebreak()
        ansi.print_ansi(columns,         color=colors.green)
        linebreak()
    
    ansi.print_ansi_centered(header1,    color=colors.yellow)
    linebreak()
    
    for mismatch in mismatches.mismatch_records:
        idx = f"{mismatch.idx}"
        
        ansi.print_ansi_name_value(f"{mismatch.thingname} [{idx.zfill(2)}]",
                                   f"{mismatch.which} ≠ {mismatch.determine}",
                                         most=most)
    
    linebreak()
    ansi.print_ansi_centered(footer0,    color=colors.cyan)
    ansi.print_ansi_centered(footer1,    color=colors.cyan)
    ansi.print_ansi_centered(filler='–', color=colors.gray)

def main():
    """ Main CLI entry point """
    from clu.constants import consts
    import os
    
    show()
    if consts.DEBUG:
        print()
        print(f"")
    
    return os.EX_OK

if __name__ == '__main__':
    import sys
    sys.exit(main())