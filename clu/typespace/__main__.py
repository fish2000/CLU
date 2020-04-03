
import sys # pragma: no cover

def test():
    
    from clu.testing.utils import inline
    
    from clu.constants.consts import pytuple, BASEPATH, VERBOTEN
    from clu.typespace import typed, types, prepare_types_ns, modulize
    
    @inline
    def test_one():
        """ Check the typespace (the “types” namespace) """
        import types as thetypes
        
        for typename in dir(thetypes):
            
            if typename.endswith('Type'):
                shortname = typed.match(typename).group('typename')
                assert hasattr(types, shortname)
                assert getattr(types, shortname) == getattr(thetypes, typename)
            
            elif typename not in VERBOTEN:
                # Can’t assert equality – many of these are different:
                assert hasattr(types, typename)
    
    # __doc__ won’t be equal as we reset it during the export;
    # and neither will the name attributes, like by definition:
    verboten = VERBOTEN + pytuple('doc', 'name', 'qualname')
    
    @inline
    def test_two():
        """ Check the output of the “prepare_types_ns(…)” function """
        moretypes = prepare_types_ns(path=__file__, basepath=BASEPATH)
        
        for typename in dir(types):
            if typename not in verboten:
                assert types[typename] == getattr(moretypes, typename)
                # print("UNEQUAL:", typename, types[typename], moretypes[typename])
    
    @inline
    def test_three():
        """ Check modulization """
        moretypes = prepare_types_ns(path=__file__, basepath=BASEPATH)
        modulize('moretypes', moretypes, "A module containing aliases into the `types` module")
        
        # from pprint import pprint
        # pprint([key for key in sys.modules.keys() if key.startswith('clu')])
        
        from clu.typespace import moretypes
        
        for typename in dir(types):
            if typename not in verboten:
                assert types[typename] == getattr(moretypes, typename)
                # print("UNEQUAL:", typename, types[typename], getattr(moretypes, typename))
    
    return inline.test(100)

if __name__ == '__main__':
    sys.exit(test())
