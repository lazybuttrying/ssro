PYTHON ?= python
PIP ?= pip

.PHONY: install run test clean

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m pytest

clean:
	rm -rf .pytest_cache
	rm -rf outputs/*.json outputs/*.csv outputs/*.txt
