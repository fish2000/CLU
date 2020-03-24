# -*- coding: utf-8 -*-
from __future__ import print_function

import sys, os

from clu.constants import consts
from clu.stdio import TermSize, linebreak

def show():
    """ Prettyprint the module lookup results """
    from clu.repl.modules import compare_module_lookups_for_all_things
    from clu.repl.modules import isplural
    from clu.repl.columnize import columnize
    from clu.scripts import ansicolors as colors
    from clu.repl.ansi import (print_ansi as output,
                               print_ansi_centered as center,
                               print_ansi_name_value as keyval)
    
    # 1) Look up all exported items in all CLU modules;
    # 2) compare the module name of each item, as determined,
    #    to the actual module from whence it camel;
    # 3) Pack the results into named tuples of tuples of named tuples –
    # 4) – the final product of which you see before you one line further down:
    results, mismatches = compare_module_lookups_for_all_things()
    
    # Calculate the longest qualified module name – a value used to align
    # multi-line name-value pairs:
    most = max(len(result.modulename) for result in results.result_records)
    
    # Retrieve the terminal character width of the parent terminal device:
    width = TermSize().width
    
    # Header + footer:
    header0 = f'MODULE LOOKUPS ({results.total} performed)'
    header1 = f'MISMATCHES FOUND (of {mismatches.total} total)'
    footer0 = f'MISMATCHES: {len(mismatches.mismatch_records)} (of {mismatches.total} total)'
    footer1 = f'FAILURE RATE: {mismatches.failure_rate}'
    
    # Print header and upper borders:
    center(filler='–', color=colors.gray)
    center(header0,    color=colors.yellow)
    linebreak()
    
    # Iterate through the module-export lookup result records:
    for result in results.result_records:
        
        # Columnize each modules’ exported item list,
        # according to the display and the list length:
        count = len(result.thingnames)
        columns = columnize(result.thingnames, display_width=width,
                                               ljust=True)
        
        # Print the module name, and its count of
        # exported items:
        keyval(f"{result.modulename}",
               f"{count} exported thing{isplural(count)}",
                                               most=most)
        linebreak()
        
        # Print out the columnized exported-item list:
        output(columns,                        color=colors.green)
        linebreak()
    
    # Print section-separating header (ending the export list
    # section, commencing the lookup-mismatch table section):
    center(header1,    color=colors.yellow)
    linebreak()
    
    # Iterate through the exported-item module-mismatch records:
    for mismatch in mismatches.mismatch_records:
        
        # Format and print:
        #   * the mismatch-record index number;
        #   * the item name;
        #   * the names of the incongruent modules,
        #     each as was determined as containing
        #     the item in question –
        #   ≠ using the length of the longest-known
        #     qualified module name, “most”:
        idx = f"{mismatch.idx}"
        keyval(f"{mismatch.thingname} [{idx.zfill(2)}]",
               f"{mismatch.which} ≠ {mismatch.determine}",
                       most=most)
    
    linebreak()
    
    # Print footer:
    center(footer0,    color=colors.cyan)
    center(footer1,    color=colors.cyan)
    center(filler='–', color=colors.gray)

def main():
    """ Main CLI entry point for exported-item module listing """
    # Show ’em:
    show()
    
    # At one point, there was an actual reason
    # for this next bit being here, I recall:
    if consts.DEBUG:
        print()
        print(f"")
    
    # Return POSIX for “all is well”:
    return os.EX_OK

if __name__ == '__main__':
    sys.exit(main())