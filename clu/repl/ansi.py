# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple

import colorama
colorama.init()

from constants import ENCODING, SEPARATOR_WIDTH
from constants import Enum, unique, auto
from naming import doctrim, qualified_name
from predicates import tuplize
from typology import string_types, bytes_types
from .enums import alias, AliasingEnumMeta

print_separator = lambda: print('-' * SEPARATOR_WIDTH)

class ANSIBase(Enum):
    
    """ Root ancestor class for all ANSI-code enums """
    
    @classmethod
    def is_ansi(cls, instance):
        return cls in type(instance).__mro__

class ANSI(AliasingEnumMeta):
    
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
        source = kwargs.pop('source')
        
        class SourceDescriptor(object):
            
            def __get__(self, *args):
                return source
            
            def __repr__(self):
                return repr(source)
        
        def init_method(self, value):
            self.code = str(getattr(type(self).source, self.name, ''))
        
        def str_method(self):
            return self.to_string()
        
        def add_method(self, other):
            if type(other) in string_types:
                return self.to_string() + other
            elif type(other) in bytes_types:
                return self.to_string() + str(other, encoding=ENCODING)
            elif ANSIBase.is_ansi(other):
                return self.to_string() + other.to_string()
            return NotImplemented
        
        doc_string = """ Enumeration mapping ANSI codes to names found in “%s” """
        
        def to_string(self):
            return str(self.code)
        
        attributes['source']    = SourceDescriptor()
        attributes['__init__']  = init_method
        attributes['__str__']   = str_method
        attributes['__add__']   = add_method
        attributes['__doc__']   = doctrim(doc_string % qualified_name(source))
        attributes['to_string'] = to_string
        
        return super(ANSI, metacls).__new__(metacls, name,
                                                     bases,
                                                     attributes,
                                                   **kwargs)
    
    def for_name(cls, name):
        """ Get an enum member or alias member by name """
        lowerstring = name.lower()
        for ansi in cls:
            if ansi.name.lower() == lowerstring:
                return ansi
        for aka, ansi in cls.__aliases__.items():
            if aka.lower() == lowerstring:
                return ansi
        raise LookupError("No ANSI code found for “%s”" % name)
    
    def convert(cls, specifier):
        """ Convert a specifier of unknown type to an enum or alias member """
        if cls.is_ansi(specifier):
            return specifier
        if type(specifier) in string_types:
            return cls.for_name(specifier)
        elif type(specifier) in bytes_types:
            return cls.for_name(str(specifier), encoding=ENCODING)
        raise LookupError("Couldn’t convert specifier to %s: %s" % (cls.__name__,
                                                                    str(specifier)))
    
    def _missing_(cls, value):
        # Insert terminal256 lookup here
        return super(ANSI, cls)._missing_(value)

@unique
class Text(ANSIBase, metaclass=ANSI, source=colorama.Fore):
    
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
    WHITE               = auto()
    YELLOW              = auto()
    GRAY                = alias(LIGHTBLACK_EX)
    GREY                = alias(LIGHTBLACK_EX)
    LIGHTBLUE           = alias(LIGHTBLUE_EX)
    LIGHTCYAN           = alias(LIGHTCYAN_EX)
    LIGHTGREEN          = alias(LIGHTGREEN_EX)
    LIGHTMAGENTA        = alias(LIGHTMAGENTA_EX)
    LIGHTRED            = alias(LIGHTRED_EX)
    PINK                = alias(LIGHTRED_EX)
    LIGHTWHITE          = alias(LIGHTWHITE_EX)
    LIGHTYELLOW         = alias(LIGHTYELLOW_EX)
    NOTHING             = auto()
    RESET               = auto()

@unique
class Background(ANSIBase, metaclass=ANSI, source=colorama.Back):
    
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
    WHITE               = auto()
    YELLOW              = auto()
    GRAY                = alias(LIGHTBLACK_EX)
    GREY                = alias(LIGHTBLACK_EX)
    LIGHTBLUE           = alias(LIGHTBLUE_EX)
    LIGHTCYAN           = alias(LIGHTCYAN_EX)
    LIGHTGREEN          = alias(LIGHTGREEN_EX)
    LIGHTMAGENTA        = alias(LIGHTMAGENTA_EX)
    LIGHTRED            = alias(LIGHTRED_EX)
    PINK                = alias(LIGHTRED_EX)
    LIGHTWHITE          = alias(LIGHTWHITE_EX)
    LIGHTYELLOW         = alias(LIGHTYELLOW_EX)
    NOTHING             = auto()
    RESET               = auto()

@unique
class Weight(ANSIBase, metaclass=ANSI, source=colorama.Style):
    
    BRIGHT              = auto()
    DIM                 = auto()
    NORMAL              = auto()
    NOTHING             = auto()
    RESET_ALL           = auto()
    RESET               = alias(RESET_ALL)

ANSIFormatBase = NamedTuple('ANSIFormatBase', ('text', 'background', 'weight'),
                                               defaults=tuplize(Background.NOTHING,
                                                                    Weight.NORMAL),
                                               module=__file__)

class ANSIFormat(ANSIFormatBase):
    
    def __new__(cls, text=Text.NOTHING,
                     background=Background.NOTHING,
                     weight=Weight.NORMAL):
        """ Instantiate an ANSIFormat, populating its fields per args """
        instance = super(ANSIFormat, cls).__new__(cls, Text.convert(text),
                                                       Background.convert(background),
                                                       Weight.convert(weight))
        return instance
    
    def render(self, string):
        return "%s%s%s" % (str(self.text) + \
                           str(self.background) + \
                           str(self.weight),
                           str(string),
                           str(Weight.RESET_ALL.to_string()))

def print_ansi(text, color=''):
    """ Print text in ANSI color, using optional inline markup
        from `colorama` for terminal color-escape delimiters
    """
    fmt = ANSIFormat(color)
    for line in text.splitlines():
        print(fmt.render(line), sep='')

def print_ansi_centered(text, color='',
                              filler='•',
                              width=SEPARATOR_WIDTH):
    """ Print a string to the terminal, centered and bookended with asterisks """
    message = f" {text.strip()} "
    asterisks = int((width / 2) - (len(message) / 2))
    
    aa = filler[0] * asterisks
    ab = filler[0] * (asterisks + 0 - (len(message) % 2))
    
    print_ansi(f"{aa}{message}{ab}", color=color)

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

__all__ = ('print_separator',
           'Text', 'Weight', 'Background', 'ANSIFormat',
           'print_ansi', 'print_ansi_centered', 'highlight')

__dir__ = lambda: list(__all__)