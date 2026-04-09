# PyPI Release Guide for flask-mongo-rest

This guide provides step-by-step instructions for publishing flask-mongo-rest to PyPI.

## Prerequisites

Before releasing, ensure you have:

1. **PyPI Account**: Create an account at [pypi.org](https://pypi.org)
2. **TestPyPI Account**: Create an account at [test.pypi.org](https://test.pypi.org) (optional but recommended)
3. **Build Tools**: Install required tools:
   ```bash
   pip install build twine
   ```
4. **PyPI API Token**: Generate a token from your PyPI account settings

## Step-by-Step Release Process

### 1. Prepare Your Release

Update version numbers in:
- `setup.py`: Change `version="1.0.0"` to your new version
- `pyproject.toml`: Update `version = "1.0.0"`
- `docs/conf.py`: Update `release = '1.0.0'` and `version = '1.0'`

Update `CHANGELOG.md` with release notes:
```markdown
## [1.1.0] - 2026-04-15

### Added
- New feature description

### Fixed
- Bug fix description
```

### 2. Run Tests Locally

Ensure all tests pass before release:
```bash
pytest tests/ -v --cov=flask_mongo_rest
```

### 3. Build Distribution Packages

Create distribution files:
```bash
python -m build
```

This generates:
- `dist/flask-mongo-rest-1.0.0.tar.gz` (source distribution)
- `dist/flask_mongo_rest-1.0.0-py3-none-any.whl` (wheel)

### 4. Test on TestPyPI (Recommended)

First, test your package on TestPyPI:

```bash
twine upload --repository testpypi dist/*
```

Then test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ flask-mongo-rest
```

### 5. Create GitHub Release

1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   git push origin main
   ```

2. Create a git tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. Create GitHub Release:
   - Go to [Releases](https://github.com/BioDataMiner/flask-mongo-rest/releases)
   - Click "Draft a new release"
   - Select the tag you just created
   - Add release notes from CHANGELOG.md
   - Click "Publish release"

### 6. Publish to PyPI

#### Option A: Using Twine (Manual)

```bash
twine upload dist/*
```

When prompted, enter your PyPI username and password (or API token).

#### Option B: Using GitHub Actions (Automated)

The repository includes automated GitHub Actions workflows. When you create a release:

1. The `publish.yml` workflow automatically triggers
2. It builds the distribution packages
3. It publishes to PyPI using your `PYPI_API_TOKEN` secret

**Setup GitHub Secrets:**
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Your PyPI API token (from pypi.org account settings)

### 7. Verify Publication

After publishing, verify your package:

```bash
pip install flask-mongo-rest
python -c "import flask_mongo_rest; print(flask_mongo_rest.__version__)"
```

Check PyPI page: https://pypi.org/project/flask-mongo-rest/

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (1.X.0): New features, backward compatible
- **PATCH** version (1.0.X): Bug fixes, backward compatible

Examples:
- `1.0.0` → `1.1.0`: New feature
- `1.0.0` → `1.0.1`: Bug fix
- `1.0.0` → `2.0.0`: Breaking changes

## Troubleshooting

### "Invalid distribution" error

Ensure your package structure is correct:
```
flask_mongo_rest/
├── __init__.py
├── mongo_models.py
├── mongo_viewsets.py
└── ...
```

### "Filename already exists" error

You cannot re-upload the same version. Increment the version number and rebuild.

### "Authentication failed" error

Check your PyPI credentials:
```bash
twine upload --repository pypi dist/* --username __token__ --password your_token_here
```

## Post-Release

After successful release:

1. Update documentation on ReadTheDocs
2. Announce the release on GitHub Discussions
3. Update social media/community channels
4. Monitor for issues and bug reports

## Continuous Integration

The repository includes GitHub Actions workflows for:

- **Testing**: Runs on every push/PR (tests.yml)
- **Publishing**: Automatically publishes on GitHub Release (publish.yml)

## Resources

- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)

---

For questions or issues, please open an issue on GitHub.
