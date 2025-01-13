VENV := venv
PYTHON := $(VENV)/bin/python
HOST = $(shell ifconfig | grep "inet " | tail -1 | cut -d\  -f2)
TAG = v$(shell grep -E '__version__ = ".*"' pyrogram/__init__.py | cut -d\" -f2)

RM := rm -rf

.PHONY: venv clean-build clean-api clean api build tag dtag clean-docs docs

all: clean venv build
	echo Done

venv:
	$(RM) $(VENV)
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -U pip wheel setuptools
	$(PYTHON) -m pip install -U -e .[docs]
	@echo "Created venv with $$($(PYTHON) --version)"

clean-build:
	$(RM) *.egg-info build dist

clean-docs:
	$(RM) docs/build
	$(RM) docs/build docs/source/api/bound-methods docs/source/api/methods docs/source/api/types docs/source/api/enums docs/source/telegram

clean-api:
	$(RM) pyrogram/errors/exceptions pyrogram/raw/all.py pyrogram/raw/base pyrogram/raw/functions pyrogram/raw/types

clean:
	make clean-build
	make clean-api

api:
	cd compiler/api && ../../$(PYTHON) compiler.py
	cd compiler/errors && ../../$(PYTHON) compiler.py

docs-live:
	make clean-docs
	make api
	cd compiler/docs && ../../$(PYTHON) compiler.py
	$(VENV)/bin/sphinx-autobuild \
		--watch pyrogram --watch docs/resources \
		-b html "docs/source" "docs/build/html" -j auto

docs:
	make clean-docs
	cd compiler/docs && ../../$(PYTHON) compiler.py
	$(VENV)/bin/sphinx-build \
		-b html "docs/source" "docs/build/html" -j auto

build: clean api docs
	echo Build

tag:
	git tag $(TAG)
	git push origin $(TAG)

dtag:
	git tag -d $(TAG)
	git push origin -d $(TAG)
