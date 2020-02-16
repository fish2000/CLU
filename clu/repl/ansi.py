# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple as NamedTuple

import abc
import colorama
import clu.abstract
import inspect
import textwrap
import sys
import zict

abstract = abc.abstractmethod

from clu.constants.consts import DEBUG, ENCODING, SEPARATOR_WIDTH
from clu.constants.polyfills import Enum, unique, auto
from clu.predicates import mro, or_none
from clu.typology import dict_types, isstring, isbytes
from clu.fs.misc import re_matcher
from clu.naming import nameof, qualified_name
from clu.enums import alias, AliasingEnumMeta
from clu.stdio import std, linebreak, flush_all
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

# colorama.init()

print_separator = lambda filler='-': print(filler * SEPARATOR_WIDTH)
evict_announcer = lambda key, value: print(f"Cache dropped: {key}")

@export
class ANSIBase(Enum):
    
    """ Root ancestor class for all ANSI-code enums """
    
    @classmethod
    def is_ansi(cls, instance):
        return cls in mro(instance)

class CacheDescriptor(object):
    
    __slots__ = ('cache', 'lru')
    
    def __init__(self):
        self.cache = {}
        self.lru = zict.LRU(18, self.cache,
                                on_evict=(DEBUG \
                                      and evict_announcer \
                                       or None))
    
    def __get__(self, *args):
        return self.lru
    
    def __set__(self, instance, value):
        self.lru = value
    
    def __repr__(self):
        return repr(self.lru)

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
            if isstring(other):
                return self.to_string() + other
            elif isbytes(other):
                return self.to_string() + str(other, encoding=ENCODING)
            elif hasattr(other, 'to_string'):
                return self.to_string() + other.to_string()
            return NotImplemented
        
        doc_string = f""" Enumeration mapping ANSI codes to names found in “{qualified_name(source)}” """
        
        def to_string(self):
            return str(self.code)
        
        attributes['cache']     = CacheDescriptor()
        attributes['source']    = SourceDescriptor()
        attributes['__init__']  = init_method
        attributes['__str__']   = str_method
        attributes['__add__']   = add_method
        attributes['__doc__']   = inspect.cleandoc(doc_string)
        attributes['to_string'] = to_string
        
        return super(ANSI, metacls).__new__(metacls, name,
                                                     bases,
                                                     attributes,
                                                   **kwargs)
    
    def for_name(cls, name):
        """ Get an enum member or alias member by name """
        # Lower-ize the name:
        lowerstring = name.casefold()
        # Check cache and return if found:
        if lowerstring in cls.cache:
            return cls.cache[lowerstring]
        # Walk through standard ANSI names first:
        for ansi in cls:
            if ansi.name.casefold() == lowerstring:
                # If a match is found on an unaliased name,
                # simply cache and return:
                cls.cache[lowerstring] = ansi
                return ansi
        # Try aliased ANSI names second:
        for aka, ansialias in cls.__aliases__.items():
            if aka.casefold() == lowerstring:
                # Once a match is found, trace it back
                # to the original value before caching
                # and returning:
                for ansi in cls:
                    if ansi.value == ansialias:
                        cls.cache[lowerstring] = ansi
                        return ansi
        raise LookupError(f"No ANSI code found for “{name}”")
    
    def convert(cls, specifier):
        """ Convert a specifier of unknown type to an enum or alias member """
        if cls.is_ansi(specifier):
            return specifier                        # Already an ANSI type, return it
        if isstring(specifier):
            return cls.for_name(specifier)          # Match by name, decoding if necessary
        elif isbytes(specifier):
            return cls.for_name(str(specifier, encoding=ENCODING))
        elif hasattr(specifier, 'to_string'):
            return cls.for_name(specifier.to_string())
        raise LookupError(f"Couldn’t convert specifier to {cls.__name__}: {specifier!s}")
    
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

ANSIFormatBase = NamedTuple('ANSIFormatBase', FIELDS)

@export
class ANSIFormat(clu.abstract.Format,
                 clu.abstract.Cloneable,
                 clu.abstract.ReprWrapper,
                 ANSIFormatBase):
    
    """ The formatter class for ANSI markup codes. """
    
    RESET_ALL = Weight.RESET_ALL.to_string()
    
    @classmethod
    def from_dict(cls, format_dict):
        """ Instantiate an ANSIFormat with a dict of related ANSI values –
            q.v. FIELD string names supra.
        """
        assert any(field in format_dict for field in FIELDS)
        assert frozenset(format_dict.keys()).issubset(fields)
        return cls(**format_dict)
    
    def to_dict(self):
        """ Return the ANSI format primitives as a dict """
        out = {}
        for field in FIELDS:
            fieldval = or_none(self, field)
            if fieldval is not None:
                out[field] = fieldval
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
        if from_value not in (None, ''):
            if type(from_value) is cls:
                if all(field is None for field in from_value):
                    return from_value
                return cls.from_dict(from_value.to_dict())
            elif hasattr(from_value, 'to_dict'):
                return cls.from_dict(from_value.to_dict())
            elif isinstance(from_value, tuple(dict_types)):
                return cls.from_dict(from_value)
            elif isstring(from_value):
                text = from_value
            elif isbytes(from_value):
                text = str(from_value, encoding=ENCODING)
            elif ANSIBase.is_ansi(from_value):
                text = from_value
        instance = super(ANSIFormat, cls).__new__(cls, Text.convert(text),
                                                       Background.convert(background),
                                                       Weight.convert(weight))
        return instance
    
    @classmethod
    def null(cls):
        instance = super(ANSIFormat, cls).__new__(cls, None,
                                                       None,
                                                       None)
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
    
    def clone(self, deep=False, memo=None):
        # N.B. deep-cloning is meaningless here as everything’s an enum value:
        return type(self)(text=self.text,
                          background=self.background,
                          weight=self.weight)
    
    def inner_repr(self):
        return f"text={self.text.name or 'None'}, " \
               f"background={self.background.name or 'None'}, " \
               f"weight={self.weight.name or 'None'}"
    
    def render(self, string):
        """ Render a string appropriately marked up with the ANSI formatting
            called for by this ANSIFormat instance, ending with the necessary
            ANSI reset sequence(s).
        """
        prefix = self.to_string()
        suffix = prefix and self.RESET_ALL or ""
        return f"{prefix}{string!s}{suffix}"

