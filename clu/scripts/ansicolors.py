# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.repl import ansi
from clu.exporting import Exporter

exporter = Exporter(path=__file__)

# ANSI colors:
green       = ansi.ANSIFormat(text=ansi.Text.GREEN)
lightgreen  = ansi.ANSIFormat(text=ansi.Text.LIGHTGREEN)

red         = ansi.ANSIFormat(text=ansi.Text.RED)
lightred    = ansi.ANSIFormat(text=ansi.Text.LIGHTRED)

cyan        = ansi.ANSIFormat(text=ansi.Text.CYAN)
dimcyan     = ansi.ANSIFormat(text=ansi.Text.CYAN,
                              weight=ansi.Weight.DIM)
lightcyan   = ansi.ANSIFormat(text=ansi.Text.LIGHTCYAN)
dimlightcyan = ansi.ANSIFormat(text=ansi.Text.LIGHTCYAN,
                              weight=ansi.Weight.DIM)

gray        = ansi.ANSIFormat(text=ansi.Text.GRAY)
dimgray     = ansi.ANSIFormat(text=ansi.Text.GRAY,
                              weight=ansi.Weight.DIM)

yellow      = ansi.ANSIFormat(text=ansi.Text.YELLOW)
blue        = ansi.ANSIFormat(text=ansi.Text.BLUE)
lightblue   = ansi.ANSIFormat(text=ansi.Text.LIGHTBLUE)
brightblue  = ansi.ANSIFormat(text=ansi.Text.LIGHTBLUE,
                              weight=ansi.Weight.BRIGHT)

green_bg    = ansi.ANSIFormat(text=ansi.Text.BLACK,
                              background=ansi.Background.GREEN,
                              weight=ansi.Weight.DIM)
cyan_bg     = ansi.ANSIFormat(text=ansi.Text.BLACK,
                              background=ansi.Background.CYAN,
                              weight=ansi.Weight.DIM)
yellow_bg   = ansi.ANSIFormat(text=ansi.Text.BLACK,
                              background=ansi.Background.YELLOW,
                              weight=ansi.Weight.DIM)

nothing     = ansi.ANSIFormat()

with exporter as export:
    
    export(green,           name='green')
    export(lightgreen,      name='lightgreen')
    
    export(red,             name='red')
    export(lightred,        name='lightred')
    
    export(cyan,            name='cyan')
    export(dimcyan,         name='dimcyan')
    export(lightcyan,       name='lightcyan')
    export(dimlightcyan,    name='dimlightcyan')
    
    export(gray,            name='gray')
    export(dimgray,         name='dimgray')
    
    export(yellow,          name='yellow')
    export(blue,            name='blue')
    export(lightblue,       name='lightblue')
    export(brightblue,      name='brightblue')
    
    export(green_bg,        name='green_bg')
    export(cyan_bg,         name='cyan_bg')
    export(yellow_bg,       name='yellow_bg')
    
    export(nothing,         name='nothing')

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
