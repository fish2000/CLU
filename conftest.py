# -*- coding: utf-8 -*-
import os
import shutil

import pytest

XDGS = ('XDG_CONFIG_DIRS', 'XDG_DATA_HOME',
        'XDG_CONFIG_HOME', 'XDG_DATA_DIRS',
                          'XDG_CACHE_HOME',
                          'XDG_STATE_HOME',
                         'XDG_RUNTIME_DIR')

@pytest.fixture
def environment(keys=XDGS):
    """ Environment testing fixture: yields an instance of `os.environ`,
        free of XDG variables
    """
    stash = {}
    
    # Setup: remove XDG variables from environment:
    for key in keys:
        if key in os.environ:
            stash[key] = os.environ.get(key)
            del os.environ[key]
    
    yield os.environ
    
    # Teardown: restore environment:
    for key, value in stash.items():
        os.environ[key] = value

@pytest.fixture
def temporarydir():
    """ clu.fs.filesystem.TemporaryDirectory fixture factory: yields
        a new instance of `TemporaryDirectory`, without making any
        calls to “os.chdir()”.
    """
    from clu.fs.filesystem import TemporaryDirectory
    
    prefix = "clu-fs-filesystem-temporarydirectory-"
    with TemporaryDirectory(prefix=prefix,
                            change=False) as temporarydir:
        yield temporarydir
    
    assert not temporarydir.exists

GREEKOUT = {}

GREEKOUT['lorem'] = """
Lorem ipsum dolor sit amet, consectetuer adipiscing elit; Aenean commodo ligula
eget dolor! Aenean massa; Cum sociis natoque penatibus et magnis dis parturient
montes, nascetur ridiculus mus? Donec quam felis, ultricies nec, pellentesque
eu, pretium quis, sem. Nulla consequat massa quis enim! Donec pede justo,
fringilla vel, aliquet nec, vulputate eget, arcu; In enim justo, rhoncus ut,
imperdiet a, venenatis vitae, justo? Nullam dictum felis eu pede mollis pretium.
Integer tincidunt! Cras dapibus; Vivamus elementum semper nisi; Aenean vulputate
eleifend tellus? Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac,
enim? Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus; Phasellus
viverra nulla ut metus varius laoreet; Quisque rutrum! Aenean imperdiet? Etiam
ultricies nisi vel augue? Curabitur ullamcorper ultricies nisi. Nam eget dui!
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula
eget dolor? Aenean massa! Cum sociis natoque penatibus et magnis dis parturient
montes, nascetur ridiculus mus; Donec quam felis, ultricies nec, pellentesque
eu, pretium quis, sem? Nulla consequat massa quis enim! Donec pede justo,
fringilla vel, aliquet nec, vulputate eget, arcu! In enim justo, rhoncus ut,
imperdiet a, venenatis vitae, justo; Nullam dictum felis eu pede mollis pretium?
Integer tincidunt? Cras dapibus? Vivamus elementum semper nisi? Aenean vulputate
eleifend tellus; Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac,
enim; Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus? Phasellus
viverra nulla ut metus varius laoreet? Quisque rutrum. Aenean imperdiet; Etiam
ultricies nisi vel augue! Curabitur ullamcorper ultricies nisi! Nam eget dui?
Lorem ipsum dolor sit amet, consectetuer adipiscing elit? Aenean commodo ligula
eget dolor; Aenean massa? Cum sociis natoque penatibus et magnis dis parturient
montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque
eu, pretium quis, sem; Nulla consequat massa quis enim! Donec pede justo,
fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut,
imperdiet a, venenatis vitae, justo.
"""