@export
class NonFormat(clu.abstract.Format):
    
    """ A “format” type whose “render(…)” method is a no-op. """
    
    def __init__(self, *args):
        pass
    
    def render(self, string):
        """ Return a string, unchanged """
        return string

@export
def print_ansi(text, color=None, file=std.OUT):
    """ print_ansi(…) → Print text in ANSI color, using optional inline markup
                        from `colorama` for terminal color-escape delimiters """
    FormatClass = file.isatty() and ANSIFormat or NonFormat
    fmt = FormatClass(color)
    for line in text.splitlines():
        print(fmt.render(line), sep='', end='\n', file=file)
    return None

@export
def print_ansi_centered(text=None, color=None,
                                   filler='•',
                                   width=None,
                                   file=std.OUT):
    """ print_ansi_centered(…) → Print a string to the terminal, centered
                                 and bookended with asterisks """
    if text is None:
        return print_ansi(filler * (width or SEPARATOR_WIDTH), color=color, file=file)
    message = f" {text.strip()} "
    return print_ansi(message.center(width or SEPARATOR_WIDTH, filler), color=color, file=file)

INITIAL     = '  ¶ '
SUBSEQUENT  = '    '

# Regex boolean predicates for matching marked (or bulleted) paragraphs:
para_mark_matcher = re_matcher(r"^\s*[0-9+•⌀\<\>«»→\#¬†‡¶§±–\-\+\*]+")
para_line_matcher = re_matcher(r"^\s*[+•⌀\<\>«»→\#¬†‡¶§±–\-\+\*]+")

@export
def paragraphize(doc):
    """ Split a docstring into continuous paragraphs. """
    lines = [line.strip() for line in doc.strip().splitlines()]
    for idx, line in enumerate(lines):
        if line == '':
            lines[idx] = lines[idx-1].endswith('\n') and "\n" or "\n\n"
        else:
            if para_line_matcher(line):
                lines[idx] += " \n"
            else:
                lines[idx] += " "
    return ''.join(lines).splitlines()

# Pre-calculate width
WIDTH = int(SEPARATOR_WIDTH * 0.8)

@export
def highlight(code_string, language='json',
                             markup='terminal256',
                              style='paraiso-dark',
                             isatty=True):
    """ Highlight a code string with inline 256-color ANSI markup,
        using `pygments.highlight(…)` and the “Paraiso Dark” theme
    """
    if not isatty:
        return code_string
    import pygments, pygments.lexers, pygments.formatters
    LexerCls = pygments.lexers.find_lexer_class_by_name(language)
    formatter = pygments.formatters.get_formatter_by_name(markup, style=style)
    return pygments.highlight(code_string, lexer=LexerCls(), formatter=formatter)

@export
def ansidoc(*things):
    """ ansidoc(*things) → Print the docstring value for each thing, in ANSI color """
    # Start output
    flush_all()
    print()
    
    for thing in things:
        # Process each things’ name and doc
        thingname = nameof(thing)
        doc = inspect.getdoc(thing) or "«¡no docstring found!»"
        sig = inspect.signature(thing) or ""
        paras = paragraphize(doc)
        
        # Print the ANSI header
        print_ansi_centered(f"__doc__ for “{thingname}”", color=Text.CYAN)
        linebreak()
        
        # Code-highlight, format and print the thing and its call-signature:
        print(highlight(textwrap.fill(f"{thingname}{sig}",
                        initial_indent=INITIAL,
                        subsequent_indent=SUBSEQUENT,
                        replace_whitespace=True,
                        placeholder="…",
                        tabsize=4, width=WIDTH), language='python',
                                                 isatty=std.OUT.isatty()),
                                                 sep='', end='\n',
                                                 file=std.OUT)
        
        # Format and print each paragraph
        for para in paras:
            if para:
                marked = para_mark_matcher(para)
                print_ansi(textwrap.fill(para, initial_indent=marked and SUBSEQUENT or INITIAL,
                                            subsequent_indent=SUBSEQUENT,
                                           replace_whitespace=marked,
                                             break_on_hyphens=False,
                                              drop_whitespace=True,
                                                  placeholder='…',
                                                      tabsize=4,
                                                        width=WIDTH),
                                                        color=Text.GRAY)
            else:
                linebreak()
        
        # FLush and cease output
        linebreak()
        print()
        flush_all()

export(print_separator,     name='print_separator', doc="print_separator(filler='-') → print ‘filler’ character consts.SEPARATOR_WIDTH times")
export(evict_announcer,     name='evict_announcer', doc="evict_announcer(key, value) → print a debug trace message about the key and value")

# NO DOCS ALLOWED:
export(Text)
export(Background)
export(Weight)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()


def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_one():
        print_ansi('yo dogg')
        print_ansi_centered('I heard you like non-ANSI-formatted text')
    
    @inline
    def test_two():
        ansidoc(ansidoc)
    
    return inline.test(10)

if __name__ == '__main__':
    sys.exit(test())