# Distribution Guide for PyDepTree

This guide covers how to build and distribute PyDepTree to PyPI.

## Prerequisites

1. Create accounts:
   - [PyPI account](https://pypi.org/account/register/)
   - [TestPyPI account](https://test.pypi.org/account/register/) (for testing)

2. Generate API tokens:
   - Go to PyPI → Account Settings → API tokens
   - Create a token with "Upload packages" scope
   - Save it securely (you'll need it for GitHub secrets)

## Local Development & Testing

### 1. Install Development Dependencies

```bash
cd pydeptree-package
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. Run Tests & Linting

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pydeptree

# Run linting
ruff check .
black .
mypy pydeptree
```

### 3. Test Installation Locally

```bash
# Build the package
python -m build

# Test install in a fresh environment
python -m venv test-env
source test-env/bin/activate
pip install dist/pydeptree-0.1.0-py3-none-any.whl
pydeptree --help
```

## Building for Distribution

### 1. Update Version

Edit version in:
- `pyproject.toml`
- `pydeptree/__init__.py`
- `CHANGELOG.md`

### 2. Build Distribution Packages

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build source distribution and wheel
python -m build
```

This creates:
- `dist/pydeptree-0.1.0.tar.gz` (source distribution)
- `dist/pydeptree-0.1.0-py3-none-any.whl` (wheel)

### 3. Verify Package Contents

```bash
# Check the wheel contents
unzip -l dist/pydeptree-0.1.0-py3-none-any.whl

# Check package metadata
twine check dist/*
```

## Publishing to PyPI

### Option 1: Manual Upload

#### Test on TestPyPI First

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ pydeptree
```

#### Upload to PyPI

```bash
# Upload to PyPI
twine upload dist/*

# Or with API token (recommended)
twine upload dist/* --username __token__ --password <your-token>
```

### Option 2: Automated with GitHub Actions

1. Add PyPI API token to GitHub secrets:
   - Go to your repo → Settings → Secrets → Actions
   - Add new secret: `PYPI_API_TOKEN`
   - Paste your PyPI API token

2. Create a new release:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

3. The GitHub Action will automatically:
   - Build the package
   - Run tests
   - Upload to PyPI

## Post-Release Verification

```bash
# Install from PyPI
pip install pydeptree

# Verify it works
pydeptree --help

# Check PyPI page
# https://pypi.org/project/pydeptree/
```

## Troubleshooting

### Common Issues

1. **"Invalid distribution file"**
   - Ensure `pyproject.toml` is valid
   - Run `python -m build` not `python setup.py`

2. **"Version already exists"**
   - Bump version number
   - Delete old releases from TestPyPI (if testing)

3. **Missing files in package**
   - Check `MANIFEST.in`
   - Verify with `python -m build --sdist`

### Package Structure Checklist

- [ ] `pyproject.toml` with all metadata
- [ ] `README.md` with badges and examples
- [ ] `LICENSE` file
- [ ] `CHANGELOG.md`
- [ ] `__init__.py` with `__version__`
- [ ] Entry points defined
- [ ] Tests passing
- [ ] Type hints (optional)
- [ ] `py.typed` marker (for type hints)

## Best Practices

1. **Versioning**: Follow [Semantic Versioning](https://semver.org/)
2. **Changelog**: Update for every release
3. **Testing**: Test on TestPyPI before PyPI
4. **Documentation**: Keep README current
5. **Dependencies**: Pin major versions only
6. **Python Support**: Test all declared versions

## Useful Commands Reference

```bash
# Development
pip install -e ".[dev]"         # Install in dev mode
pytest                          # Run tests
black .                         # Format code
ruff check .                    # Lint code
mypy pydeptree                  # Type check

# Building
python -m build                 # Build distributions
twine check dist/*              # Validate packages

# Publishing
twine upload --repository testpypi dist/*  # Test upload
twine upload dist/*                        # Production upload

# Installation
pip install pydeptree           # From PyPI
pipx install pydeptree          # Isolated install
pip install git+https://...     # From GitHub
```