N.B. regarding “clu/scripts/boilerplate.py”
===========================================

If the contents of this file appear skeletal and unfinished, it’s exactly because they are, intentionally. “boilerplate.py”
is the untouched, uncensored, and utterly unmitigated output of the invocation of the “clu-boilerplate” CLI endpoint, which
one of the unit tests in “test_boilerplate.py” imports and executes wholesale, as proof-positive of this code fragments’ 
ineffable shipability. Maybe it should be elsewhere? Maybe not – I’ll shed that bike when I cross in front of it while texting,
dogg, yeah.

**References:**

* [Lines in CLU’s “setup.py” file relevant to the “clu-boilerplate” endpoint](https://github.com/fish2000/CLU/blob/0230d601d6305d91de35955b7818191db69bb065/setup.py#L69-L70) – there are two related command endpoints and the one that doesn’t attempt to write to the pasteboard is the working one RN
* [The actual authoritative source of the endpoint code in question](https://github.com/fish2000/CLU/blob/0230d601d6305d91de35955b7818191db69bb065/clu/repl/cli/boilerplate.py#L6-L41) – probably one of the least intellectually thrilling Python modules under the aegis of my authorship, but it gets the job done; they’ll be time enough for
premature optimization when we’re old, my love
* [The aforementioned unit-test function](https://github.com/fish2000/CLU/blob/0230d601d6305d91de35955b7818191db69bb065/tests/test_boilerplate.py#L33-L55) – which I do fondly remember because it honestly feels fantastic to be able to `assert "a hundred times" in output`, like once in a while

**Further Inquiries:**

… are theoretically technically possible but utterly implausible in this Universe
