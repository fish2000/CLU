# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants.consts import BASEPATH, DEBUG, QUALIFIER, NoDefault
from clu.exporting import (path_to_dotpath, determine_name,
                                            search_for_name,
                                            search_for_module)
from clu.exporting import Exporter, Registry

exporter = Exporter(path=__file__)
export = exporter.decorator()

# MODULE SEARCH FUNCTIONS: iterate and search modules, yielding
# names, thing values, and/or id(thing) values, matching by given
# by thing names or id(thing) values

@export
def determine_module(thing, name=None):
    """ Private module function to find the module of a thing,
        using “pickle.whichmodule(…)”
    """
    import pickle
    
    if name is not None:
        return name
    if thing is None:
        return None
    
    return pickle.whichmodule(thing, None) or name

@export
def nameof(thing, default=NoDefault):
    """ Get the name of a thing, according to its attributes,
        how it appears as a registered item in any Exporter
        subclasses, or (failing any of those) as it appears
        in the module in which it appears to be ensconced –
        … optionally specifying a “default” fallback.
    """
    from clu.predicates import pyname
    
    result = pyname(thing) or \
             Registry.nameof(thing) or \
             search_for_name(thing)
    
    if default is NoDefault:
        return dotpath_split(result)[0]
    return dotpath_split(result)[0] or default

@export
def moduleof(thing, default=NoDefault):
    """ Determine in which module a given thing is ensconced,
        and return that modules’ name as a string.
    """
    from clu.predicates import pymodule
    
    result = pymodule(thing) or \
             determine_name(
                 Registry.moduleof(thing) or \
                 search_for_module(thing)) or \
             determine_module(thing)
    
    if default is NoDefault:
        return result
    return result or default

# QUALIFIED-NAME FUNCTIONS: import by qualified name (like e.g. “yo.dogg.DoggListener”),
# assess a thing’s qualified name, etc etc.

@export
def dotpath_join(base, *addenda):
    """ Join dotpath elements together as one, á la os.path.join(…) """
    if base is None or base == '':
        return dotpath_join(*addenda)
    for addendum in addenda:
        if addendum is not None:
            if not base.endswith(QUALIFIER):
                base += QUALIFIER
            if addendum.startswith(QUALIFIER):
                if len(addendum) == 1:
                    raise ValueError(f'operand too short: {addendum}')
                addendum = addendum[1:]
            base += addendum
    # N.B. this might be overthinking it -- 
    # maybe we *want* to allow dotpaths
    # that happen to start and/or end with dots?
    while base.startswith(QUALIFIER):
        base = base[1:]
    while base.endswith(QUALIFIER):
        base = base[:-1]
    return base

@export
def dotpath_split(dotpath):
    """ For a dotted path e.g. `yo.dogg.DoggListener`,
        return a tuple `('DoggListener', 'yo.dogg')`.
        When called with a string containing no dots,
        `dotpath_split(…)` returns `(string, None)`.
    """
    if dotpath is None:
        return None, None
    head = dotpath.split(QUALIFIER)[-1]
    tail = dotpath.replace(f"{QUALIFIER}{head}", '')
    return head, tail != head and tail or None

@export
def qualified_import(qualified):
    """ Import a qualified thing-name.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    import importlib
    if QUALIFIER not in qualified:
        raise ValueError(f"qualified name required (got {qualified})")
    head, tail = dotpath_split(qualified)
    module = importlib.import_module(tail)
    imported = getattr(module, head)
    if DEBUG:
        print(f"Qualified Import: {qualified}")
    return imported

@export
def qualified_name_tuple(thing):
    """ Get the module/package and thing-name for a class or module.
        e.g. ('instakit.processors.halftone', 'FloydSteinberg')
    """
    return moduleof(thing), nameof(thing)

@export
def qualified_name(thing):
    """ Get a qualified thing-name for a thing.
        e.g. 'instakit.processors.halftone.FloydSteinberg'
    """
    mod_name, cls_name = qualified_name_tuple(thing)
    qualname = dotpath_join(mod_name, cls_name)
    if DEBUG:
        print(f"Qualified Name: {qualname}")
    return qualname

@export
def dotpath_to_prefix(dotpath, sep='-', end='-'):
    """ Convert a dotted path into a “prefix” string, suitable for
        use with e.g. clu.fs.filesystem.TemporaryDirectory –
        e.g. 'clu.typespace.namespace.SimpleNamespace' becomes:
             'clu-typespace-namespace-simplenamespace-'
    """
    if any(c is None for c in (sep, end)):
        raise ValueError(f"“sep” and “end” must be non-None (sep={sep}, end={end})")
    if not dotpath:
        raise ValueError(f"“dotpath” cannot be None or zero-length (dotpath={dotpath})")
    return dotpath.lower().replace(QUALIFIER, sep) + end

@export
def path_to_prefix(path, sep='-', end='-', relative_to=BASEPATH):
    """ Shortcut for dotpath_to_prefix(path_to_dotpath(…)) """
    return dotpath_to_prefix(path_to_dotpath(path,
                                             relative_to=relative_to),
                             sep=sep,
                             end=end)

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
