PYTHON ?= python3
CONFIG ?= config.ini
export PYTHONPATH := $(CURDIR)/src

.PHONY: run test lint clean

run:
	$(PYTHON) -m depvis.cli --config $(CONFIG)

test:
	$(PYTHON) -m pytest -q tests

lint:
	$(PYTHON) -m pycodestyle --max-line-length=79 src tests
	$(PYTHON) -m radon cc -n C src

clean:
	rm -rf ep5_output .pytest_cache
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
