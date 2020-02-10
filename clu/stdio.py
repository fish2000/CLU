# -*- coding: utf-8 -*-
from __future__ import print_function
from dataclasses import dataclass as dataclass_fn, field, fields
from functools import lru_cache

import sys, os

from clu.constants import consts
from clu.predicates import attr, attrs
from clu.repr import stringify
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

dataclass = dataclass_fn(repr=False)
cache = lambda function: export(lru_cache()(function))
onecache = lambda function: export(lru_cache(maxsize=1)(function))

# Determine the proper output streams for the current I/O environment:
sestream = attr(sys, '__stderr__', 'stderr')
sostream = attr(sys, '__stdout__', 'stdout')
streams = attrs(sys, '__stdout__', 'stdout')

# Some basic shortcuts:
linebreak = lambda: print(file=sostream)
flush_all = lambda: (stream.flush() for stream in streams)

def terminal_size_fd():
    import fcntl, termios, struct
    descriptor = None
    try:
        descriptor = os.open(os.ctermid(), os.O_RDONLY)
        h, w, hp, wp = struct.unpack('HHHH',
            fcntl.ioctl(descriptor, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)))
        return w, h
    except OSError:
        return None, None
    finally:
        if descriptor is not None:
            os.close(descriptor)

@onecache
def terminal_size():
    """ Deeper cut than “os.get_terminal_size(…)” value in “consts” """
    # q.v. https://stackoverflow.com/a/3010495/298171 sub.
    import fcntl, termios, struct, io
    try:
        with io.open(os.ctermid()) as terminal:
            h, w, hp, wp = struct.unpack('HHHH',
                fcntl.ioctl(terminal.fileno(),
                            termios.TIOCGWINSZ,
                struct.pack('HHHH', 0, 0, 0, 0)))
    except OSError:
        return None, None
    else:
        return w, h

@export
def ctermid():
    return terminal_size()[0] and os.ctermid() or os.devnull

@export
@dataclass
class TermSize:
    
    id:     str = field(default_factory=ctermid)
    width:  int = field(default_factory=lambda: terminal_size()[0] or consts.SEPARATOR_WIDTH)
    height: int = field(default_factory=lambda: terminal_size()[1] or 0)
    
    def __repr__(self):
        return stringify(self,
                    type(self).fields,
                         try_callables=False)

# Sort this out once (when the module loads) instead of each
# and every fucking time a TermSize instance is to get repr’d:
TermSize.fields = tuple(field.name for field in fields(TermSize))

# NO DOCS ALLOWED:
export(sestream,            name='sestream')
export(sostream,            name='sostream')
export(streams,             name='streams')

export(linebreak,           name='linebreak',       doc="linebreak() → print a newline to `stdout`")
export(flush_all,           name='flush_all',       doc="flush_all() → flush the output buffers of all possible `stdout` candidates")

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()

def test():
    
    from clu.testing.utils import inline
    
    @inline
    def test_one():
        terminal_size()
    
    @inline
    def test_two():
        print(terminal_size_fd())
        print(TermSize())
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())

