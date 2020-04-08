# -*- coding: utf-8 -*-
from __future__ import print_function

class TestCSV(object):
    
    """ Run the tests for the “clu.csv” module. """
    
    def test_pad_csv(self):
        from clu import csv
        
        result = csv.pad_csv(csv.unpadded)
        assert csv.padded.strip() == result.strip()
    
    def test_max_segments(self):
        from clu import csv
        
        maxseg = csv.max_segments(csv.unpadded)
        assert maxseg == csv.max_segments(csv.padded)
    
    def test_pad_line(self):
        from clu import csv
        
        line = "yo,dogg"
        pd = (('''"",''') * 98).rstrip(',')
        
        assert csv.pad_line(line, 100).endswith(pd)