# -*- coding: utf-8 -*-
from __future__ import print_function

find_hex_id = lambda function: repr(function).split()[-1].rstrip('>')

test_lambda = lambda: 'yo dogg'
test_hex_id = find_hex_id(test_lambda)

class TestRepr(object):
    
    """ Run the tests for the clu.repr module. """
    
    def test_strfield(self):
        # from clu.constants.consts import SINGLETON_TYPES
        from clu.repr import strfield
        from clu.typespace.namespace import Namespace
        from decimal import Decimal
        from enum import Enum, unique
        
        rstr = "yo dogg"
        byts = b"YO DOGG!"
        # sngl = (True, False, None, ..., NotImplemented)
        # numb = (3, 3.14, complex(3, 4), Decimal(3.14))
        # each = (rstr, byts, buls, bnts, numb)
        dic = { 'yo' : 'dogg' }
        ns = Namespace(yo='dogg')
        l = ['yo', 'dogg']
        t = ('yo', 'dogg')
        
        @unique
        class Things(Enum):
            
            YO = 'yo'
            DOGG = 'dogg'
            I = 'I'
            HEARD = 'heard'
        
        assert strfield(rstr)           == "“yo dogg”"
        assert strfield(byts)           == "“YO DOGG!”"
        assert strfield(dic)            == '{ yo=dogg }'
        assert strfield(ns)             == "{ yo : 'dogg' }"
        assert strfield(l)              == '[ “yo”, “dogg” ]'
        assert strfield(t)              == '[ “yo”, “dogg” ]'
        assert strfield(True)           == "«True»"
        assert strfield(False)          == "«False»"
        assert strfield(None)           == "«None»"
        assert strfield(...)            == "«Ellipsis»"
        assert strfield(Ellipsis)       == "«Ellipsis»"
        assert strfield(NotImplemented) == "«NotImplemented»"
        assert strfield(3)              == "3"
        assert strfield(3.14)           == "3.14"
        assert strfield(complex(3, 4))  == "(3+4j)"
        
        assert strfield(Decimal(3.14)).startswith("3.1400000000000001243")
        assert strfield(Things).startswith("‘Things<(YO, DOGG, I, HEARD) @ ")
    
    def test_chop_instance_repr(self, dirname):
        from clu.repr import chop_instance_repr, INSTANCE_DELIMITER
        data = dirname.subdirectory('data')
        
        assert chop_instance_repr(dirname)       == "Directory(name=“/Users/fish/Dropbox/CLU/clu/tests”, exists=«True»)"
        assert chop_instance_repr(data)          == "Directory(name=“/Users/fish/Dropbox/CLU/clu/tests/data”, exists=«True»)"
        assert chop_instance_repr(repr(dirname)) == "Directory(name=“/Users/fish/Dropbox/CLU/clu/tests”, exists=«True»)"
        assert chop_instance_repr(repr(data))    == "Directory(name=“/Users/fish/Dropbox/CLU/clu/tests/data”, exists=«True»)"
        assert repr(dirname).startswith(chop_instance_repr(dirname))
        assert repr(data).startswith(chop_instance_repr(data))
        
        assert repr(dirname).find(INSTANCE_DELIMITER) != -1
        assert repr(data).find(INSTANCE_DELIMITER) != -1
        assert chop_instance_repr(dirname).find(INSTANCE_DELIMITER) == -1
        assert chop_instance_repr(data).find(INSTANCE_DELIMITER) == -1
    
    def test_strfields(self):
        pass
    
    def test_strfields_slotted_class(self):
        from clu.abstract import Slotted
        from clu.repr import strfields
        import abc
        
        class Thingy(abc.ABC, metaclass=Slotted):
            
            __slots__ = ('yo', 'dogg', 'iheard', 'youlike')
            
            def __init__(self, **kwargs):
                self.yo         = kwargs.pop('yo',      'YO')
                self.dogg       = kwargs.pop('dogg',    'DOGG')
                self.iheard     = kwargs.pop('iheard',  'IHEARD')
                self.youlike    = kwargs.pop('youlike', 'YOULIKE')
            
            def __repr__(self):
                return strfields(self, self.__slots__, try_callables=False)
        
        t0 = Thingy()
        assert repr(t0) == "yo=“YO”, dogg=“DOGG”, iheard=“IHEARD”, youlike=“YOULIKE”"
    
    def test_stringify_directory_instance(self, dirname):
        from clu.fs.filesystem import Directory
        from clu.repr import stringify, chop_instance_repr
        data = dirname.subdirectory('data')
        
        assert chop_instance_repr(dirname) == chop_instance_repr(stringify(dirname, Directory.fields))
        assert chop_instance_repr(data)    == chop_instance_repr(stringify(data,    Directory.fields))
        assert chop_instance_repr(dirname) == chop_instance_repr(stringify(dirname, None))
        assert chop_instance_repr(data)    == chop_instance_repr(stringify(data,    None))
    
    def test_stringify(self):
        pass
    
    def test_stringify_slotted_class(self):
        from clu.abstract import Slotted
        from clu.repr import stringify, chop_instance_repr
        import abc
        
        class Thingy(abc.ABC, metaclass=Slotted):
            
            __slots__ = ('yo', 'dogg', 'iheard', 'youlike')
            
            def __init__(self, **kwargs):
                self.yo         = kwargs.pop('yo',      'YO')
                self.dogg       = kwargs.pop('dogg',    'DOGG')
                self.iheard     = kwargs.pop('iheard',  'IHEARD')
                self.youlike    = kwargs.pop('youlike', 'YOULIKE')
            
            def __repr__(self):
                return stringify(self, self.__slots__, try_callables=False)
        
        t0 = Thingy()
        assert chop_instance_repr(t0) == "Thingy(yo=“YO”, dogg=“DOGG”, iheard=“IHEARD”, youlike=“YOULIKE”)"
    
    def test_repr_lambdas(self):
        from clu.constants.consts import λ
        from clu.exporting import Exporter
        
        test_lambda_qualname = lambda: 'yo dogg'
        test_hex_id_qualname = find_hex_id(test_lambda_qualname)
        
        test_classname = type(self).__name__
        test_funcname = self.test_repr_lambdas.__func__.__name__
        test_qualname = f"{test_classname}.{test_funcname}.<locals>"
        
        assert repr(test_lambda) == f"<function {λ} at {test_hex_id}>"
        assert repr(test_lambda_qualname) == f"<function {test_qualname}.{λ} at {test_hex_id_qualname}>"
        
        exporter = Exporter()
        export = exporter.decorator()
        
        export(test_lambda)                         # renames using determined name of lambda
        export(test_lambda_qualname, 'yo_dogg')     # renames using provided string name
        
        assert repr(test_lambda) == f"<function test_lambda at {test_hex_id}>"
        assert repr(test_lambda_qualname) == f"<function yo_dogg at {test_hex_id_qualname}>"
