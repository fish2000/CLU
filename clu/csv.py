# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.mathematics import Σ
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

segments        = lambda line: len(line.split(','))

max_segments    = lambda csv_data: Σ(lambda line_segments, next_line:
                                        max(line_segments, segments(next_line)),
                                            csv_data.splitlines(), 0)

pad_line        = lambda line, padding: line + ',' + (('''"",''') * padding).rstrip(',')

pad_segments    = lambda csv_data, padding: map(lambda line: segments(line) < padding and \
                                              pad_line(line, padding - segments(line)) or \
                                                       line, csv_data.splitlines())

pad_csv         = lambda csv_data: '\n'.join(pad_segments(csv_data,
                                             max_segments(csv_data)))

export(segments,        name='segments',        doc="segments(«CSV line») → •line segment count•")
export(max_segments,    name='max_segments',    doc="max_segments(«uneven CSV data») → •largest line segment count•")
export(pad_line,        name='pad_line',        doc="pad_line(«uneven CSV lines») → «padded CSV lines»")
export(pad_segments,    name='pad_segments',    doc="pad_segments(«uneven CSV line fragments») → «padded CSV lines»")
export(pad_csv,         name='pad_csv',         doc="pad_csv(«uneven CSV data») → «padded CSV data»")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()