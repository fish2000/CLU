# -*- coding: utf-8 -*-
from __future__ import print_function

import re

from constants import unicode

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
    (sanitize.re(r'√(?P<arg>[\w\d]*)'), 'sqrt(\g<arg>)'),
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
