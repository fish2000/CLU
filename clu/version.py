import re, os

if not hasattr(__builtins__, 'cmp'):
    def cmp(a, b):
        return (a > b) - (a < b)

from collections import OrderedDict, namedtuple as NamedTuple
from functools import wraps
from pkg_resources import parse_version as pkg_resources_parse_version
from pkg_resources.extern.packaging.version import Version as PkgResourcesVersion

FIELDS = ('major', 'minor', 'patch',
          'pre',   'build')

# The `namedtuple` ancestor,
# from which our VersionInfo struct inherits:
VersionAncestor = NamedTuple('VersionAncestor', FIELDS)

# sets, for various comparisons and checks:
fields = frozenset(FIELDS)
string_types = { type(lit) for lit in ('', u'', r'') }
byte_types = { bytes, bytearray } - string_types # On py2, bytes == str
dict_types = { dict, OrderedDict }
comparable = dict_types | { VersionAncestor }

# utility conversion functions:
def intify(arg):
    if arg is None:
        return None
    return int(arg)

def strify(arg):
    if arg is None:
        return None
    if type(arg) in string_types:
        return arg
    if type(arg) in byte_types:
        return arg.decode('UTF-8')
    return str(arg)

def dictify(arg):
    if arg is None:
        return None
    if hasattr(arg, '_asdict'):
        return arg._asdict()
    if hasattr(arg, 'to_dict'):
        return arg.to_dict()
    if type(arg) in dict_types:
        return arg
    return dict(arg)

# compare version information by dicts:
def compare_keys(dict1, dict2):
    """ Blatantly based on code from “semver”: https://git.io/fhb98 """
    
    for key in ('major', 'minor', 'patch'):
        result = cmp(dict1.get(key), dict2.get(key))
        if result:
            return result
    
    pre1, pre2 = dict1.get('pre'), dict2.get('pre')
    if pre1 is None and pre2 is None:
        return 0
    if pre1 is None:
        pre1 = '<unknown>'
    elif pre2 is None:
        pre2 = '<unknown>'
    preresult = cmp(pre1, pre2)
    
    if not preresult:
        return 0
    if not pre1:
        return 1
    elif not pre2:
        return -1
    return preresult

# comparison-operator method decorator:
def comparator(operator):
    """ Wrap a VersionInfo binary op method in a typechecker """
    @wraps(operator)
    def wrapper(self, other):
        if not isinstance(other, tuple(comparable)):
            return NotImplemented
        return operator(self, other)
    return wrapper

