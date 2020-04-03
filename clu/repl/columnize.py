# -*- coding: utf-8 -*-
""" Transform an iterable list of something into a columnized
    string representation.
    
    Adapted from the routine of the same name found in “cmd.py”;
    further messed with to remove all the “pass” statements,
    simplify keyword-arg handling, normalize basically all of the
    argument names, and generally adapt it to the CLU world.
    
    Q.v. the original pre-CLU version supra: https://git.io/JvPfl
"""
from __future__ import print_function

import collections.abc
import clu.abstract
import sys, os

from clu.constants import consts
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class Percenter(clu.abstract.SlottedFormat):
    
    """ A format type that uses the %% (string-interpolation) operator
        on its opstring to render its operands.
    """
    
    def __init__(self, opstring):
        self.opstring = str(opstring)
    
    def render(self, string):
        return self.opstring % string

@export
class StrMethod(clu.abstract.SlottedFormat):
    
    """ A format type that uses a call to the “format(…)” method
        on its opstring to render its operands.
    """
    
    def __init__(self, opstring):
        self.opstring = str(opstring).replace('{}', '{0}', 1)
    
    def render(self, string):
        return self.opstring.format(string)

def computed_display_width():
    """ Figure out a decent and non-bonkers terminal display width value.
        
        • Uses os.environ['COLUMNS'] if possible,
        • Falls back to “consts.SEPARATOR_WIDTH”,
        • Failing that, returns 80 (an altogether reasonable number).
    """
    return int(os.environ.get('COLUMNS', consts.SEPARATOR_WIDTH)) or 80

default_opts = {
    'standard_display' : False,  # Check if file has changed since last time
    'vertical_display' : True,
    'format'           : clu.abstract.NonFormat(),
    'separator'        : '  ',
    'array_prefix'     : '',
    'array_suffix'     : '',
    'line_prefix'      : '',
    'line_suffix'      : "\n",
    'ljust'            : None,
    'term_adjust'      : False
}

def vertical_index(nrows, row, col):
    """ Compute the array index using vertical-display logic """
    # lambda nrows, row, col: nrows * col + row
    return nrows * col + row

def horizontal_index(ncols, row, col):
    """ Compute the array index using horizontal-display logic """
    # lambda ncols, row, col: ncols * (row - 1) + col
    return ncols * (row - 1) + col

