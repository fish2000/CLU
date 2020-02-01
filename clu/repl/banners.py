# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import sys

from clu.constants import consts
from clu.repl import ansi
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
prefix = consts.PYPY and 'pypy' or 'python'

# Configure ANSI-color python banner, per python version:
if consts.PY3:
    banner = banners.get(f'{prefix}3.{sys.version_info.minor}', banners[f'{prefix}3.x'])
    banner_color = ansi.Text.CYAN
else:
    banner = banners[f'{prefix}2.7']
    banner_color = ansi.Text.LIGHTGREEN

now = datetime.datetime.now
python2_expires = 'January 1st, 2020'
is_python2_dead = now() >= now().strptime(python2_expires, '%B %dst, %Y') and ['YES'] or []

@export
def print_python_banner(text, color,
                              reset=ansi.ANSIFormat.RESET_ALL,
                               file=ansi.sostream):
    for line in text.splitlines():
        print(color + line, sep='', file=file)
    print(reset, end='', file=file)

@export
def print_warning(text, color=ansi.Text.RED,
                        reset=ansi.ANSIFormat.RESET_ALL,
                         file=ansi.sostream):
    print(color + text, sep='', file=file)
    print(reset, end='', file=file)

@export
def print_banner():
    # If we’re running in TextMate, use `sys.stderr` instead of ANSI colors,
    # as that’s the only way to get any sort of colored output in TextMate’s
    # console output window:
    if consts.TEXTMATE:
        print(banner, file=sys.stderr)
    
    else:
        print_python_banner(banner, banner_color)
    
    if consts.DEBUG:
        ansi.print_ansi_centered("DEBUG MODE INITIATED",
                                 color=(consts.TEXTMATE and ansi.Text.NOTHING \
                                                         or ansi.Text.LIGHTYELLOW_EX))
        print()
    
    if not consts.PY3:
        
        if is_python2_dead:
            warning = u"∞§• ¡LOOK OUT! Python 2.x has been officially declared DEAD!!!!!!!\n"
        else:
            warning = u"∞§• ¡BEWARE! Python 2.x will perish when the clock strikes 2020!!!\n"
        
        if consts.TEXTMATE:
            print(warning, file=sys.stderr)
        else:
            print_warning(warning)
            ansi.flush_all()

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()