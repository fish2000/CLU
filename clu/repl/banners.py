# -*- coding: utf-8 -*-
"""
banners.py

• Default module imports and other configgy code,
• For generic use in python repls – both the python2 and python3 interactive
  interpreters, as well as bpython, ipython, ptpython, pyzo, PyCharm, and
  whatever else; code specific to any given repl module lives in the config
  files, per whatever that packages’ demands may be.

Created by FI$H 2000 on 2019-02-27.
Copyright (c) 2012-2025 Objects In Space And Time, LLC. All rights reserved.

"""
from __future__ import print_function

import datetime
import colorama
import os
import sys

from clu.constants.consts import DEBUG, PY3, PYPY, TEXTMATE
from clu.repl.ansi import Text, print_ansi_centered
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# Python version figlet banners – using the figlet “Colossal” typeface:
banners = {}

banners['python3.x'] = """
                  888    888                         .d8888b.                
                  888    888                        d88P  Y88b               
                  888    888                             .d88P               
88888b.  888  888 888888 88888b.   .d88b.  88888b.      8888"      888  888  
888 "88b 888  888 888    888 "88b d88""88b 888 "88b      "Y8b.     `Y8bd8P'  
888  888 888  888 888    888  888 888  888 888  888 888    888       X88K    
888 d88P Y88b 888 Y88b.  888  888 Y88..88P 888  888 Y88b  d88P d8b .d8""8b.  
88888P"   "Y88888  "Y888 888  888  "Y88P"  888  888  "Y8888P"  Y8P 888  888  
888           888                                                            
888      Y8b d88P                                                            
888       "Y88P"                                                             
                                                                             
"""

banners['python3.8'] = """
                  888    888                         .d8888b.       .d8888b.  
                  888    888                        d88P  Y88b     d88P  Y88b 
                  888    888                             .d88P     Y88b .d88P 
88888b.  888  888 888888 88888b.   .d88b.  88888b.      8888"       "888888"  
888 "88b 888  888 888    888 "88b d88""88b 888 "88b      "Y8b.     .d8Y""Y8b. 
888  888 888  888 888    888  888 888  888 888  888 888    888     888    888 
888 d88P Y88b 888 Y88b.  888  888 Y88..88P 888  888 Y88b  d88P d8b Y88b  d88P 
88888P"   "Y88888  "Y888 888  888  "Y88P"  888  888  "Y8888P"  Y8P  "Y8888P"  
888           888                                                             
888      Y8b d88P                                                             
888       "Y88P"                                                              
                                                                              
"""

banners['python3.7'] = """
                  888    888                         .d8888b.      8888888888 
                  888    888                        d88P  Y88b           d88P 
                  888    888                             .d88P          d88P  
88888b.  888  888 888888 88888b.   .d88b.  88888b.      8888"          d88P   
888 "88b 888  888 888    888 "88b d88""88b 888 "88b      "Y8b.      88888888  
888  888 888  888 888    888  888 888  888 888  888 888    888       d88P     
888 d88P Y88b 888 Y88b.  888  888 Y88..88P 888  888 Y88b  d88P d8b  d88P      
88888P"   "Y88888  "Y888 888  888  "Y88P"  888  888  "Y8888P"  Y8P d88P       
888           888                                                             
888      Y8b d88P                                                             
888       "Y88P"                                                              
                                                                              
"""

banners['python2.7'] = """
                  888    888                         .d8888b.      8888888888 
                  888    888                        d88P  Y88b           d88P 
                  888    888                               888          d88P  
88888b.  888  888 888888 88888b.   .d88b.  88888b.       .d88P         d88P   
888 "88b 888  888 888    888 "88b d88""88b 888 "88b  .od888P"       88888888  
888  888 888  888 888    888  888 888  888 888  888 d88P"            d88P     
888 d88P Y88b 888 Y88b.  888  888 Y88..88P 888  888 888"       d8b  d88P      
88888P"   "Y88888  "Y888 888  888  "Y88P"  888  888 888888888  Y8P d88P       
888           888                                                             
888      Y8b d88P                                                             
888       "Y88P"                                                              
                                                                              
"""

banners['pypy3.x'] = """
                                     .d8888b.                                 
                                    d88P  Y88b                                
                                         .d88P                                
88888b.  888  888 88888b.  888  888     8888"      888  888                   
888 "88b 888  888 888 "88b 888  888      "Y8b.     `Y8bd8P'                   
888  888 888  888 888  888 888  888 888    888       X88K                     
888 d88P Y88b 888 888 d88P Y88b 888 Y88b  d88P d8b .d8""8b.                   
88888P"   "Y88888 88888P"   "Y88888  "Y8888P"  Y8P 888  888                   
888           888 888           888                                           
888      Y8b d88P 888      Y8b d88P                                           
888       "Y88P"  888       "Y88P"                                            
                                                                              
"""