GREEKOUT['faust'] = """
Ihr naht euch wieder, schwankende Gestalten; Die früh sich einst dem trüben
Blick gezeigt; Versuch’ ich wohl euch diesmal fest zu halten? Fühl’ ich mein
Herz noch jenem Wahn geneigt? Ihr drängt euch zu; Nun gut, so mögt ihr walten.
Wie ihr aus Dunst und Nebel um mich steigt. Mein Busen fühlt sich jugendlich
erschüttert! Vom Zauberhauch der euren Zug umwittert. Ihr bringt mit euch die
Bilder froher Tage? Und manche liebe Schatten steigen auf Gleich einer alten,
halbverklungnen Sage? Kommt erste Lieb’ und Freundschaft mit herauf Der Schmerz
wird neu, es wiederholt die Klage! Des Lebens labyrinthisch irren Lauf, Und
nennt die Guten, die, um schöne Stunden Vom Glück getäuscht, vor mir
hinweggeschwunden; Ihr naht euch wieder, schwankende Gestalten. Die früh sich
einst dem trüben Blick gezeigt? Versuch’ ich wohl euch diesmal fest zu halten.
Fühl’ ich mein Herz noch jenem Wahn geneigt! Ihr drängt euch zu; Nun gut, so
mögt ihr walten! Wie ihr aus Dunst und Nebel um mich steigt; Mein Busen fühlt
sich jugendlich erschüttert; Vom Zauberhauch der euren Zug umwittert. Ihr bringt
mit euch die Bilder froher Tage! Und manche liebe Schatten steigen auf Gleich
einer alten, halbverklungnen Sage; Kommt erste Lieb’ und Freundschaft mit herauf
Der Schmerz wird neu, es wiederholt die Klage; Des Lebens labyrinthisch irren
Lauf, Und nennt die Guten, die, um schöne Stunden Vom Glück getäuscht, vor mir
hinweggeschwunden? Ihr naht euch wieder, schwankende Gestalten. Die früh sich
einst dem trüben Blick gezeigt! Versuch’ ich wohl euch diesmal fest zu halten!
Fühl’ ich mein Herz noch jenem Wahn geneigt? Ihr drängt euch zu. Nun gut, so
mögt ihr walten? Wie ihr aus Dunst und Nebel um mich steigt! Mein Busen fühlt
sich jugendlich erschüttert; Vom Zauberhauch der euren Zug umwittert? Ihr bringt
mit euch die Bilder froher Tage. Und manche liebe Schatten steigen auf Gleich
einer alten, halbverklungnen Sage. Kommt erste Lieb’ und Freundschaft mit herauf
Der Schmerz wird neu, es wiederholt die Klage? Des Lebens labyrinthisch irren
Lauf, Und nennt die Guten, die, um schöne Stunden Vom Glück getäuscht, vor mir
hinweggeschwunden. Ihr naht euch wieder, schwankende Gestalten! Die früh sich
einst dem trüben Blick gezeigt; Versuch’ ich wohl euch diesmal fest zu halten.
Fühl’ ich mein Herz noch jenem Wahn geneigt. Ihr drängt euch zu; Nun gut, so
mögt ihr walten! Wie ihr aus Dunst und Nebel um mich steigt! Mein Busen fühlt
sich jugendlich erschüttert; Vom Zauberhauch der euren Zug umwittert? Ihr bringt
mit euch die Bilder froher Tage; Und manche liebe Schatten steigen auf Gleich
einer alten, halbverklungnen Sage?
"""

