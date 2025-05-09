The deal with CLU is, it is a bunch of stuff. Like, a junk drawer… but a junk drawer
full of building sets: Legos, Robotix, Capsela – and also magic interfaces that let
you plug Legos into Capselas and all that. It’s a la carte: you can use one part of
CLU (say the inline testing stuff) and ignore the rest. Or just the exporter, or just
the predicates collection. Naturally, these things taste great and also taste great
together, too, 

CLU is, basically, a bunch of sub-top-level packages. “clu.config” contains things to
help with configuration, like config-file loading and saving, and datastructures like
our famous namespaced keymaps. “clu.exporting” has the @export decorator, a utility
to easily label module members for export by adding them to a modules’ __all__ and
__dir__ members, plus other stuff like real-name determination. Which, speaking of
which, “clu.naming” has additional easy functions for dealing with the names of your
things, and “clu.repr” has stuff for easily specifying an objects’ string representation.

You’ll like “clu.abstract” if you like building class towers – we have ABCs for all
types of things. If you like dicts, check out the aforementioned “clu.config.keymaps”
and “clu.dicts” modules – you’ll find things to build dictionary types, represent
them, and deal with them later. “clu.dispatch” will help you manage subprocess easily,
“clu.version” is better then ‘semver’ (I promise), “clu.testing” is great for inlining
some quick unit tests, and “clu.scripts” and “clu.repl” are what you want for whatever
your REPL environment may be… `bpython`, `ipython`, AND MORE!!! So have a
look around.