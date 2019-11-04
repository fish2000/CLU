# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants.consts import ENCODING, TOKEN
from clu.constants.exceptions import ConfigurationError
from clu.fs.misc import u8str
from clu.repr import stringify
from clu.typespace.namespace import SimpleNamespace
from clu.typology import isstring
from clu.exporting import Exporter

exporter = Exporter(path=__file__)
export = exporter.decorator()

@export
class Macro(object):
    
    __slots__ = ('name', 'definition', 'undefine')
    
    STRING_ZERO = '0'
    STRING_ONE  = '1'
    
    @staticmethod
    def is_string_value(putative, value=0):
        """ Predicate function for checking for the values of stringified integers """
        if not isstring(putative):
            return False
        intdef = 0
        try:
            intdef += int(putative, base=10)
        except ValueError:
            return False
        return intdef == int(value)
    
    def __init__(self, name, definition=None,
                             *,
                             undefine=False):
        """ Initialize a new Macro instance, specifiying a name, a definition (optionally),
            and a boolean flag (optionally) indicating that the macro is “undefined” --
            that is to say, that it is a so-called “undef macro”.
        """
        if not name:
            raise ConfigurationError("Macro() requires a valid name")
        string_zero = self.is_string_value(definition)
        string_one = self.is_string_value(definition, value=1)
        string_something = string_zero or string_one
        self.name = name
        self.definition = (not string_something or None) and definition
        self.undefine = string_zero or undefine
    
    def to_string(self):
        """ Stringify the macro instance as a GCC- or Clang-compatible command-line switch,
            e.g. “DMACRO_NAME=Some_Macro_Value” -- or just “DMACRO_NAME” or “UMACRO_NAME”,
            if applicable.
        """
        if self.undefine:
            return f"U{u8str(self.name)}"
        if self.definition is not None:
            return f"D{u8str(self.name)}={u8str(self.definition)}"
        return f"D{u8str(self.name)}"
    
    def to_tuple(self):
        """ Tuple-ize the macro instance -- return a tuple in the form (name, value)
            as per the macro’s contents. The returned tuple always has a value field;
            in the case of undefined macros, the value is '0' -- stringified zero --
            and in the case of macros lacking definition values, the value is '1' --
            stringified one.
        """
        if self.undefine:
            return (u8str(self.name),
                          self.STRING_ZERO)
        if self.definition is not None:
            return (u8str(self.name),
                    u8str(self.definition))
        return (u8str(self.name),
                      self.STRING_ONE)
    
    def __repr__(self):
        return stringify(self, type(self).__slots__)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.to_string(), encoding=ENCODING)
    
    def __bool__(self):
        """ An instance of Macro is considered Falsey if undefined, Truthy if not. """
        return not self.undefine

@export
class Macros(SimpleNamespace):
    
    __slots__ = tuple() # type: tuple
    
    def define(self, name, definition=None,
                           *,
                           undefine=False):
        """ Define a Macro within the Macrospace – specifiying a name, a definition (optionally),
            and a boolean flag (optionally) indicating that the macro is “undefined” --
            that is to say, that it is a so-called “undef macro”.
        """
        return self.add(Macro(name,
                              definition,
                              undefine=undefine))
    
    def undefine(self, name, **kwargs):
        """ Create a new “undefined” Macro within the Macrospace. Only a name needs to be specified;
            the fact of the Macro’s undefinedness is its definition and payload.
        """
        return self.add(Macro(name, undefine=True))
    
    def add(self, macro):
        """ The `add(…)` method is called by both `define(…)` and `undefine(…)` to create any sort
            of new Macro within the Macrospace. Passing a fresh Macro instance to `add(¬)` will add
            this instance to the Macrospace; do not invoke this directly unless you’re certain of
            yourself, as using a macro with an already-existing name will overwrite the contents
            of whatever was previously occupying that named entry. 
        """
        name = macro.name
        if bool(macro):
            # macro is defined:
            self[name] = macro.definition or Macro.STRING_ONE
        else:
            # macro is an undef macro:
            self[name] = Macro.STRING_ZERO
        return macro
    
    def delete(self, name, **kwargs):
        """ The `delete(…)` method will delete a Macro from the Macrospace by name; currently,
            this method accepts arbitrary kwargs but does not consider them. 
        """
        if name in self:
            del self[name]
            return True
        return False
    
    def definition_for(self, name):
        """ Use the `definition_for(…)` method to query the Macrospace – it will return a new
            Macro instance with definitions filled in from that which it matches by name; if no
            macro is found for a given name, an “undefined” macro is returned instead. As such,
            this method will always return an initialized Macro instance in a valid state.
        """
        if name not in self:
            return Macro(name, undefine=True)
        return Macro(name, self[name])
    
    def to_list(self):
        """ The `to_list()` method returns a new list, containing a tuplized version of each
            macro instance in the Macrospace – q.v. `Macro.to_tuple()` notes and implementation
            supra. for a description of this process.
        """
        out = []
        for k, v in self.items():
            out.append(Macro(k, v).to_tuple())
        return out
    
    def to_tuple(self):
        """ This is exactly like `to_list()`, above; except that the container of tuplized
            Macro instances return is a tuple instead.
        """
        return tuple(self.to_list())
    
    def to_string(self):
        """ A method to return the command-line value-equivalent of the Macrospace and its
            contents – q.v. `Macro.to_string()` notes and implementation supra. The value
            of `to_string()` should – for certain values of “should” – work out-of-the-box
            if passed to recent versions of the GCC or Clang C/C++/ObjC preprocessors.
        """
        stringified = TOKEN.join(Macro(k, v).to_string() for k, v in self.items()).strip()
        return f"{TOKEN.lstrip()}{stringified}"
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.to_string(), encoding=ENCODING)

# Assign the modules’ `__all__` and `__dir__` using the exporter:
__all__, __dir__ = exporter.all_and_dir()
