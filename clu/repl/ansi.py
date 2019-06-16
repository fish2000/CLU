# -*- coding: utf-8 -*-
from __future__ import print_function

def print_color(text, color='', reset=None):
    """ Print text in ANSI color, using optional inline markup
        from `colorama` for terminal color-escape delimiters
    """
    import colorama
    colorama.init()
    for line in text.splitlines():
        print(color + line, sep='')
    print(reset or colorama.Style.RESET_ALL, end='')

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