# -*- coding: utf-8 -*-
from __future__ import print_function

import pytest

class TestColumize(object):
    
    def test_columnize_basic(self):
        """ Basic “columnize(¬)” sanity and status testing. """
        from clu.repl.columnize import columnize
        
        assert "1, 2, 3\n"      == columnize(['1', '2', '3'], display_width=10, separator=', ')
        assert "1  3\n2  4\n"   == columnize(['1', '2', '3', '4'], display_width=4)
        assert "1  3\n2  4\n"   == columnize(['1', '2', '3', '4'], display_width=7)
        
        assert "0  1  2\n3\n"   == columnize(['0', '1', '2', '3'], display_width=7, vertical_display=False)
        
        assert "<empty>\n"      == columnize([])
        assert "oneitem\n"      == columnize(["oneitem"])
        
        data = [str(idx) for idx in range(55)]
        
        assert \
            "0,  6, 12, 18, 24, 30, 36, 42, 48, 54\n" + \
            "1,  7, 13, 19, 25, 31, 37, 43, 49\n" +     \
            "2,  8, 14, 20, 26, 32, 38, 44, 50\n" +     \
            "3,  9, 15, 21, 27, 33, 39, 45, 51\n" +     \
            "4, 10, 16, 22, 28, 34, 40, 46, 52\n" +     \
            "5, 11, 17, 23, 29, 35, 41, 47, 53\n" == columnize(data,
                                                               display_width=39,
                                                               ljust=False,
                                                               vertical_display=True,
                                                               separator=', ')
        
        assert \
            "    0,  7, 14, 21, 28, 35, 42, 49\n" +     \
            "    1,  8, 15, 22, 29, 36, 43, 50\n" +     \
            "    2,  9, 16, 23, 30, 37, 44, 51\n" +     \
            "    3, 10, 17, 24, 31, 38, 45, 52\n" +     \
            "    4, 11, 18, 25, 32, 39, 46, 53\n" +     \
            "    5, 12, 19, 26, 33, 40, 47, 54\n" +     \
            "    6, 13, 20, 27, 34, 41, 48\n"     == columnize(data,
                                                               display_width=39,
                                                               ljust=False,
                                                               vertical_display=True,
                                                               separator=', ',
                                                               line_prefix='    ')
        
        assert \
            " 0,  1,  2,  3,  4,  5,  6,  7,  8,  9\n" + \
            "10, 11, 12, 13, 14, 15, 16, 17, 18, 19\n" + \
            "20, 21, 22, 23, 24, 25, 26, 27, 28, 29\n" + \
            "30, 31, 32, 33, 34, 35, 36, 37, 38, 39\n" + \
            "40, 41, 42, 43, 44, 45, 46, 47, 48, 49\n" + \
            "50, 51, 52, 53, 54\n"                     == columnize(data,
                                                                    display_width=39,
                                                                    ljust=False,
                                                                    vertical_display=False,
                                                                    separator=', ')
        
        assert \
            "     0,  1,  2,  3,  4,  5,  6,  7\n" +    \
            "     8,  9, 10, 11, 12, 13, 14, 15\n" +    \
            "    16, 17, 18, 19, 20, 21, 22, 23\n" +    \
            "    24, 25, 26, 27, 28, 29, 30, 31\n" +    \
            "    32, 33, 34, 35, 36, 37, 38, 39\n" +    \
            "    40, 41, 42, 43, 44, 45, 46, 47\n" +    \
            "    48, 49, 50, 51, 52, 53, 54\n"     == columnize(data,
                                                                display_width=34,
                                                                ljust=False,
                                                                vertical_display=False,
                                                                separator=', ',
                                                                line_prefix='    ')
    
    def test_columnize_intermediate(self):
        """ Intermediate “columnize(¬)” sanity and status testing. """
        from clu.repl.columnize import columnize
        
        data = (
            "one",       "two",         "three",
            "four",      "five",        "six",
            "seven",     "eight",       "nine",
            "ten",       "eleven",      "twelve",
            "thirteen",  "fourteen",    "fifteen",
            "sixteen",   "seventeen",   "eightteen",
            "nineteen",  "twenty",      "twentyone",
            "twentytwo", "twentythree", "twentyfour",
            "twentyfive","twentysix",   "twentyseven")
        
        assert \
            "one         two        three        four       five         six       \n" + \
            "seven       eight      nine         ten        eleven       twelve    \n" + \
            "thirteen    fourteen   fifteen      sixteen    seventeen    eightteen \n" + \
            "nineteen    twenty     twentyone    twentytwo  twentythree  twentyfour\n" + \
            "twentyfive  twentysix  twentyseven\n" == columnize(data,
                                                                display_width=71,
                                                                vertical_display=False,
                                                                ljust=True)
        
        # assert \
        #     "one    five   nine    thirteen  seventeen  twentyone    twentyfive \n" + \
        #     "two    six    ten     fourteen  eightteen  twentytwo    twentysix  \n" + \
        #     "three  seven  eleven  fifteen   nineteen   twentythree  twentyseven\n" + \
        #     "four   eight  twelve  sixteen   twenty     twentyfour \n" == columnize(data)
        
        assert '0  1  2  3\n' == columnize(list(range(4)))
        
        assert \
            "[ 0,  1,  2,  3,  4,  5,  6,  7,  8,\n" + \
            "  9, 10, 11, 12, 13, 14, 15, 16, 17,\n" + \
            " 18, 19, 20, 21, 22, 23, 24, 25, 26,\n" + \
            " 27, 28, 29, 30, 31, 32, 33, 34, 35,\n" + \
            " 36, 37, 38, 39, 40, 41, 42, 43, 44,\n" + \
            " 45, 46, 47, 48, 49, 50, 51, 52, 53,\n" + \
            " 54]\n\n" == columnize(list(range(55)), **{ 'display_width' : 38, 'standard_display' : True })
        
        assert """[ 0,
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
 10,
 11]

""" == columnize(list(range(12)), **{ 'display_width' : 6, 'standard_display' : True })
        
        assert """[ 0,  1,
  2,  3,
  4,  5,
  6,  7,
  8,  9,
 10, 11]

""" == columnize(list(range(12)), **{ 'display_width' : 9, 'standard_display' : True })
    
    def test_columnize_format_percenter(self):
        from clu.repl.columnize import columnize
        assert '    0    1    2    3' == columnize([0, 1, 2, 3], display_width=7,
                                                           vertical_display=False,
                                                           **{ 'format' : '%5d', 'line_suffix' : '' })
    
    def test_columnize_line_prefix(self):
        from clu.repl.columnize import columnize
        assert '>>>       0\n>>>       1\n>>>       2\n>>>       3\n' == columnize([0, 1, 2, 3],
                                                                                   vertical_display=False,
                                                                                   **{ 'format' : '%5d', 'display_width' : 16, 'line_prefix' : '>>>   ' })
    
    def test_columnize_line_prefix_just_wide_enough(self):
        from clu.repl.columnize import columnize
        assert '>>>10  12\n>>>11  13\n' == columnize([10, 11, 12, 13], **{ 'line_prefix' : '>>>', 'display_width' : 9 })
    
    @pytest.mark.parametrize('columns', range(75, 95, 2))
    def test_computed_display_width_environment_COLUMNS(self, columns, environment):
        from clu.repl.columnize import computed_display_width
        environment['COLUMNS'] = str(columns)
        width = computed_display_width()
        assert width == columns
    
    def _test_errors(self):
        """ Test various error conditions. """
        from clu.repl.columnize import columnize
        self.assertRaises(TypeError, columnize, 5, 'reject input - not array')
