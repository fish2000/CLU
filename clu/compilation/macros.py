# -*- coding: utf-8 -*-
from __future__ import print_function

from constants import ENCODING, ConfigurationError
from typespace import SimpleNamespace
from typology import isstring
from fs import stringify, u8str

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

class Macros(SimpleNamespace):
    
    __slots__ = tuple()
    
    def define(self, name, definition=None,
                           *,
                           undefine=False):
        return self.add(Macro(name,
                              definition,
                              undefine=undefine))
    
    def undefine(self, name, **kwargs):
        return self.add(Macro(name, undefine=True))
    
    def add(self, macro):
        name = macro.name
        if bool(macro):
            # macro is defined:
            self[name] = macro.definition or Macro.STRING_ONE
        else:
            # macro is an undef macro:
            self[name] = Macro.STRING_ZERO
        return macro
    
    def delete(self, name, **kwargs):
        if name in self:
            del self[name]
            return True
        return False
    
    def definition_for(self, name):
        if name not in self:
            return Macro(name, undefine=True)
        return Macro(name, self[name])
    
    def to_list(self):
        out = []
        for k, v in self.items():
            out.append(Macro(k, v).to_tuple())
        return out
    
    def to_tuple(self):
        return tuple(self.to_list())
    
    def to_string(self):
        global TOKEN
        stringified = TOKEN.join(Macro(k, v).to_string() for k, v in self.items()).strip()
        return f"{TOKEN.lstrip()}{stringified}"
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.to_string(), encoding=ENCODING)

__all__ = ('Macro', 'Macros')
__dir__ = lambda: list(__all__)
