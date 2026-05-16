PY ?= .venv/Scripts/python.exe
ifeq ($(OS),Windows_NT)
  ifeq ($(wildcard $(PY)),)
    PY := py -3.12
  endif
else
  PY := .venv/bin/python
endif

.PHONY: help install test test-parallel stability-check smoke regression lint format clean allure-report allure-serve

help:
	@echo "Targets: install test test-parallel stability-check smoke regression lint format clean allure-report allure-serve"

install:
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) -m pytest

test-parallel:
	$(PY) -m pytest -n auto --dist=loadscope

stability-check:
	@for i in 1 2 3; do $(PY) -m pytest -m regression || exit 1; done

smoke:
	$(PY) -m pytest -m smoke

regression:
	$(PY) -m pytest -m regression

lint:
	$(PY) -m ruff check src conftest.py scripts

format:
	$(PY) -m ruff format src conftest.py scripts

clean:
	$(PY) scripts/clean_cache.py

allure-report:
	allure generate allure-results -o allure-report --clean

allure-serve:
	allure serve allure-results
