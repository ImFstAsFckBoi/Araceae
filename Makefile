ifeq ($(OS), Windows_NT)
	PY = python
else
	PY = python3
endif

PIP = ${PY} -m pip


CLEAN_LIST = *.so build/ dist/ *.egg-info/ .mypy_cache/ .pytest_cache/

dev:
	${PIP} install -e '.[dev]'

install:
	${PIP} install .

venv:
	${PY} -m venv .venv 

test:
	python3 -m pytest araceae/ -W ignore::DeprecationWarning

clean:
	rm -rf ${CLEAN_LIST}
	find araceae -wholename "*__pycache__*" -delete

full-clean: clean
	rm -rf .venv/

build:
	${PY} -m build -w .
