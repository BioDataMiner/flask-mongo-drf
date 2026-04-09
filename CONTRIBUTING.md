# Contributing to flask-mongo-rest

Thank you for your interest in contributing to flask-mongo-rest! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct.

## Getting Started

### Prerequisites

- Python 3.7+
- MongoDB (local or remote instance for testing)
- Git

### Development Setup

1. Fork the repository on GitHub.

2. Clone your fork locally:
   ```bash
   git clone https://github.com/BioDataMiner/flask-mongo-rest.git
   cd flask-mongo-rest
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=flask_mongo_rest --cov-report=html

# Run specific test file
pytest tests/test_models.py -v
```

### Code Style

We use `black` for code formatting and `flake8` for linting.

```bash
# Format code with black
black flask_mongo_rest/ tests/

# Check code style with flake8
flake8 flask_mongo_rest/ tests/
```

### Writing Tests

- Write tests for all new features and bug fixes.
- Place tests in the `tests/` directory.
- Use descriptive test names that explain what is being tested.
- Aim for at least 80% code coverage.

Example test structure:

```python
import pytest
from flask_mongo_rest import MongoBaseModel

class TestMongoBaseModel:
    def test_insert_one(self, mock_collection):
        model = MongoBaseModel(mock_collection)
        result = model.insert_one({"name": "test"})
        assert result.inserted_id is not None
```

### Documentation

- Update documentation for any new features or API changes.
- Use clear, concise language.
- Include code examples where appropriate.
- Build docs locally to verify:
  ```bash
  cd docs
  make html
  ```

## Submitting Changes

### Commit Messages

Write clear, descriptive commit messages:

```
[FEATURE] Add support for custom serializers

- Implement CustomSerializer base class
- Add validation framework
- Update documentation with examples

Fixes #123
```

### Pull Request Process

1. Update the CHANGELOG.md with notes on your changes.
2. Ensure all tests pass: `pytest tests/ -v`
3. Ensure code is formatted: `black flask_mongo_rest/ tests/`
4. Ensure no linting issues: `flake8 flask_mongo_rest/ tests/`
5. Push your branch to GitHub.
6. Create a Pull Request with a clear description of your changes.
7. Link any related issues.

### PR Guidelines

- Keep PRs focused on a single feature or bug fix.
- Provide a clear description of what changes and why.
- Include any relevant issue numbers.
- Ensure CI/CD checks pass.
- Request review from maintainers.

## Reporting Bugs

When reporting bugs, please include:

- Python version
- MongoDB version
- flask-mongo-rest version
- Minimal code example to reproduce the issue
- Expected vs. actual behavior
- Error messages and stack traces

## Suggesting Enhancements

We welcome feature suggestions! When proposing new features:

- Explain the use case and motivation.
- Provide examples of how it would be used.
- Consider backward compatibility.
- Discuss potential implementation approaches.

## Release Process

Maintainers will handle releases. The process includes:

1. Update version in `setup.py` and `pyproject.toml`.
2. Update CHANGELOG.md.
3. Create a git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions automatically builds and publishes to PyPI.

## Questions?

Feel free to open an issue or reach out to the maintainers.

---

Thank you for contributing to flask-mongo-rest! 🎉
