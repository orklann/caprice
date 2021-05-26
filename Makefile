all:
	@grep -Ee '^[a-z].*:' Makefile | cut -d: -f1 | grep -vF all

clean:
	rm -rf build/ dist/

release: clean
	make force_release

force_release: clean
	python setup.py sdist bdist_wheel
	twine upload dist/*