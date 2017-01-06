.PHONY: clean test

clean:
	-find . -type f -name "*.pyc" -delete

test:
	py.test
