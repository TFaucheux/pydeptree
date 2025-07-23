# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Notes

- The `sample_project/` directory contains **intentional linting errors and code quality issues** for demonstration purposes. These are NOT bugs.
- The project includes both a basic CLI (`pydeptree.cli`) and an enhanced CLI (`pydeptree.cli_enhanced`) with additional features.

## Common Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests (including enhanced CLI tests)
pytest

# Run tests with coverage
pytest --cov=pydeptree

# Run a specific test file
pytest tests/test_cli.py          # Basic CLI tests
pytest tests/test_cli_enhanced.py # Enhanced CLI tests

# Run a specific test
pytest tests/test_cli_enhanced.py::TestFileTypeDetection::test_detect_model_files
```

### Code Quality
```bash
# Format code with black
black .

# Check formatting without modifying
black --check .

# Run linting with ruff
ruff check pydeptree/    # Check only main package (clean code)
ruff check .             # Check everything (includes demo errors)

# Type checking
mypy pydeptree

# Note: sample_project/ contains intentional lint errors for demo purposes
```

### Building and Distribution
```bash
# Build distribution packages (uses uv)
./build.sh

# Publish to TestPyPI (requires .env with TWINE_USERNAME_TEST and TWINE_PASSWORD_TEST)
./publish.sh test

# Publish to PyPI (requires .env with TWINE_USERNAME_PROD and TWINE_PASSWORD_PROD)
./publish.sh prod
```

### Automated Release (Recommended)
```bash
# Complete automated release process (version bump, tag, build, publish)
./release.sh <version>                    # Full release
./release.sh <version> --dry-run          # Preview changes without executing

# Examples
./release.sh 1.0.0                        # Release version 1.0.0
./release.sh 0.4.5 --dry-run              # Preview release 0.4.5

# The release script automatically:
# 1. Updates version in __init__.py, setup.py, pyproject.toml, CHANGELOG.md
# 2. Commits changes with standardized message
# 3. Creates and pushes git tag
# 4. Builds distribution packages with uv
# 5. Publishes to both TestPyPI and PyPI
```

### Demo and Testing Enhanced Features
```bash
# Run the interactive demo
python demo_enhanced.py

# Test enhanced CLI on sample project
python -m pydeptree.cli_enhanced sample_project/main.py --depth 2

# Quick example with basic CLI
python -m pydeptree.cli sample_project/main.py --depth 2
```

## Architecture Overview

PyDepTree is a CLI tool for analyzing Python module dependencies. It uses AST parsing to extract imports and creates visual dependency trees.

### Core Components

1. **pydeptree/cli.py** - Basic CLI implementation
   - `ImportVisitor`: AST visitor for extracting import statements
   - `parse_imports()`: Parses a Python file and returns all imports
   - `is_project_module()`: Determines if an import is part of the project
   - `module_to_file_path()`: Converts module names to file paths
   - `get_dependencies()`: Recursively builds dependency graph with depth control
   - `build_rich_tree()`: Creates Rich tree visualization with circular dependency detection
   - `main()`: Click CLI entry point

2. **pydeptree/cli_enhanced.py** - Enhanced CLI with additional features
   - All functionality from basic CLI, plus:
   - `FileInfo`: Data class for storing file metadata (size, lines, lint issues)
   - `detect_file_type()`: Categorizes files (model, service, utils, test, main, other)
   - `run_ruff_check()`: Integrates with ruff for lint error detection
   - `get_file_info()`: Collects comprehensive file statistics
   - `format_file_label()`: Creates rich labels with badges and colors
   - `create_summary_table()`: Generates statistics table by file type

3. **Entry Points**: 
   - `pydeptree` maps to `pydeptree.cli:main` (basic CLI)
   - `pydeptree-enhanced` maps to `pydeptree.cli_enhanced:main` (enhanced CLI)

4. **Demo Components**:
   - `sample_project/` - Realistic Python project with intentional lint issues for demonstration
   - `demo_enhanced.py` - Interactive demo script showcasing enhanced features

### Key Design Decisions

- Uses AST parsing instead of regex for accurate import detection
- Filters out standard library and external packages to focus on project dependencies
- Handles circular dependencies by tracking visited files
- Supports configurable analysis depth to control recursion
- Uses Rich library for beautiful terminal output with progress indicators
- Supports both `import X` and `from X import Y` statements

### Testing Strategy

Tests use pytest with Click's CliRunner for CLI testing. Test fixtures create temporary Python files to test import analysis functionality.

### Distribution

- Package uses both pyproject.toml (modern) and setup.py (compatibility)
- Scripts use `uv` for building and `twine` for PyPI uploads
- API tokens stored in .env file (see .env.example)