# -*- coding: utf-8 -*-
from __future__ import print_function

""" CLU’s Custom exception classes live here """

class BadDotpathWarning(Warning):
    """ Conversion from a path to a dotpath resulted in a bad dotpath
        … likely there are invalid characters like dashes in there.
    """
    pass

class CDBError(Exception):
    """ A problem with a compilation database """
    pass

class ConfigurationError(Exception):
    """ An error that occurred in the course of macro configuration """
    pass

class ExecutionError(Exception):
    """ An error during the execution of a shell command """
    pass

class ExportError(NameError):
    """ An error during the preparation of an item for export """
    pass

class ExportWarning(Warning):
    """ A non-life-threatening condition that occured during an export """
    pass

class FilesystemError(Exception):
    """ An error that occurred while mucking about with the filesystem """
    pass

class KeyValueError(ValueError):
    """ An error raised in the clu.keyvalue API """
    pass

class Nondeterminism(Exception):
    """ An error indicating a “heisenbug” –
        a nondeterministic problem.
    """

__all__ = ('BadDotpathWarning',
           'CDBError',
           'ConfigurationError',
           'ExecutionError', 'FilesystemError',
           'ExportError', 'ExportWarning',
           'KeyValueError',
           'Nondeterminism')

__dir__ = lambda: list(__all__)