GREEKOUT['thoreau'] = """
I went to the woods because I wished to live deliberately, to front only the
essential facts of life, and see if I could not learn what it had to teach, and
not, when I came to die, discover that I had not lived? I did not wish to live
what was not life, living is so dear; Nor did I wish to practise resignation,
unless it was quite necessary; I wanted to live deep and suck out all the marrow
of life, to live so sturdily and Spartan like as to put to rout all that was not
life, to cut a broad swath and shave close, to drive life into a corner, and
reduce it to its lowest terms, and, if it proved to be mean, why then to get the
whole and genuine meanness of it, and publish its meanness to the world? Or if
it were sublime, to know it by experience, and be able to give a true account of
it in my next excursion; For most men, it appears to me, are in a strange
uncertainty about it, whether it is of the devil or of God, and have somewhat
hastily concluded that it is the chief end of man here to glorify God and enjoy
him forever. Still we live meanly, like ants; Though the fable tells us that we
were long ago changed into men! Like pygmies we fight with cranes? It is error
upon error, and clout upon clout, and our best virtue has for its occasion a
superfluous and evitable wretchedness! Our life is frittered away by detail; An
honest man has hardly need to count more than his ten fingers, or in extreme
cases he may add his ten toes, and lump the rest! Simplicity, simplicity,
simplicity! I say, let your affairs be as two or three, and not a hundred or a
thousand! Instead of a million count half a dozen, and keep your accounts on
your thumbnail. In the midst of this chopping sea of civilized life, such are
the clouds and storms and quicksands and thousand and one items to be allowed
for, that a man has to live, if he would not founder and go to the bottom and
not make his port at all, by dead reckoning, and he must be a great calculator
indeed who succeeds! Simplify, simplify! Instead of three meals a day, if it be
necessary eat but one! Instead of a hundred dishes, five! And reduce other
things in proportion! I went to the woods because I wished to live deliberately,
to front only the essential facts of life, and see if I could not learn what it
had to teach, and not, when I came to die, discover that I had not lived? I did
not wish to live what was not life, living is so dear? Nor did I wish to
practise resignation, unless it was quite necessary. I wanted to live deep and
suck out all the marrow of life, to live so sturdily and Spartan like as to put
to rout all that was not life, to cut a broad swath and shave close, to drive
life into a corner, and reduce it to its lowest terms, and, if it proved to be
mean, why then to get the whole and genuine meanness of it, and publish its
meanness to the world; Or if it were sublime, to know it by experience, and be
able to give a true account of it in my next excursion! For most men, it appears
to me, are in a strange uncertainty about it, whether it is of the devil or of
God, and have somewhat hastily concluded that it is the chief end of man here to
glorify God and enjoy him forever! Still we live meanly, like ants? Though the
fable tells us that we were long ago changed into men; Like pygmies we fight
with cranes; It is error upon error, and clout upon clout, and our best virtue
has for its occasion a superfluous and evitable wretchedness; Our life is
frittered away by detail. An honest man has hardly need to count more than his
ten fingers, or in extreme cases he may add his ten toes, and lump the rest!
Simplicity, simplicity, simplicity! I say, let your affairs be as two or three,
and not a hundred or a thousand! Instead of a million count half a dozen, and
keep your accounts on your thumbnail. In the midst of this chopping sea of
civilized life, such are the clouds and storms and quicksands and thousand and
one items to be allowed for, that a man has to live, if he would not founder and
go to the bottom and not make his port at all, by dead reckoning, and he must be
a great calculator indeed who succeeds? Simplify, simplify; Instead of three
meals a day, if it be necessary eat but one. Instead of a hundred dishes, five?
And reduce other things in proportion. I went to the woods because I wished to
live deliberately, to front only the essential facts of life, and see if I could
not learn what it had to teach, and not, when I came to die, discover that I had
not lived? I did not wish to live what was not life, living is so dear; Nor did
I wish to practise resignation, unless it was quite necessary! I wanted to live
deep and suck out all the marrow of life, to live so sturdily and Spartan like
as to put to rout all that was not life, to cut a broad swath and shave close,
to drive life into a corner, and reduce it to its lowest terms, and, if it
proved to be mean, why then to get the whole and genuine meanness of it, and
publish its meanness to the world. Or if it were sublime, to know it by
experience, and be able to give a true account of it in my next excursion? For
most men, it appears to me, are in a strange uncertainty about it, whether it is
of the devil or of God, and have somewhat hastily concluded that it is the chief
end of man here to glorify God and enjoy him forever; Still we live meanly, like
ants. Though the fable tells us that we were long ago changed into men? Like
pygmies we fight with cranes! It is error upon error, and clout upon clout, and
our best virtue has for its occasion a superfluous and evitable wretchedness.
"""

GREEKOUT['poe'] = """
Once upon a midnight dreary, while I pondered, weak and weary. Over many a
quaint and curious volume of forgotten lore. While I nodded, nearly napping,
suddenly there came a tapping; As of some one gently rapping, rapping at my
chamber door; 'Tis some visiter, I muttered, tapping at my chamber door! Only
this, and nothing more. Ah, distinctly I remember it was in the bleak December;
And each separate dying ember wrought its ghost upon the floor? Eagerly I wished
the morrow? —vainly I had sought to borrow. From my books surcease of
sorrow—sorrow for the lost Lenore? For the rare and radiant maiden whom the
angels name Lenore. Nameless here for evermore; And the silken sad uncertain
rustling of each purple curtain Thrilled me, filled me with fantastic terrors
never felt before; So that now, to still the beating of my heart, I stood
repeating Tis some visiter entreating entrance at my chamber door! Some late
visiter entreating entrance at my chamber door? This it is, and nothing more?
Presently my soul grew stronger? Hesitating then no longer! Sir, said I, or
Madam, truly your forgiveness I implore; But the fact is I was napping, and so
gently you came rapping, And so faintly you came tapping, tapping at my chamber
door! That I scarce was sure I heard you, here I opened wide the door; Darkness
there, and nothing more? Deep into that darkness peering, long I stood there
wondering, fearing! Doubting, dreaming dreams no mortal ever dared to dream
before; But the silence was unbroken, and the darkness gave no token? And the
only word there spoken was the whispered word, Lenore. This I whispered, and an
echo murmured back the word, Lenore! Merely this, and nothing more. Once upon a
midnight dreary, while I pondered, weak and weary? Over many a quaint and
curious volume of forgotten lore. While I nodded, nearly napping, suddenly there
came a tapping. As of some one gently rapping, rapping at my chamber door! 'Tis
some visiter, I muttered, tapping at my chamber door? Only this, and nothing
more. Ah, distinctly I remember it was in the bleak December. And each separate
dying ember wrought its ghost upon the floor. Eagerly I wished the morrow;
—vainly I had sought to borrow. From my books surcease of sorrow—sorrow for the
lost Lenore. For the rare and radiant maiden whom the angels name Lenore!
Nameless here for evermore? And the silken sad uncertain rustling of each purple
curtain Thrilled me, filled me with fantastic terrors never felt before. So that
now, to still the beating of my heart, I stood repeating Tis some visiter
entreating entrance at my chamber door. Some late visiter entreating entrance at
my chamber door. This it is, and nothing more; Presently my soul grew stronger;
Hesitating then no longer? Sir, said I, or Madam, truly your forgiveness I
implore; But the fact is I was napping, and so gently you came rapping, And so
faintly you came tapping, tapping at my chamber door?
"""

