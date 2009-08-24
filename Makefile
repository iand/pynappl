PYTHON = python

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  all          clean directories, compile and  test  all source files"
	@echo "  compile      compile all source files"
	@echo "  test         run all tests"
	@echo "  clean        clean all compiled files"

all: clean compile test 

compile:
	$(PYTHON) -m compileall .

test:
	$(PYTHON) tests/all_tests.py

clean:
	$(PYTHON) clean.py

dist:
	$(PYTHON) setup.py
