# -*- coding: utf-8 -*-
from __future__ import print_function

from clu.constants import consts

import os
import pytest

class TestFsMisc(object):
    
    """ Run the tests for the clu.fs.misc module. """
    
    def test_modeflags(self, consts):
        from clu.fs.misc import modeflags
        from tempfile import _bin_openflags as binflags, _text_openflags as textflags
        
        # N.B. the DELETE_FLAG const is zero on non-Windows systems
        
        assert modeflags('r') == textflags | consts.DELETE_FLAG
        assert modeflags('w') == textflags | consts.DELETE_FLAG
        assert modeflags('rb') == binflags | consts.DELETE_FLAG
        assert modeflags('wb') == binflags | consts.DELETE_FLAG
        
        assert modeflags('r', delete=False) == textflags
        assert modeflags('w', delete=False) == textflags
        assert modeflags('rb', delete=False) == binflags
        assert modeflags('wb', delete=False) == binflags
    
    def test_gethomedir(self, environment):
        from clu.fs.misc import gethomedir
        if 'HOME' in environment:
            # it’s cached, so do it twice:
            assert gethomedir() == environment['HOME']
            assert gethomedir() == environment['HOME']
    
    def test_re_matcher(self):
        from clu.fs.misc import re_matcher
        
        always = re_matcher(None)
        assert always()
        assert always('yo')
        assert always('yo dogg')
        
        yo = re_matcher('yo')
        assert yo('yo')
        assert yo('yo dogg')
        assert not yo('dogg')
        assert not yo('dogg yo')
    
    def test_re_searcher(self):
        from clu.fs.misc import re_searcher
        
        always = re_searcher(None)
        assert always()
        assert always('yo')
        assert always('yo dogg')
        
        yo = re_searcher('yo')
        assert yo('yo')
        assert yo('yo dogg')
        assert not yo('dogg')
        assert yo('dogg yo')
    
    def test_re_suffix(self):
        from clu.fs.misc import re_suffix
        
        assert re_suffix(None) is None
        assert re_suffix('') is None
        assert re_suffix(".jpg") == "jpg$"
        assert re_suffix("jpg") == "jpg$"
        assert re_suffix(".jpg$") == "jpg$"
        assert re_suffix(".JPG") == "jpg$"
        assert re_suffix("JPG") == "jpg$"
        assert re_suffix(".JPG$") == "jpg$"
    
    def test_suffix_searcher(self, dirname):
        from clu.fs.misc import suffix_searcher
        from clu.testing.utils import countfiles
        from clu.typology import iterlen
        from collections import Counter
        
        data = dirname.subdirectory('data')
        suffixes = tuple(data.suffixes()) + (None,) # None → count everything!
        searchers = { suffix : suffix_searcher(suffix) for suffix in suffixes }
        counts = Counter({ suffix : 0 for suffix in suffixes })
        
        for root, dirs, files in data.walk():
            for suffix in suffixes:
                counts[suffix] += iterlen(filter(searchers[suffix], files))
        
        histo = data.suffix_histogram()
        for suffix in histo.keys():
            assert counts[suffix] == histo[suffix]
        
        # The LHS here can pick up random shit occasionally:
        # assert sum(histo.values()) + 1 == counts[None]
        assert countfiles(data) == counts[None]
    
    def test_re_excluder(self):
        from clu.fs.misc import re_excluder
        from clu.typology import iterlen
        
        # tonestr('so', 'la', 'ti', 'do') → 'tones: SO-LA-TI-DO'
        tonestr = lambda *tones: f"tones: {'-'.join(t.upper() for t in tones)}"
        
        strings = (
            tonestr(),
            tonestr('do'),
            tonestr('do', 're'),
            tonestr('do', 're', 'mi'),
            tonestr('do', 're', 'mi', 'fa'),
            tonestr('do', 're', 'mi', 'fa', 'so'),
            tonestr('do', 're', 'mi', 'fa', 'so', 'la'),
            tonestr('do', 're', 'mi', 'fa', 'so', 'la', 'ti'),
            tonestr('do', 're', 'mi', 'fa', 'so', 'la', 'ti', 'do'),
        )
        
        assert iterlen(filter(re_excluder('do'), strings)) == 1
        assert iterlen(filter(re_excluder('re'), strings)) == 2
        assert iterlen(filter(re_excluder('mi'), strings)) == 3
        
        assert iterlen(filter(re_excluder('ti-do'), strings)) == 8
        assert iterlen(filter(re_excluder('la-ti'), strings)) == 7
        assert iterlen(filter(re_excluder('so-la'), strings)) == 6
        
        assert iterlen(filter(re_excluder('fa-so', 'la-ti'), strings)) == 5
        assert iterlen(filter(re_excluder('ti-do', 'la-ti'), strings)) == 7
        assert iterlen(filter(re_excluder('do-', '-do'), strings)) == 2 # Aha!
        assert iterlen(filter(re_excluder('-mi-'), strings)) == 4
    
    def test_swapext(self):
        from clu.fs.misc import swapext
        
        assert swapext('/yo/dogg.obj', 'odb') == '/yo/dogg.odb'
        assert swapext('/yo/dogg.obj', '.odb') == '/yo/dogg.odb'
        assert swapext('/yo/dogg', 'odb') == '/yo/dogg.odb'
    
    def test_filesize_samesize(self, dirname, temporaryname):
        from clu.testing.utils import countfiles
        from clu.fs.misc import filesize, samesize
        from clu.constants.exceptions import FilesystemError
        
        # Ensure the “data” directory has something
        # in it, of which we can make use:
        data = dirname.subdirectory('data')
        assert countfiles(data) > 10
        
        # Use a TemporaryName instance for the zip archive:
        tzip = temporaryname(prefix='test-fs-misc-filesize-',
                             suffix='zip')
        
        # Create a large zipfile with that instance:
        fzip = data.zip_archive(tzip.name)
        
        # Check the zipfile’s size attributes:
        assert tzip.exists
        assert tzip.filesize > 10000
        assert os.path.exists(tzip)
        assert filesize(tzip.name) > 10000
        
        assert os.path.exists(fzip)
        assert os.path.samefile(tzip, fzip)
        assert samesize(tzip, fzip)
        assert filesize(fzip) > 10000
        
        assert filesize(tzip.name) == filesize(fzip)
        assert filesize(tzip.name) != -1
        assert filesize(fzip) != -1
        
        # Create a nonexistant TemporaryName instance:
        nofile = temporaryname(prefix='test-fs-misc-filesize-',
                               suffix='none')
        
        # Check the nonexistant files’ size attributes:
        assert not nofile.exists
        assert nofile.filesize == -1
        assert not os.path.exists(nofile)
        assert filesize(nofile.name) == -1
        
        with pytest.raises(FilesystemError) as exc:
            assert samesize(tzip, nofile)
        assert "paths must both" in str(exc.value)
        
        with pytest.raises(FilesystemError) as exc:
            assert samesize(fzip, nofile)
        assert "paths must both" in str(exc.value)
    
    def test_differentfile_differentsize_samesize(self, dirname, temporaryname):
        from clu.fs.misc import differentfile, differentsize, samesize
        
        data = "YO DOGG!, " * 1000
        data += "YO DOGG."
        
        somefile = temporaryname(prefix='test-fs-misc-differentfile-',
                                 suffix='wat')
        somefile.write(data)
        
        for root, dirs, files in dirname.subdirectory('data').walk():
            for someotherfile in files:
                theother = os.path.join(root, someotherfile)
                assert differentfile(theother, somefile)
                assert differentsize(theother, somefile)
                assert not samesize(theother, somefile)
        
        yetanotherfile = temporaryname(prefix='test-fs-misc-differentfile-',
                                       suffix='wat')
        yetanotherfile.write(data)
        assert samesize(somefile, yetanotherfile)
        assert differentfile(somefile, yetanotherfile)
        assert not differentsize(somefile, yetanotherfile)
    
    def test_u8bytes_and_u8str(self):
        from clu.fs.misc import u8bytes, u8str
        from clu.predicates import tuplize
        from itertools import chain
        from decimal import Decimal
        
        iterchain = chain.from_iterable
        
        rstr = ("yo dogg", '')
        byts = (b"YO DOGG!", b'')
        buls = (True, False)
        bnts = tuplize(None)
        numb = (3, 3.14, complex(3, 4), Decimal(3.14))
        each = (rstr, byts, buls, bnts, numb)
        
        for thing in iterchain(each):
            assert type(u8bytes(thing)) is bytes
            assert type(u8str(thing)) is str
    
    @pytest.mark.skipif(consts.PYPY, reason="Failure on PyPy")
    def test_umask_values(self):
        from clu.fs.filesystem import back_tick
        from clu.fs.misc import octalize, current_umask
        
        # Do it a bunch of times to affirm the caching stuff works:
        assert octalize(current_umask()) == "0o%s" % back_tick('umask')
        assert octalize(current_umask()) == "0o%s" % back_tick('umask')
        assert octalize(current_umask()) == "0o%s" % back_tick('umask')
        assert octalize(current_umask()) == "0o%s" % back_tick('umask')
    
    @pytest.mark.TODO
    def test_win32_longpath(self):
        """ Win32 longpath test TODO """
        win32com_shell = pytest.importorskip('win32com.shell')
        assert bool(win32com_shell)