banners['pypy3.8'] = """
                                     .d8888b.       .d8888b.                  
                                    d88P  Y88b     d88P  Y88b                 
                                         .d88P     Y88b .d88P                 
88888b.  888  888 88888b.  888  888     8888"       "888888"                  
888 "88b 888  888 888 "88b 888  888      "Y8b.     .d8Y""Y8b.                 
888  888 888  888 888  888 888  888 888    888     888    888                 
888 d88P Y88b 888 888 d88P Y88b 888 Y88b  d88P d8b Y88b  d88P                 
88888P"   "Y88888 88888P"   "Y88888  "Y8888P"  Y8P  "Y8888P"                  
888           888 888           888                                           
888      Y8b d88P 888      Y8b d88P                                           
888       "Y88P"  888       "Y88P"                                            
                                                                              
"""

banners['pypy3.7'] = """
                                     .d8888b.      8888888888                 
                                    d88P  Y88b           d88P                 
                                         .d88P          d88P                  
88888b.  888  888 88888b.  888  888     8888"          d88P                   
888 "88b 888  888 888 "88b 888  888      "Y8b.      88888888                  
888  888 888  888 888  888 888  888 888    888       d88P                     
888 d88P Y88b 888 888 d88P Y88b 888 Y88b  d88P d8b  d88P                      
88888P"   "Y88888 88888P"   "Y88888  "Y8888P"  Y8P d88P                       
888           888 888           888                                           
888      Y8b d88P 888      Y8b d88P                                           
888       "Y88P"  888       "Y88P"                                            
                                                                              
"""

banners['pypy3.6'] = """
                                     .d8888b.       .d8888b.                  
                                    d88P  Y88b     d88P  Y88b                 
                                         .d88P     888                        
88888b.  888  888 88888b.  888  888     8888"      888d888b.                  
888 "88b 888  888 888 "88b 888  888      "Y8b.     888P "Y88b                 
888  888 888  888 888  888 888  888 888    888     888    888                 
888 d88P Y88b 888 888 d88P Y88b 888 Y88b  d88P d8b Y88b  d88P                 
88888P"   "Y88888 88888P"   "Y88888  "Y8888P"  Y8P  "Y8888P"                  
888           888 888           888                                           
888      Y8b d88P 888      Y8b d88P                                           
888       "Y88P"  888       "Y88P"                                            
                                                                              
"""

banners['pypy2.7'] = """
                                     .d8888b.      8888888888                 
                                    d88P  Y88b           d88P                 
                                           888          d88P                  
88888b.  888  888 88888b.  888  888      .d88P         d88P                   
888 "88b 888  888 888 "88b 888  888  .od888P"       88888888                  
888  888 888  888 888  888 888  888 d88P"            d88P                     
888 d88P Y88b 888 888 d88P Y88b 888 888"       d8b  d88P                      
88888P"   "Y88888 88888P"   "Y88888 888888888  Y8P d88P                       
888           888 888           888                                           
888      Y8b d88P 888      Y8b d88P                                           
888       "Y88P"  888       "Y88P"                                            
                                                                              
"""

# Determine if we’re on PyPy and/or Python 3:
prefix = PYPY and 'pypy' or 'python'

# Configure ANSI-color python banner, per python version:
if PY3:
    banner = banners.get(f'{prefix}3.{sys.version_info.minor}', banners[f'{prefix}3.x'])
    banner_color = colorama.Fore.CYAN
else:
    banner = banners[f'{prefix}2.7']
    banner_color = colorama.Fore.LIGHTGREEN_EX

now = datetime.datetime.now
python2_expires = 'January 1st, 2020'
is_python2_dead = now() >= now().strptime(python2_expires, '%B %dst, %Y') and ['YES'] or []

@export
def print_python_banner(text, color,
                              reset=colorama.Style.RESET_ALL):
    for line in text.splitlines():
        print(color + line, sep='')
    print(reset, end='')

@export
def print_warning(text, color=colorama.Fore.RED,
                        reset=colorama.Style.RESET_ALL):
    print(color + text, sep='')
    print(reset, end='')

@export
def print_banner():
    # If we’re running in TextMate, use `sys.stderr` instead of ANSI colors,
    # as that’s the only way to get any sort of colored output in TextMate’s
    # console output window:
    if TEXTMATE:
        print(banner, file=sys.stderr)
    else:
        colorama.init()
        print_python_banner(banner, banner_color)
    
    if DEBUG:
        print_ansi_centered("DEBUG MODE INITIATED",
                             color=(TEXTMATE and Text.NOTHING \
                                              or Text.LIGHTYELLOW_EX))
        print()
    
    if not PY3:
        if is_python2_dead:
            warning = u"∞§• ¡LOOK OUT! Python 2.x has been officially declared DEAD!!!!!!!\n"
        else:
            warning = u"∞§• ¡BEWARE! Python 2.x will perish when the clock strikes 2020!!!\n"
        if os.environ.get('TM_PYTHON'):
            print(warning, file=sys.stderr)
        else:
            print_warning(warning)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()