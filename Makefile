PYTHON ?= python3
.PHONY: build test
build:
	$(PYTHON) -m compileall -q src
test:
	$(PYTHON) -m unittest discover -s tests -v
