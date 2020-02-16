# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple

import pickle

from clu.all import import_all_modules
from clu.constants import consts
from clu.exporting import Exporter
from clu.naming import nameof, moduleof
from clu.repl import ansi
from clu.repl.columnize import columnize
from clu.scripts import ansicolors as colors

chevron = colors.red.render("»")
ronchev = colors.gray.render("»")
colon = colors.gray.render(":")

def printout(name, value, most=25):
    """ Format and colorize each segment of the name/value output """
    itemname = colors.brightblue.render(f" {name} ".rjust(most+2))
    itemvalue = colors.gray.render(f" {value}")
    ansi.print_ansi(chevron + itemname + colon + itemvalue, color=colors.nothing)

Mismatch = NamedTuple('Mismatch', ('which',
                                   'determine',
                                   'modulename',
                                   'thingname',
                                   'idx'))

Mismatches = NamedTuple('Mismatches', ('total',
                                       'mismatch_records',
                                       'failure_rate'))

Result = NamedTuple('Result', ('modulename',
                               'thingnames',
                               'idx'))

Results = NamedTuple('Results', ('total',
                                 'modulenames',
                                 'result_records'))

def compare_module_lookups_for_all_things():
    """ Iterate through each exported item, for each exported module,
        and look up the original module of the exported item with both:
            
            1) “pickle.whichmodule(…)” and
            2) “clu.naming.moduleof(…)”
        
        … comparing the results of the two search functions and computing
        the overall results.
    """
    idx = 0
    total = 0
    mismatch_count = 0
    mismatches = []
    results = []
    
    clumodules = import_all_modules(consts.BASEPATH,
                                    consts.PROJECT_NAME,
                                    consts.EXPORTER_NAME)
    assert clumodules
    
    modulenames = tuple(Exporter.modulenames())
    
    for modulename in modulenames:
        exports = Exporter[modulename].exports()
        total += len(exports)
        results.append(Result(modulename, tuple(exports.keys()), idx))
        for name, thing in exports.items():
            whichmodule = pickle.whichmodule(thing, None)
            determination = moduleof(thing)
            try:
                assert determination == whichmodule
            except AssertionError:
                mismatches.append(Mismatch(whichmodule,
                                           determination,
                                           modulename,
                                           nameof(thing),
                                           mismatch_count))
                mismatch_count += 1
            idx += 1
    
    # In practice the failure rate seemed to be around 7.65 %
    failure_rate = 100 * (float(mismatch_count) / float(total))
    assert failure_rate < 10.0 # percent
    
    return Results(idx, modulenames, tuple(results)), \
           Mismatches(total,         tuple(mismatches),
                                           failure_rate)

isplural = lambda integer: integer != 1 and 's' or ''

def show():
    """ Prettyprint the module lookup results """
    results, mismatches = compare_module_lookups_for_all_things()
    
    header0 = f'MODULE LOOKUPS ({results.total} performed)'
    header1 = f'MISMATCHES FOUND (of {mismatches.total} total)'
    footer0 = f'MISMATCHES: {len(mismatches.mismatch_records)} (of {mismatches.total} total)'
    footer1 = f'FAILURE RATE: {mismatches.failure_rate}'
    
    ansi.print_ansi_centered(filler='–', color=colors.gray)
    ansi.print_ansi_centered(header0,    color=colors.yellow)
    print()
    
    most = max(len(result.modulename) for result in results.result_records)
    
    for result in results.result_records:
        thinglength = len(result.thingnames)
        columns = columnize(result.thingnames)
        printout(f"{result.modulename}",
                 f"{thinglength} exported thing{isplural(thinglength)}", most=most)
        print()
        ansi.print_ansi(columns,         color=colors.green)
        print()
    
    ansi.print_ansi_centered(header1,    color=colors.yellow)
    print()
    
    for mismatch in mismatches.mismatch_records:
        idx = f"{mismatch.idx}"
        
        printout(f"{mismatch.thingname} [{idx.zfill(2)}]",
                 f"{mismatch.which} ≠ {mismatch.determine}", most=most)
    
    print()
    ansi.print_ansi_centered(footer0,    color=colors.cyan)
    ansi.print_ansi_centered(footer1,    color=colors.cyan)
    ansi.print_ansi_centered(filler='–', color=colors.gray)

def main():
    """ Main CLI entry point """
    if consts.TEXTMATE:
        print()
        print("NO TEXTMATE VERSION AT THIS TIME SO SORRY COME BACK ANYTIME")
        print()
    else:
        # Show ’em and weep:
        show()
        if consts.DEBUG:
            print()
            print(f"")

if __name__ == '__main__':
    main()