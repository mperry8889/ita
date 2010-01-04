compile: _compile clean
_compile:
	python -c "import compileall; compileall.compile_dir('./src')"

clean:
	find . -name \*.pyc -exec rm {} \;


.PHONY: compile _compile clean