# the VersionInfo class:
class VersionInfo(VersionAncestor):
    
    """ NamedTuple-descendant class allowing for convenient
        and reasonably sane manipulation of semantic-version
        (née “semver”) string-triple numberings, or whatever
        the fuck is the technical term for them, erm. Yes!
    """
    
    SEPARATORS = '..-+'
    UNKNOWN = '‽'
    NULL_VERSION = "%s.%s.%s" % ((UNKNOWN,) * 3)
    REG = re.compile('(?P<major>[\d‽]+)\.'     \
                     '(?P<minor>[\d‽]+)'       \
                     '(?:\.(?P<patch>[\d‽]+)'  \
                     '(?:\-(?P<pre>[\w‽]+)'    \
                     '(?:\+(?P<build>[\d‽]+))?)?)?')
    
    @classmethod
    def from_string(cls, version_string):
        """ Instantiate a VersionInfo with a semver string """
        result = cls.REG.search(version_string)
        if result:
            return cls.from_dict(result.groupdict())
        return cls.from_dict({ field : cls.UNKNOWN for field in FIELDS })
    
    @classmethod
    def from_dict(cls, version_dict):
        """ Instantiate a VersionInfo with a dict of related values
            (q.v. FIELD string names supra.)
        """
        for field in FIELDS[:2]: # major, minor
            assert field in version_dict
        assert frozenset(version_dict.keys()).issubset(fields)
        return cls(**version_dict)
    
    def to_string(self):
        """ Return the VersionInfo data as a semver string """
        if not bool(self):
            return type(self).NULL_VERSION
        SEPARATORS = type(self).SEPARATORS
        out = "%i%s%i" % (self.major or 0, SEPARATORS[0],
                          self.minor or 0)
        if self.patch is not None:
            out += "%s%i" % (SEPARATORS[1], self.patch)
            if self.pre:
                out += "%s%s" % (SEPARATORS[2], self.pre)
                if self.build:
                    out += "%s%i" % (SEPARATORS[3], self.build)
        return out
    
    def to_dict(self):
        """ Really an OrderedDict but who’s counting? """
        out = OrderedDict()
        for field in FIELDS:
            if getattr(self, field, None) is not None:
                out[field] = getattr(self, field)
        return out
    
    def to_tuple(self):
        """ Return a complete tuple (as in, including “pre” and “build” fields) """
        return (self.major, self.minor, self.patch,
                self.pre, self.build)
    
    def to_packaging_version(self):
        """ aka an instance of `pkg_resources.extern.packaging.version.Version` """
        return pkg_resources_parse_version(self.to_string())
    
    def __new__(cls, from_value=None, major='‽', minor='‽',
                                      patch='‽', pre='‽',
                                      build=0):
        """ Instantiate a VersionInfo, populating its fields per args """
        if from_value is not None:
            if type(from_value) in string_types:
                return cls.from_string(from_value)
            elif type(from_value) is PkgResourcesVersion:
                return cls.from_string(str(from_value))
            elif type(from_value) in byte_types:
                return cls.from_string(from_value.decode('UTF-8'))
            elif type(from_value) in dict_types:
                return cls.from_dict(from_value)
            elif type(from_value) is cls:
                return cls.from_dict(from_value.to_dict())
        if cls.UNKNOWN in str(major):
            major = None
        if cls.UNKNOWN in str(minor):
            minor = None
        if cls.UNKNOWN in str(patch):
            patch = None
        if cls.UNKNOWN in str(pre):
            pre = None
        if cls.UNKNOWN in str(build):
            build = 0
        instance = super(VersionInfo, cls).__new__(cls, intify(major),
                                                        intify(minor),
                                                        intify(patch),
                                                        strify(pre),
                                                               build)
        return instance
    
    def __str__(self):
        """ Stringify the VersionInfo (q.v. “to_string(…)” supra.) """
        return self.to_string()
    
    def __bytes__(self):
        """ Bytes-ify the VersionInfo (q.v. “to_string(…)” supra.) """
        return bytes(self.to_string())
    
    def __hash__(self):
        """ Hash the VersionInfo, using its tuplized value """
        return hash(self.to_tuple())
    
    def __bool__(self):
        """ An instance of VersionInfo is considered Falsey if its “major”,
           “minor”, and “patch” fields are all set to None; otherwise it’s
            a Truthy value in boolean contexts
        """
        return not (self.major is None and \
                    self.minor is None and \
                    self.patch is None)
    
    # Comparison methods also lifted from “semver”: https://git.io/fhb9i
    
    @comparator
    def __eq__(self, other):
        return compare_keys(self._asdict(), dictify(other)) == 0
    
    @comparator
    def __ne__(self, other):
        return compare_keys(self._asdict(), dictify(other)) != 0
    
    @comparator
    def __lt__(self, other):
        return compare_keys(self._asdict(), dictify(other)) < 0
    
    @comparator
    def __le__(self, other):
        return compare_keys(self._asdict(), dictify(other)) <= 0
    
    @comparator
    def __gt__(self, other):
        return compare_keys(self._asdict(), dictify(other)) > 0
    
    @comparator
    def __ge__(self, other):
        return compare_keys(self._asdict(), dictify(other)) >= 0

# Inline tests:
def test(version):
    # global __version__
        
    # The CLU project version:
    print("__version__ in globals():", '__version__' in globals())
    print("__version__ in locals():", '__version__' in locals())
    print("__version__:", __version__)
    
    # print(VersionInfo.REG)
    print("VersionInfo Instance:", repr(version))
    print("Semantic Version:", version)
    
    assert version  < VersionInfo("9.0.0")
    assert version == VersionInfo(version)
    assert version == VersionInfo(__version__)
    assert version == VersionInfo(PkgResourcesVersion(__version__))
    assert version == VersionInfo(str(PkgResourcesVersion(__version__)))
    assert version <= VersionInfo(__version__)
    assert version >= VersionInfo(__version__)
    assert version  > VersionInfo(b'0.0.1')
    assert version != VersionInfo(b'0.0.1')
    
    assert bool(version)
    assert not bool(VersionInfo('‽.‽.‽'))
    
    print("All assertions passed")

# get the project version tag without importing:
__version__ = "<undefined>"
BASEPATH = os.path.dirname(__file__)

try:
    exec(compile(open(os.path.join(BASEPATH, '__version__.py')).read(),
                                             '__version__.py', 'exec'))
except:
    import traceback, sys
    print("ERROR: failed to parse __version__.py")
    traceback.print_exc(file=sys.stdout)
    __version__ = '0.1.0'

version = VersionInfo(__version__)

if __name__ == '__main__':
    test(version)