# GitHub Repository Setup and PyPI Publishing Guide

This guide documents the exact steps taken to create the GitHub repository and how to set up PyPI publishing so users can install with `pipx install pydeptree`.

## Part 1: Creating GitHub Repository from Existing Code

Here are the exact Git commands used to initialize and push this repository:

### 1. Initialize Git Repository

```bash
# Navigate to your project directory
cd pydeptree-package

# Initialize a new Git repository
git init
```

### 2. Add Files and Create Initial Commit

```bash
# Add all files to staging
git add .

# Create the initial commit
git commit -m "Initial commit: PyDepTree - Python dependency analyzer

- Core functionality with AST-based import parsing
- Rich terminal output with colored dependency trees
- Configurable depth traversal
- Circular dependency detection
- Professional package structure for PyPI distribution
- Comprehensive documentation and tests
- GitHub Actions for CI/CD"
```

### 3. Create GitHub Repository and Push

```bash
# Add the remote repository
# Note: The repository must exist on GitHub first
git remote add origin https://github.com/tfaucheux/pydeptree.git

# Rename default branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### Alternative: Using GitHub CLI

If you have GitHub CLI installed, you can create the repo and push in one command:

```bash
# Create repo and push (if gh CLI is installed)
gh repo create tfaucheux/pydeptree --public --source . --push
```

### 4. Subsequent Changes

```bash
# For any updates
git add <files>
git commit -m "descriptive commit message"
git push origin main
```

## Part 2: PyPI Setup for `pipx install pydeptree`

To enable users to install your package with `pipx install pydeptree`, you need to publish it to PyPI. Here's how:

### Prerequisites

1. **Create a PyPI Account**
   - Go to https://pypi.org/account/register/
   - Verify your email address
   - Enable 2FA (recommended)

2. **Create a Test PyPI Account** (Optional but recommended)
   - Go to https://test.pypi.org/account/register/
   - Use this for testing before real releases

### Step 1: Generate PyPI API Token

1. Log into PyPI: https://pypi.org/manage/account/
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Give it a name (e.g., "pydeptree-github-actions")
5. Scope: "Entire account" (or project-specific after first upload)
6. Copy the token (starts with `pypi-`)
7. Save it securely - you won't see it again!

### Step 2: Add Token to GitHub Secrets

1. Go to your repo: https://github.com/tfaucheux/pydeptree
2. Click Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

### Step 3: Test Build Locally

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the package
twine check dist/*

# Optional: Test on TestPyPI first
twine upload --repository testpypi dist/*
```

### Step 4: Create a Release

The GitHub Actions workflow is already configured to automatically publish to PyPI when you create a tagged release.

```bash
# Update version in pyproject.toml and pydeptree/__init__.py first!

# Commit version bump
git add pyproject.toml pydeptree/__init__.py
git commit -m "Bump version to 0.1.0"
git push

# Create and push a tag
git tag v0.1.0
git push origin v0.1.0
```

The GitHub Action will automatically:
1. Build the package
2. Run tests
3. Upload to PyPI

### Step 5: Verify Installation

After about 1-2 minutes, users can install:

```bash
# With pipx (recommended)
pipx install pydeptree

# With pip
pip install pydeptree

# Verify it works
pydeptree --help
```

## Quick Checklist for PyPI Publishing

- [ ] PyPI account created and verified
- [ ] API token generated
- [ ] Token added to GitHub secrets as `PYPI_API_TOKEN`
- [ ] Version updated in `pyproject.toml` and `__init__.py`
- [ ] Changes committed and pushed
- [ ] Tag created and pushed (`git tag v0.1.0 && git push origin v0.1.0`)
- [ ] GitHub Action completed successfully
- [ ] Package visible on https://pypi.org/project/pydeptree/
- [ ] `pipx install pydeptree` works

## Troubleshooting

### "Package already exists"
- You can't reupload the same version
- Bump the version number and try again

### "Invalid API token"
- Make sure you copied the entire token
- Token should start with `pypi-`
- Check it's in GitHub secrets correctly

### GitHub Action Failing
- Check the Actions tab for error logs
- Ensure all tests pass locally first
- Verify the package builds with `python -m build`

### Package Not Appearing on PyPI
- Wait 1-2 minutes for processing
- Check https://pypi.org/project/pydeptree/
- Try hard refresh (Ctrl+F5)

## Managing Releases

For future releases:

1. Update version in `pyproject.toml` and `__init__.py`
2. Update `CHANGELOG.md`
3. Commit changes
4. Create tag: `git tag v0.2.0`
5. Push: `git push origin v0.2.0`
6. GitHub Actions handles the rest!

## Additional Resources

- [Python Packaging Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [pipx Documentation](https://pypa.github.io/pipx/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Help](https://pypi.org/help/)