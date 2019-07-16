
PROJECT_NAME = clu

clean: clean-cython clean-build-artifacts clean-pyc

distclean: clean-test-artifacts clean-build-artifacts

rebuild: clean-build-artifacts cython

dist: twine-upload

upload: bump dist
	git push

bigupload: bigbump dist
	git push

clean-pyc:
	find . -name \*.pyc -print -delete

clean-cython:
	find $(PROJECT_NAME)/ -name \*.so -print -delete

clean-build-artifacts: clean-cython
	rm -rf build dist python_$(PROJECT_NAME).egg-info

clean-pytest-artifacts:
	pushd $(TMPDIR) && rm -rf pytest-of-$(USER) && popd

clean-test-artifacts: clean-pyc clean-pytest-artifacts
	rm -rf ../.pytest_cache ../.hypothesis .pytest_cache .hypothesis .tox

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

check: clean-build-artifacts
	check-manifest -v
	python setup.py check -m -s
	travis lint .travis.yml

test: check
	pytest

test-all: check
	tox

.PHONY: clean distclean rebuild
.PHONY: dist upload bigupload
.PHONY: clean-pyc clean-cython clean-build-artifacts clean-test-artifacts

.PHONY: cython sdist wheel twine-upload bump bigbump

.PHONY: check test test-all

