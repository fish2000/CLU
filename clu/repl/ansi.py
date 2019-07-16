# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple

import colorama
colorama.init()

import sys

from clu.constants import ENCODING, SEPARATOR_WIDTH
from clu.constants import Enum, unique, auto
from clu.exporting import doctrim
from clu.naming import qualified_name
from clu.typology import string_types, bytes_types, dict_types
from clu.enums import alias, AliasingEnumMeta
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

print_separator = lambda filler='-': print(filler * SEPARATOR_WIDTH)

@export
class ANSIBase(Enum):
    
    """ Root ancestor class for all ANSI-code enums """
    
    @classmethod
    def is_ansi(cls, instance):
        return cls in type(instance).__mro__

class CacheDescriptor(object):
    
    __slots__ = ('cache',)
    
    def __init__(self):
        self.cache = {}
        self.cache['HITS'] = 0
        self.cache['MISSES'] = 0
    
    def __get__(self, *args):
        return self.cache
    
    def __set__(self, instance, value):
        self.cache = value
    
    def __repr__(self):
        return repr(self.cache)

@export
class ANSI(AliasingEnumMeta):
    
    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        """ Remove the “source” class keyword before calling up """
        superkws = dict(kwargs)
        if 'source' in superkws:
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
            
            __slots__ = tuple()
            
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
        
        attributes['cache']     = CacheDescriptor()
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
        # Lower-ize the name:
        lowerstring = name.lower()
        # Check cache and return if found:
        if lowerstring in cls.cache:
            cls.cache['HITS'] += 1
            return cls.cache[lowerstring]
        # Walk through standard ANSI names first:
        for ansi in cls:
            if ansi.name.lower() == lowerstring:
                # If a match is found on an unaliased name,
                # simply cache and return:
                cls.cache['MISSES'] += 1
                cls.cache[lowerstring] = ansi
                return ansi
        # Try aliased ANSI names second:
        for aka, ansialias in cls.__aliases__.items():
            if aka.lower() == lowerstring:
                # Once a match is found, trace it back
                # to the original value before caching
                # and returning:
                for ansi in cls:
                    if ansi.value == ansialias:
                        cls.cache['MISSES'] += 1
                        cls.cache[lowerstring] = ansi
                        return ansi
        raise LookupError("No ANSI code found for “%s”" % name)
    
    def convert(cls, specifier):
        """ Convert a specifier of unknown type to an enum or alias member """
        if cls.is_ansi(specifier):
            return specifier                        # Already an ANSI type, return it
        if isinstance(specifier, string_types):
            return cls.for_name(specifier)          # Match by name, decoding if necessary
        elif isinstance(specifier, bytes_types):
            return cls.for_name(str(specifier, encoding=ENCODING))
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

FIELDS = ('text', 'background', 'weight')
fields = frozenset(FIELDS)

ANSIFormatBase = NamedTuple('ANSIFormatBase', FIELDS, module=__file__)

@export
class ANSIFormat(ANSIFormatBase):
    
    RESET_ALL = Weight.RESET_ALL.to_string()
    
    @classmethod
    def from_dict(cls, format_dict):
        """ Instantiate an ANSIFormat with a dict of related ANSI values –
            q.v. FIELD string names supra.
        """
        assert any((field in format_dict) for field in FIELDS)
        assert frozenset(format_dict.keys()).issubset(fields)
        return cls(**format_dict)
    
    def to_dict(self):
        """ Return the ANSI format primitives as a dict """
        out = {}
        for field in FIELDS:
            if getattr(self, field, None) is not None:
                out[field] = getattr(self, field)
        return out
    
    def to_tuple(self):
        """ Return the ANSI format primitives as a tuple """
        return (self.text,
                self.background,
                self.weight)
    
    def to_string(self):
        """ Build up an initial ANSI format string based on values present """
        out = ""
        if self.text is not None:
            out += str(self.text)
        if self.background is not None:
            out += str(self.background)
        if self.weight is not None:
            out += str(self.weight)
        return out
    
    def __new__(cls, from_value=None, text=Text.NOTHING,
                                      background=Background.NOTHING,
                                      weight=Weight.NORMAL):
        """ Instantiate an ANSIFormat, populating its fields per args """
        if from_value is not None:
            if type(from_value) is cls:
                return cls.from_dict(from_value.to_dict())
            elif hasattr(from_value, 'to_dict'):
                return cls.from_dict(from_value.to_dict())
            elif type(from_value) in dict_types:
                return cls.from_dict(from_value)
            elif type(from_value) in string_types + bytes_types:
                text = from_value
            elif ANSIBase.is_ansi(from_value):
                text = from_value
        instance = super(ANSIFormat, cls).__new__(cls, Text.convert(text),
                                                       Background.convert(background),
                                                       Weight.convert(weight))
        return instance
    
    def __str__(self):
        """ Stringify the ANSIFormat (q.v. “to_string(…)” supra.) """
        return self.to_string()
    
    def __bytes__(self):
        """ Bytes-ify the ANSIFormat (q.v. “to_string(…)” supra.) """
        return bytes(self.to_string(), encoding=ENCODING)
    
    def __hash__(self):
        """ Hash the ANSIFormat, using its tuplized value """
        return hash(self.to_tuple())
    
    def __bool__(self):
        """ An instance of ANSIFormat is considered Falsey if its “text”,
           “background”, and “weight” fields are all set to None; otherwise it’s
            a Truthy value in boolean contexts
        """
        return not (self.text is None and \
                    self.background is None and \
                    self.weight is None)
    
    def render(self, string):
        """ Render a string appropriately marked up with the ANSI formatting
            called for by this ANSIFormat instance, ending with the necessary
            ANSI reset sequence(s).
        """
        return "%s%s%s" % (self.to_string(), str(string),
                                             str(self.RESET_ALL))

@export
def print_ansi(text, color=''):
    """ print_ansi(…) → Print text in ANSI color, using optional inline markup
                        from `colorama` for terminal color-escape delimiters """
    fmt = ANSIFormat(text=color)
    for line in text.splitlines():
        print(file=sys.__stdout__)
        print(fmt.render(line), sep='', file=sys.__stdout__)

@export
def print_ansi_centered(text, color='',
                              filler='•',
                              width=SEPARATOR_WIDTH):
    """ print_ansi_centered(…) → Print a string to the terminal, centered
                                 and bookended with asterisks """
    message = f" {text.strip()} "
    asterisks = int((width / 2) - (len(message) / 2))
    
    aa = filler[0] * asterisks
    ab = filler[0] * (asterisks + 0 - (len(message) % 2))
    
    print_ansi(f"{aa}{message}{ab}", color=color)

@export
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

export(print_separator,     name='print_separator', doc="print_separator(filler_char='-') → print filler_char TERMINAL_WIDTH times")

# NO DOCS ALLOWED:
export(Text)
export(Background)
export(Weight)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()