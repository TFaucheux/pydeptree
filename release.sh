#!/bin/bash

# PyDepTree Release Script
# Usage: ./release.sh <version> [--dry-run]
# Example: ./release.sh 0.4.0

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if version argument is provided
if [ $# -eq 0 ]; then
    log_error "Version argument is required"
    echo "Usage: ./release.sh <version> [--dry-run]"
    echo "Example: ./release.sh 0.4.0"
    exit 1
fi

NEW_VERSION="$1"
DRY_RUN=false

# Check for dry-run flag
if [ "$2" = "--dry-run" ] || [ "$2" = "-n" ]; then
    DRY_RUN=true
    log_warning "DRY RUN MODE - No changes will be made"
fi

# Validate version format (semantic versioning)
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "Invalid version format. Use semantic versioning (e.g., 1.2.3)"
    exit 1
fi

log_info "Starting release process for version $NEW_VERSION"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not in a git repository"
    exit 1
fi

# Check if working directory is clean
if ! git diff-index --quiet HEAD --; then
    log_error "Working directory is not clean. Please commit or stash changes first."
    git status --porcelain
    exit 1
fi

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    log_warning "You are on branch '$CURRENT_BRANCH', not 'main'. Continue? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        log_info "Release cancelled"
        exit 0
    fi
fi

# Get current version from __init__.py
CURRENT_VERSION=$(grep -o '__version__ = "[^"]*"' pydeptree/__init__.py | cut -d'"' -f2)
log_info "Current version: $CURRENT_VERSION"

# Check if tag already exists
if git tag --list | grep -q "^v$NEW_VERSION$"; then
    log_error "Tag v$NEW_VERSION already exists"
    exit 1
fi

# Update version in files
log_info "Updating version in files..."

if [ "$DRY_RUN" = false ]; then
    # Update pydeptree/__init__.py
    sed -i.bak "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" pydeptree/__init__.py
    rm pydeptree/__init__.py.bak
    
    # Update setup.py
    sed -i.bak "s/version=\"$CURRENT_VERSION\"/version=\"$NEW_VERSION\"/" setup.py
    rm setup.py.bak
    
    # Update pyproject.toml
    sed -i.bak "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
    rm pyproject.toml.bak
    
    # Update CHANGELOG.md
    TODAY=$(date '+%Y-%m-%d')
    sed -i.bak "s/## \[Unreleased\]/## [Unreleased]\n\n## [$NEW_VERSION] - $TODAY/" CHANGELOG.md
    rm CHANGELOG.md.bak
    
    log_success "Version files updated"
else
    log_info "[DRY RUN] Would update version in:"
    log_info "  - pydeptree/__init__.py"
    log_info "  - setup.py"
    log_info "  - pyproject.toml"
    log_info "  - CHANGELOG.md"
fi

# Show what files would be changed
log_info "Files that will be committed:"
if [ "$DRY_RUN" = false ]; then
    git add pydeptree/__init__.py setup.py pyproject.toml CHANGELOG.md
    git diff --cached --name-only
else
    echo "  - pydeptree/__init__.py"
    echo "  - setup.py"
    echo "  - pyproject.toml"
    echo "  - CHANGELOG.md"
fi

# Commit changes
log_info "Committing version changes..."
if [ "$DRY_RUN" = false ]; then
    git commit -m "Release v$NEW_VERSION

Bump version to $NEW_VERSION and update changelog"
    log_success "Changes committed"
else
    log_info "[DRY RUN] Would commit with message: 'Release v$NEW_VERSION'"
fi

# Create and push tag
log_info "Creating and pushing git tag..."
if [ "$DRY_RUN" = false ]; then
    git tag "v$NEW_VERSION"
    git push origin "$CURRENT_BRANCH"
    git push origin "v$NEW_VERSION"
    log_success "Git tag v$NEW_VERSION created and pushed"
else
    log_info "[DRY RUN] Would create and push tag: v$NEW_VERSION"
fi

# Activate virtual environment
log_info "Activating virtual environment..."
if [ -f ".venv/bin/activate" ]; then
    if [ "$DRY_RUN" = false ]; then
        source .venv/bin/activate
        log_success "Virtual environment activated"
    else
        log_info "[DRY RUN] Would activate virtual environment"
    fi
else
    log_warning "Virtual environment not found at .venv/bin/activate"
    log_info "Make sure you have the required dependencies installed"
fi

# Clean and build with uv
log_info "Building distribution packages with uv..."
if [ "$DRY_RUN" = false ]; then
    rm -f dist/*
    uv build
    log_success "Distribution packages built"
    ls -la dist/
else
    log_info "[DRY RUN] Would clean dist/ and run 'uv build'"
fi

# Publish to TestPyPI and PyPI
log_info "Publishing to TestPyPI..."
if [ "$DRY_RUN" = false ]; then
    if [ -f "./publish.sh" ]; then
        ./publish.sh test
        log_success "Published to TestPyPI"
    else
        log_error "publish.sh script not found"
        exit 1
    fi
else
    log_info "[DRY RUN] Would run './publish.sh test'"
fi

log_info "Publishing to PyPI..."
if [ "$DRY_RUN" = false ]; then
    ./publish.sh prod
    log_success "Published to PyPI"
else
    log_info "[DRY RUN] Would run './publish.sh prod'"
fi

# Final success message
log_success "🎉 Release v$NEW_VERSION completed successfully!"

if [ "$DRY_RUN" = false ]; then
    echo ""
    log_info "Release Summary:"
    log_info "  Version: $CURRENT_VERSION → $NEW_VERSION"
    log_info "  Git tag: v$NEW_VERSION"
    log_info "  TestPyPI: https://test.pypi.org/project/pydeptree/$NEW_VERSION/"
    log_info "  PyPI: https://pypi.org/project/pydeptree/$NEW_VERSION/"
    echo ""
    log_info "Installation commands:"
    echo "  pip install pydeptree==$NEW_VERSION"
    echo "  pipx install pydeptree==$NEW_VERSION"
else
    echo ""
    log_info "This was a dry run. To execute the release, run:"
    echo "  ./release.sh $NEW_VERSION"
fi