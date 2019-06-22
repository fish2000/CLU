# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple

import colorama
colorama.init()

from constants import SEPARATOR_WIDTH, Enum, EnumMeta, unique, auto
from naming import qualified_name
from predicates import tuplize

print_separator = lambda: print('-' * SEPARATOR_WIDTH)

# class ANSISource(object):
#
#     """ Read-only descriptor for Colorama sources of ANSI codes """
#
#     def __init__(self, source):
#         self.source = source
#
#     def __get__(self, *args):
#         return self.source
#
#     def __repr__(self):
#         return repr(self.source)

class ANSIAncestor(Enum):
    
    """ Root ancestor class for all ANSI-code enums """
    
    @classmethod
    def is_ansi(cls, instance):
        return cls in type(instance).__mro__

class ANSI(EnumMeta):
    
    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        """ Remove the “source” class keyword before calling up """
        superkws = dict(kwargs)
        del superkws['source']
        return super(ANSI, metacls).__prepare__(name, bases, **superkws)
    
    def __new__(metacls, name, bases, attributes, **kwargs):
        """ Override for `type.__new__(…)` setting up a derived
            Enum class that pulls from a “source” with the
            requisite methods (q.v. Text, Background and Weight
            definitions sub.)
        """
        source = kwargs.pop('source', None) or colorama.Fore
        
        class Source(object):
            
            def __get__(self, *args):
                return source
            
            def __repr__(self):
                return repr(source)
        
        def init_method(self, value):
            self.code = getattr(type(self).source, self.name)
        
        def str_method(self):
            return self.to_string()
        
        def add_method(self, other):
            if not type(self).is_ansi(other):
                return NotImplemented
            return self.to_string() + other.to_string()
        
        doc_string = """ Enum class mapping ANSI names %s codes """ % qualified_name(source)
        
        def to_string(self):
            return str(self.code)
        
        attributes['source']    = Source()
        attributes['__init__']  = init_method
        attributes['__str__']   = str_method
        attributes['__add__']   = add_method
        attributes['__doc__']   = doc_string
        attributes['to_string'] = to_string
        
        return super(ANSI, metacls).__new__(metacls, name,
                                                     bases,
                                                     attributes,
                                                   **kwargs)
    
    def for_string(cls, string):
        lowerstring = string.lower()
        for ansi in cls:
            if ansi.name.lower() == lowerstring:
                return ansi
        raise LookupError("No ANSI code found for “%s”" % string)
    
    def _missing_(cls, value):
        # Insert terminal256 lookup here
        return super(ANSI, cls)._missing_(value)

@unique
class Text(ANSIAncestor, metaclass=ANSI,
                         source=colorama.Fore):
    
    BLACK               = auto()
    BLUE                = auto()
    CYAN                = auto()
    GREEN               = auto()
    LIGHTBLACK_EX       = auto()
    LIGHTBLUE_EX        = auto()
    LIGHTCYAN_EX        = auto()
    LIGHTGREEN_EX       = auto()
    LIGHTMAGENTA_EX     = auto()
    LIGHTRED_EX         = auto()
    LIGHTWHITE_EX       = auto()
    LIGHTYELLOW_EX      = auto()
    MAGENTA             = auto()
    RED                 = auto()
    RESET               = auto()
    WHITE               = auto()
    YELLOW              = auto()

@unique
class Background(ANSIAncestor, metaclass=ANSI,
                               source=colorama.Back):
    
    BLACK               = auto()
    BLUE                = auto()
    CYAN                = auto()
    GREEN               = auto()
    LIGHTBLACK_EX       = auto()
    LIGHTBLUE_EX        = auto()
    LIGHTCYAN_EX        = auto()
    LIGHTGREEN_EX       = auto()
    LIGHTMAGENTA_EX     = auto()
    LIGHTRED_EX         = auto()
    LIGHTWHITE_EX       = auto()
    LIGHTYELLOW_EX      = auto()
    MAGENTA             = auto()
    RED                 = auto()
    RESET               = auto()
    WHITE               = auto()
    YELLOW              = auto()

@unique
class Weight(ANSIAncestor, metaclass=ANSI,
                           source=colorama.Style):
    
    BRIGHT              = auto()
    DIM                 = auto()
    NORMAL              = auto()
    RESET_ALL           = auto()

# class ForegroundAncestor(Enum):
#
#     def _generate_next_value(name,
#                              start,
#                              count,
#                              last_values):
#         return getattr(colorama.Fore, name)
#
#     @classmethod
#     def _missing_(cls, value):
#         # Insert terminal256 lookup shit here
#         pass

ANSIFormat = NamedTuple('ANSIFormat', ('text', 'background', 'weight'),
                      defaults=tuplize(Weight.NORMAL),
                        module=__file__)

def print_ansi(text, color='', reset=None):
    """ Print text in ANSI color, using optional inline markup
        from `colorama` for terminal color-escape delimiters
    """
    for line in text.splitlines():
        print(color + line, sep='')
    print(reset or colorama.Style.RESET_ALL, end='')

def print_ansi_centered(text, color='', reset=None,
                              filler='*',
                              width=SEPARATOR_WIDTH):
    """ Print a string to the terminal, centered and bookended with asterisks """
    message = f" {text.strip()} "
    asterisks = (width / 2) - (len(message) / 2)
    
    aa = filler[0] * asterisks
    ab = filler[0] * (asterisks + 0 - (len(message) % 2))
    
    print_ansi(f"{aa}{message}{ab}", color=color,
                                     reset=reset)

def highlight(code_string, language='json',
                             markup='terminal256',
                              style='paraiso-dark'):
    """ Highlight a code string with inline 256-color ANSI markup,
        using `pygments.highlight(…)` and the “Paraiso Dark” theme
    """
    import pygments, pygments.lexers, pygments.formatters
    LexerCls = pygments.lexers.find_lexer_class_by_name(language)
    formatter = pygments.formatters.get_formatter_by_name(markup, style=style)
    return pygments.highlight(code_string, lexer=LexerCls(), formatter=formatter)