@export
def columnize(array, display_width=computed_display_width(), **opts):
    """ Return a list of strings as a compact set of columns, distributed
        horizontally or vertically.
        
        For example, for a line width of 4 characters (arranged vertically):
            ['1', '2,', '3', '4'] → '1  3\n2  4\n'
        
        … or arranged horizontally:
            ['1', '2,', '3', '4'] → '1  2\n3  4\n'
        
        Each column is only as wide as necessary.  By default, columns
        are separated by two spaces - one wasn’t legible enough.
        
        • Set the “separator” option to adjust the string separate columns.
        • Set “display_width” to set the line width.
        
        Normally, consecutive items go down from the top to bottom from
        the left-most column to the right-most. If "vertical_display" is
        set false, consecutive items will go across, left to right, top to
        bottom.
    """
    if not isinstance(array, collections.abc.Iterable):
        typename = type(array).__name__
        raise TypeError(f'“array” must be an iterable instance (got “{typename}”)')
    
    o = { 'display_width' : display_width }
    o.update(default_opts)
    
    if len(opts.keys()) > 0:
        
        o.update(opts)
        
        if opts.get('standard_display', False):
            o['standard_display']   = True
            o['vertical_display']   = False
            o['separator']          = ', '
            o['array_prefix']       = '['
            o['array_suffix']       = "]\n"
            o['line_prefix']        = ' '
            o['line_suffix']        = ",\n"
    
    fmt = o.get('format')
    if not isinstance(fmt, clu.abstract.Format):
        if isinstance(fmt, type(None)):
            fmt = opts.get('format')
        if isinstance(fmt, (bytes, bytearray)):
            fmt = str(fmt, encoding=consts.ENCODING)
        if isinstance(fmt, str):
            if '%' in fmt:
                fmt = Percenter(fmt)
            elif '{' in fmt and '}' in fmt:
                fmt = StrMethod(fmt)
            else:
                raise ValueError(f"Opstring “{fmt!s}” contains no format-control characters")
    
    array = [fmt.render(item) for item in array]
    
    # Some degenerate cases
    size = len(array)
    if size == 0:
        return "<empty>\n"
    elif size == 1:
        return '%s%s%s\n' % (o['array_prefix'], str(array[0]),
                             o['array_suffix'])
    
    o['display_width'] = max(4, o['display_width'] - len(o['line_prefix']))
    
    if o['vertical_display']:
        # Try every row count from 1 upwards
        for nrows in range(1, size + 1):
            ncols = (size + nrows - 1) // nrows
            colwidths = []
            totwidth = -len(o['separator'])
            for col in range(ncols):
                # get max column width for this column
                colwidth = 0
                for row in range(nrows):
                    idx = vertical_index(nrows, row, col)
                    if idx >= size:
                        break
                    x = array[idx]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + len(o['separator'])
                if totwidth > o['display_width']:
                    break
            if totwidth <= o['display_width']:
                break
        
        # The smallest number of rows computed and the
        # max widths for each column has been obtained.
        # Now we just have to format each of the
        # rows.
        
        s = ''
        
        for row in range(nrows):
            texts = []
            
            for col in range(ncols):
                idx = row + nrows * col
                if idx >= size:
                    x = ""
                else:
                    x = array[idx]
                texts.append(x)
            
            while texts and not texts[-1]:
                del texts[-1]
            
            for col in range(len(texts)):
                if o['ljust']:
                    texts[col] = texts[col].ljust(colwidths[col])
                else:
                    texts[col] = texts[col].rjust(colwidths[col])
            
            s += "%s%s%s" % (o['line_prefix'], str(o['separator'].join(texts)),
                             o['line_suffix'])
        return s
    
    else: # 'vertical_display' is False
        # Try every column count from size downwards
        colwidths = []
        for ncols in range(size, 0, -1):
            # Try every row count from 1 upwards
            min_rows = (size + ncols - 1) // ncols
            nrows = min_rows - 1
            while nrows < size:
                nrows += 1
                rounded_size = nrows * ncols
                colwidths = []
                totwidth  = -len(o['separator'])
                for col in range(ncols):
                    # get max column width for this column
                    colwidth  = 0
                    for row in range(1, nrows + 1):
                        idx = horizontal_index(ncols, row, col)
                        if idx >= rounded_size:
                            break
                        elif idx < size:
                            x = array[idx]
                            colwidth = max(colwidth, len(x))
                    colwidths.append(colwidth)
                    totwidth += colwidth + len(o['separator'])
                    if totwidth >= o['display_width']:
                        break
                if totwidth <= o['display_width'] and idx >= rounded_size - 1:
                    # Found the right nrows and ncols
                    # print "right nrows and ncols"
                    nrows = row
                    break
                elif totwidth >= o['display_width']:
                    # print "reduce ncols", ncols
                    # Need to reduce ncols
                    break
            if totwidth <= o['display_width'] and idx >= rounded_size - 1:
                break
        
        # The smallest number of rows computed and the
        # max widths for each column has been obtained.
        # Now we just have to format each of the
        # rows.
        
        s = ''
        
        if len(o['array_prefix']) != 0:
            prefix = o['array_prefix']
        else:
            prefix = o['line_prefix']
        
        for row in range(1, nrows + 1):
            texts = []
            
            for col in range(ncols):
                idx = horizontal_index(ncols, row, col)
                if idx >= size:
                    break
                else:
                    x = array[idx]
                texts.append(x)
            
            for col in range(len(texts)):
                if o['ljust']:
                    texts[col] = texts[col].ljust(colwidths[col])
                else:
                    texts[col] = texts[col].rjust(colwidths[col])
            
            s += "%s%s%s" % (prefix, str(o['separator'].join(texts)),
                                         o['line_suffix'])
            prefix = o['line_prefix']
        
        if o['standard_display']:
            separator = o['separator'].rstrip()
            separator_pos = -(len(separator) + 1)
            if s[separator_pos:] == separator + "\n":
                s = s[:separator_pos] + o['array_suffix'] + "\n"
        else:
            s += o['array_suffix']
        
        return s

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def demo():
    """ Print a series of illustrations of the “columnize(…)” function """
    
    WIDTH = computed_display_width()
    
    def columnprint(*args, line_character='=', **kwargs):
        out = columnize(*args, **kwargs)
        print(line_character * WIDTH)
        print(out)
    
    columnprint(list(range(12)), **{ 'display_width' : 6, 'standard_display' : True })
    columnprint(list(range(12)), **{ 'display_width' : 10, 'standard_display' : True })
    
    for t in ((4, 4), (4, 7), (100, 80)):
        width = t[1]
        data = [str(idx) for idx in range(t[0])]
        options = {}
        
        for t2 in ((False, 'horizontal'), (True, 'vertical')):
            print('=' * WIDTH)
            print("Width: %d, direction: %s" % (width, t2[1]))
            options['display_width'] = width
            options['vertical_display'] = t2[0]
            columnprint(data, line_character='-', **options)
    
    columnprint([])
    columnprint(["oneitem"])
    columnprint(("one", "two", "three"))
    
    columnprint(["a", '2', "c", '3', "p", '0'], display_width=25,
                                                separator='  ',
                                                format=Percenter('_________%s'),
                                                line_suffix=" …\n")
    
    for t in ((4, 4), (4, 7), (100, 80)):
        width = WIDTH
        data = [str(idx) for idx in range(t[0])]
        options = {}
        
        for t2 in ((False, 'horizontal'), (True, 'vertical')):
            print('=' * WIDTH)
            print("Width: %d, direction: %s" % (width, t2[1]))
            options['display_width'] = width
            options['vertical_display'] = t2[0]
            columnprint(data, line_character='-', **options)
    
    data = (
        "one",        "two",         "three",
        "four",       "five",        "six",
        "seven",      "eight",       "nine",
        "ten",        "eleven",      "twelve",
        "thirteen",   "fourteen",    "fifteen",
        "sixteen",    "seventeen",   "eighteen",
        "nineteen",   "twenty",      "twentyone",
        "twentytwo",  "twentythree", "twentyfour",
        "twentyfive", "twentysix",   "twentyseven")
    
    columnprint(data)
    columnprint(data, vertical_display=False)
    
    data = [str(idx) for idx in range(55)]
    
    columnprint(data, **{ 'display_width' : 39, 'standard_display' : True })
    
    columnprint(data, display_width=39,
                      ljust=False,
                      separator=', ',
                      line_prefix='    ')
    
    columnprint(data, display_width=39,
                      ljust=False,
                      vertical_display=False,
                      separator=', ')
    
    columnprint(data, display_width=39,
                      ljust=False,
                      vertical_display=False,
                      separator=', ',
                      line_prefix='    ')
    
    # Attempt to columnize something non-iterable:
    try:
        columnprint(5)
    except TypeError:
        _, err, _ = sys.exc_info()
        print('≠' * WIDTH)
        print(err)
        print()
    
    columnprint(data, **{ 'display_width' : WIDTH, 'standard_display' : True })
    
    columnprint(data, display_width=WIDTH,
                      ljust=False,
                      separator=', ',
                      line_prefix='    ')
    
    columnprint(data, display_width=WIDTH,
                      ljust=False,
                      vertical_display=False,
                      separator=', ')
    
    columnprint(data, display_width=WIDTH,
                      ljust=False,
                      vertical_display=False,
                      separator=', ',
                      line_prefix='    ')
    
    columnprint(list(range(4)))

if __name__=='__main__':
    demo()