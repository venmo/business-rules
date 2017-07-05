.PHONY: clean test coverage

clean:
	-find . -type f -name "*.pyc" -delete

deps:
	pip install -r requirements-dev.txt

test:
	py.test $(pytest_args)

coverage:
	py.test --cov-report term-missing --cov=./business_rules $(pytest_args)
