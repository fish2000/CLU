
PROJECT_NAME = clu

clean: clean-pyc

distclean: clean-pyc clean-build-artifacts

rebuild: distclean cython

dist: twine-upload

upload: bump dist

bigupload: bigbump dist

clean-pyc:
	find . -name \*.pyc -print -delete

clean-cython:
	find clu/ -name \*.so -print -delete

clean-build-artifacts:
	rm -rf build dist python_$(PROJECT_NAME).egg-info

cython:
	python setup.py build_ext --inplace

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

twine-upload: cython sdist wheel
	twine upload -s dist/*

bump:
	bumpversion --verbose patch

bigbump:
	bumpversion --verbose minor

check:
	check-manifest -v
	python setup.py check -m -s
	travis lint .travis.yml

check-all: check clean-build-artifacts
	pytest

.PHONY: clean-pyc clean-cython clean-build-artifacts
.PHONY: clean distclean rebuild dist upload bigupload
.PHONY: cython sdist wheel twine-upload bump bigbump
.PHONY: check check-all

