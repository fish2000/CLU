# -*- coding: utf-8 -*-
from __future__ import print_function

# import pytest

class TestEnumAliases(object):
    
    """ Run the tests for the clu.enums module. """
    
    def test_alias_basic_enum(self):
        from enum import Enum, unique
        from clu.enums import alias
        
        @unique
        class Numbers(Enum):
            """ This is literally the example from the alias
                object docstring.
            """
            ONE = 1
            TWO = 2
            THREE = 3
            UNO = alias(ONE)
            DOS = alias(TWO)
            TRÉS = alias(THREE)
        
        # Members and aliases are the same instances:
        assert Numbers.UNO  is Numbers.ONE
        assert Numbers.DOS  is Numbers.TWO
        assert Numbers.TRÉS is Numbers.THREE
        
        # Aliases on basic Enum subclasses aren’t registered
        # in an “__aliases__” dict on the Enum subclass itself:
        assert not hasattr(Numbers, '__aliases__')
        assert len(getattr(Numbers, '__aliases__', {})) == 0
        
        # len(Numbers) reflects only the non-alias members:
        assert len(Numbers) == 3
    
    def test_aliasing_enum_metaclass(self):
        from enum import Enum, unique
        from clu.enums import alias, AliasingEnumMeta
        
        @unique
        class Numbers(Enum, metaclass=AliasingEnumMeta):
            """ This Enum subclass has AliasingEnumMeta
                as its metaclass.
            """
            ONE = 1
            TWO = 2
            THREE = 3
            UNO = alias(ONE)
            DOS = alias(TWO)
            TRÉS = alias(THREE)
        
        # Members and aliases are the same instances:
        assert Numbers.UNO  is Numbers.ONE
        assert Numbers.DOS  is Numbers.TWO
        assert Numbers.TRÉS is Numbers.THREE
        
        # Aliases on Enum subclasses that use AliasingEnumMeta
        # register their aliases in an “__aliases__” dict on
        # the Enum subclass itself:
        assert hasattr(Numbers, '__aliases__')
        assert len(getattr(Numbers, '__aliases__', {})) == 3
        
        # len(Numbers) reflects only the non-alias members:
        assert len(Numbers) == 3
    
    def test_aliasing_enum_subclass(self):
        from enum import unique
        from clu.enums import alias, AliasingEnum
        
        @unique
        class Numbers(AliasingEnum):
            """ This is a subclass of AliasingEnum, itself
                an intermediate Enum subclass that furnishes
                the AliasingEnumMeta metaclass.
            """
            ONE = 1
            TWO = 2
            THREE = 3
            UNO = alias(ONE)
            DOS = alias(TWO)
            TRÉS = alias(THREE)
        
        # Members and aliases are the same instances:
        assert Numbers.UNO  is Numbers.ONE
        assert Numbers.DOS  is Numbers.TWO
        assert Numbers.TRÉS is Numbers.THREE
        
        # Aliases on AliasingEnum subclasses register their
        # aliases in an “__aliases__” dict on the AliasingEnum
        # subclass itself:
        assert hasattr(Numbers, '__aliases__')
        assert len(getattr(Numbers, '__aliases__', {})) == 3
        
        # len(Numbers) reflects only the non-alias members:
        assert len(Numbers) == 3