# -*- coding: utf-8 -*-
from __future__ import print_function

import re

from constants import unicode, PY3, ENCODING

# TEXT UTILITIES: `sanitize(…)` to remove high-code-point glyphs

def sanitize(text):
    """ Remove specific unicode strings, in favor of ASCII-friendly versions """
    sanitized = unicode(text)
    for sanitizer, substitution in sanitize.sanitizers:
        sanitized, _ = sanitizer.subn(substitution, sanitized)
    return sanitized

# Regular expression compiler shortcut:
sanitize.re = lambda string: re.compile(string, re.MULTILINE)

# Sanitization regexes and their replacement strings:
sanitize.sanitizers = (
    (sanitize.re(r"[“”]"),              '"'),
    (sanitize.re(r"[‘’]"),              "'"),
    (sanitize.re(r"[«»]"),              ":"),
    (sanitize.re(r"[äáª]"),             "a"),
    (sanitize.re(r"[ëé]"),              "e"),
    (sanitize.re(r"[ïí]"),              "i"),
    (sanitize.re(r"[öóº]"),             "o"),
    (sanitize.re(r"[üú]"),              "u"),
    (sanitize.re(r"‽"),                 "?!"),
    (sanitize.re(r"¡"),                 "!"),
    (sanitize.re(r"¿"),                 "?"),
    (sanitize.re(r"±"),                 "+/-"),
    (sanitize.re(r"÷"),                 "/"),
    (sanitize.re(r"•"),                 "*"),
    (sanitize.re(r"ˆ"),                 "^"),
    (sanitize.re(r"†"),                 "<*>"),
    (sanitize.re(r"‡"),                 "<**>"),
    (sanitize.re(r"§"),                 "$"),
    (sanitize.re(r"¥"),                 "Y"),
    (sanitize.re(r"¢"),                 "c"),
    (sanitize.re(r"ƒ"),                 "f"),
    (sanitize.re(r"∫"),                 "S"),
    (sanitize.re(r"ß"),                 "ss"),
    (sanitize.re(r"ﬂ"),                 "fl"),
    (sanitize.re(r"ﬁ"),                 "fi"),
    (sanitize.re(r"£"),                 "lb."),
    (sanitize.re(r""),                 "Apple"),
    (sanitize.re(r"⌘"),                 "command"),
    (sanitize.re(r"∞"),                 "infinity"),
    (sanitize.re(r'√(?P<arg>[\w\d]*)'), r'sqrt(\g<arg>)'),
    (sanitize.re(r"¶"),                 "[P]"),
    (sanitize.re(r"[∂∆]"),              "d"),
    (sanitize.re(r"Ø"),                 "0"),
    (sanitize.re(r"→"),                 "->"),
    (sanitize.re(r"¬"),                 "-]"),
    (sanitize.re(r"…"),                 "..."),
    (sanitize.re(r"©"),                 "(c)"),
    (sanitize.re(r"®"),                 "(r)"),
    (sanitize.re(r"™"),                 "(tm)"),
    (sanitize.re(r"—"),                 "-"))

sanitizers = lambda: tuple((sani.pattern, sub) for sani, sub in sanitize.sanitizers)

if PY3:
    def utf8_encode(source):
        """ Encode a source as a UTF-8 bytes object using Python 3 semantics """
        if type(source) is bytes:
            return source
        elif type(source) is bytearray:
            return bytes(source)
        return bytes(source, encoding=utf8_encode.encoding)
    
    def utf8_decode(source):
        """ Decode a source from UTF-8 bytes to a string using Python 3 semantics """
        if type(source) in (bytes, bytearray):
            return str(source, encoding=utf8_decode.encoding)
        return source

else:
    def utf8_encode(source):
        """ Encode a source as a UTF-8 bytestring using Python 2 semantics """
        if type(source) is unicode:
            return source.encode(utf8_encode.encoding)
        elif type(source) is bytearray:
            return str(source)
        return source
    
    def utf8_decode(source):
        """ Decode a source from a UTF-8 bytestring to Unicode using Python 2 semantics """
        if type(source) in (str, bytearray):
            return source.decode(utf8_decode.encoding)
        return source

utf8_encode.encoding = utf8_decode.encoding = ENCODING

__all__ = ('sanitize', 'sanitizers', 'utf8_encode', 'utf8_decode')
__dir__ = lambda: list(__all__)