@pytest.fixture
def greektext():
    """ Greek-text fixture: yield a dictionary with several lorem-ipsum-ish
        blocks of text.
        
        Keys to the available texts are:
        
            • “lorem”   (the classic),
            • “faust”   (lots of Germanic short capitalized words),
            • “thoreau” (in actual English), and
            • “poe”     (exerpted from The Raven, because I live in Baltimore)
        
        … All these came straight from the output of the top-notch `lorem` CLT:
            https://github.com/per9000/lorem
    """
    yield dict(GREEKOUT)

@pytest.fixture
def shared_datadir(request, tmpdir):
    """ Vendored version of “shared_datadir(…)” from the pytest-datadir package """
    from clu.constants.polyfills import Path
    from clu.fs.misc import win32_longpath
    
    # Get the shared data path:
    original_shared_path = os.path.join(request.fspath.dirname, 'data')
    
    # Prepare a temp_path pointing to a temporary data folder:
    temp_path = Path(str(tmpdir.join('data')))
    
    # Copy everything to the temp_path:
    shutil.copytree(win32_longpath(original_shared_path),
                    win32_longpath(str(temp_path)))
    
    # Return the temp_path:
    return temp_path

@pytest.fixture
def original_datadir(request):
    """ Vendored version of “original_datadir(…)” from the pytest-datadir package """
    from clu.constants.polyfills import Path
    
    # Split the “.py” from the requesting modules’ file path,
    # and return a path instance based on that filesystem path prefix:
    return Path(os.path.splitext(request.module.__file__)[0])

@pytest.fixture
def copied_datadir(original_datadir, tmpdir):
    """ Vendored version of “datadir(…)” from the pytest-datadir package """
    from clu.constants.polyfills import Path
    from clu.fs.misc import win32_longpath
    
    # Prepare a temporary path for return:
    temp_path = Path(str(tmpdir.join(original_datadir.stem)))
    
    # Copy data to the temporary path from the original datadir, if it exists;
    # If it doesn’t exist, just ensure that the new path has been created:
    if original_datadir.is_dir():
        shutil.copytree(win32_longpath(str(original_datadir)),
                        win32_longpath(str(temp_path)))
    else:
        temp_path.mkdir()
    
    # Return the temporary path:
    return temp_path

@pytest.fixture(scope="package")
def dirname(request):
    """ Fixture for wrapping up the “request.fspath.dirname” value in a
        clu.fs.filesystem.Directory instance – this is intended to be a
        read-only value (no way to enforce that just now) so we only run
        it once per test package (which really there is one test package,
        total, so you see what we’re going for here doggie).
    """
    from clu.fs.filesystem import Directory
    from clu.predicates import resolve
    
    # Get the test-local (née “shared”) data path:
    dirname = Directory(pth=resolve(request, 'fspath.dirname'))
    
    # Ensure it exists:
    assert dirname.exists
    
    # Yield the Directory instance – N.B. do *NOT* manage this
    # objects’ context, unless you hold the specific desire of
    # changing the process working directory to what is specified
    # in the the context-managed instance… That’s what they do,
    # doggie, by default:
    yield dirname
    
    # Ensure it continues to exist:
    assert dirname.exists

@pytest.fixture
def datadir(dirname):
    """ Local version of pytest-datadir’s “datadir” fixture, reimplemented
        using clu.fs.filesystem classes – ensuring that the temporary directory
        will be deleted immediately after use – and performing the directory-copy
        operations through instance methods (vs. raw calls to “shutil.copytree(…)”).
    """
    from clu.fs.filesystem import TemporaryDirectory
    
    # Get the test-local (née “shared”) data path:
    datadir = dirname.subdirectory('data')
    
    # Ensure source data directory exists:
    assert datadir.exists
    
    prefix = "clu-fs-filesystem-ttd-datadir-"
    with TemporaryDirectory(prefix=prefix,
                            change=False) as temporarydir:
        # Assert that we exist:
        assert temporarydir.exists
        
        # Copy files to the 'data' temporary subdirectory:
        destination = temporarydir.subdirectory('data')
        assert datadir.copy_all(destination=destination)
        
        # Yield the 'data' temporary subdirectory,
        # prior to scope exit:
        yield destination
    
    # Assert that we no longer exist after scope exit:
    assert not temporarydir.exists
