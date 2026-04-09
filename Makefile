.PHONY: help install install-dev test test-cov lint format docs clean build publish

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black"
	@echo "  make docs          - Build documentation"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make build         - Build distribution packages"
	@echo "  make publish       - Publish to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=flask_mongo_drf --cov-report=html --cov-report=term-missing

lint:
	flake8 flask_mongo_drf tests
	black --check flask_mongo_drf tests

format:
	black flask_mongo_drf tests

docs:
	cd docs && make html

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf htmlcov/ .coverage
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	twine upload dist/*
