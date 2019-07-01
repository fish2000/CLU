# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import pickle
import warnings

from constants import BASEPATH, BUILTINS, DEBUG, QUALIFIER
from constants import BadDotpathWarning
from exporting import determine_name, Exporter
# from predicates import pyattr

exporter = Exporter()
export = exporter.decorator()

# MODULE SEARCH FUNCTIONS: iterate and search modules, yielding
# names, thing values, and/or id(thing) values, matching by given
# by thing names or id(thing) values

@export
def itermodule(module):
    """ Get an iterable of `(name, thing)` tuples for all things
        contained in a given module (although it’ll probably work
        for classes and instances too – anything `dir()`-able.)
    """
    keys = tuple(key for key in sorted(dir(module)) \
                      if key not in BUILTINS)
    values = (getattr(module, key) for key in keys)
    return zip(keys, values)

@export
def moduleids(module):
    """ Get a dictionary of `(name, thing)` tuples from a module,
        indexed by the `id()` value of `thing`
    """
    out = {}
    for key, thing in itermodule(module):
        out[id(thing)] = (key, thing)
    return out

@export
def thingname(original, *modules):
    """ Find the name of a thing, according to what it is called
        in the context of a module in which it resides
    """
    inquestion = id(original)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for module in frozenset(modules):
            for key, thing in itermodule(module):
                if id(thing) == inquestion:
                    return key
    return None

@export
def nameof(thing, fallback=''):
    """ Get the name of a thing, according to either:
        >>> thing.__qualname__
        … or:
        >>> thing.__name__
        … optionally specifying a fallback string.
    """
    return determine_name(thing) or fallback

@export
def determine_module(thing):
    """ Determine in which module a given thing is ensconced,
        and return that modules’ name as a string.
    """
    # return pyattr(thing, 'module', 'package') or \
    #        determine_name(
    #        thingname_search_by_id(id(thing))[0])
    return pickle.whichmodule(thing, None)

# QUALIFIED-NAME FUNCTIONS: import by qualified name (like e.g. “yo.dogg.DoggListener”),
# assess a thing’s qualified name, etc etc.

@export
def path_to_dotpath(path):
    """ Convert a file path (e.g. “/yo/dogg/iheard/youlike.py”)
        to a dotpath (á la “yo.dogg.iheard.youlike”) in what I
        would call a “quick and dirty” fashion.
        
        Issues a BadDotpathWarning if the converted path contains
        dashes – I don’t quite know what to do about something
        like that besides warn, so erm. There you go.
    """
    # Relativize the path to the BASEPATH,
    # and replace slashes with dots:
    relpath = os.path.relpath(path, start=BASEPATH)
    dotpath = relpath.replace(os.path.sep, QUALIFIER)
    
    # Trim off any remaining “.py” suffixes,
    # and extraneous dot-prefixes:
    if dotpath.endswith('.py'):
        dotpath = dotpath[:len(dotpath)-3]
    while dotpath.startswith(QUALIFIER):
        dotpath = dotpath[1:]
    
    # Warn before returning, if the converted path
    # should contain dashes:
    if '-' in dotpath:
        warnings.warn("Dotpath contains dashes: “%s”" % dotpath,
                      BadDotpathWarning, stacklevel=2)
    
    return dotpath

@export
def dotpath_join(base, *addenda):
    """ Join dotpath elements together as one, á la os.path.join(…) """
    if base is None or base == '':
        return dotpath_join(*addenda)
    for addendum in addenda:
        if not base.endswith(QUALIFIER):
            base += QUALIFIER
        if addendum.startswith(QUALIFIER):
            if len(addendum) == 1:
                raise ValueError('operand too short: %s' % addendum)
            addendum = addendum[1:]
        base += addendum
    # N.B. this might be overthinking it -- 
    # maybe we *want* to allow dotpaths
    # that happen to start and/or end with dots?
    if base.endswith(QUALIFIER):
        return base[:-1]
    return base

@export
def dotpath_split(dotpath):
    """ For a dotted path e.g. `yo.dogg.DoggListener`,
        return a tuple `('DoggListener', 'yo.dogg')`.
        When called with a string containing no dots,
        `dotpath_split(…)` returns `(string, None)`.
    """
    head = dotpath.split(QUALIFIER)[-1]
    tail = dotpath.replace("%s%s" % (QUALIFIER, head), '')
    return head, tail != head and tail or None

@export
def qualified_import(qualified):
    """ Import a qualified thing-name.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    import importlib
    if QUALIFIER not in qualified:
        raise ValueError("qualified name required (got %s)" % qualified)
    head, tail = dotpath_split(qualified)
    module = importlib.import_module(tail)
    imported = getattr(module, head)
    if DEBUG:
        print("Qualified Import: %s" % qualified)
    return imported

@export
def qualified_name_tuple(thing):
    """ Get the module/package and thing-name for a class or module.
        e.g. ('instakit.processors.halftone', 'FloydSteinberg')
    """
    return determine_module(thing), \
           dotpath_split(
           determine_name(thing))[0]

@export
def qualified_name(thing):
    """ Get a qualified thing-name for a thing.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    mod_name, cls_name = qualified_name_tuple(thing)
    qualname = dotpath_join(mod_name, cls_name)
    if DEBUG:
        print("Qualified Name: %s" % qualname)
    return qualname

@export
def split_abbreviations(s):
    """ Split a string into a tuple of its unique constituents,
        based on its internal capitalization -- to wit:
        
        >>> split_abbreviations('RGB')
        ('R', 'G', 'B')
        >>> split_abbreviations('CMYK')
        ('C', 'M', 'Y', 'K')
        >>> split_abbreviations('YCbCr')
        ('Y', 'Cb', 'Cr')
        >>> split_abbreviations('sRGB')
        ('R', 'G', 'B')
        >>> split_abbreviations('XYZZ')
        ('X', 'Y', 'Z')
        >>> split_abbreviations('I;16B')
        ('I',)
        
        If you still find this function inscrutable,
        have a look here: https://gist.github.com/4027079
    """
    abbreviations = []
    current_token = ''
    for char in s.split(';')[0]:
        if current_token == '':
            current_token += char
        elif char.islower():
            current_token += char
        else:
            if not current_token.islower():
                if current_token not in abbreviations:
                    abbreviations.append(current_token)
            current_token = ''
            current_token += char
    if current_token != '':
        if current_token not in abbreviations:
            abbreviations.append(current_token)
    return tuple(abbreviations)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
