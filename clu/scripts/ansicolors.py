# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.repl import ansi
    
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
