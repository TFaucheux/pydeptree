# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-01-22

### Added
- **Enhanced CLI** (`pydeptree-enhanced`) with advanced features:
  - Color-coded file types: Models (📊), Services (🌐), Utils (🔧), Tests (🧪), Main (🚀)
  - File statistics badges: size, line count, import count
  - Lint error/warning detection using ruff integration
  - Summary statistics table by file type
  - Enhanced Rich terminal output with progress indicators
- **Comprehensive test suite** with 28 new tests for enhanced features (33 total tests, 85% coverage)
- **Sample project** with intentional lint errors for demonstration purposes
- **Interactive demo script** (`demo_enhanced.py`) showcasing all features
- **Extensive documentation** updates explaining enhanced features
- **New CLI options**: `--check-lint/--no-check-lint`, `--show-stats/--no-show-stats`

### Enhanced
- Updated README with Quick Start examples and enhanced feature documentation
- Added comprehensive test coverage for all new functionality
- Improved error handling and user experience
- Enhanced project structure with better separation of concerns

### Fixed
- Proper Click option handling for boolean flags with negation support

## [0.1.0] - 2024-01-22

### Added
- Initial release
- Python dependency tree analysis with AST parsing
- Rich terminal output with colored trees
- Configurable depth traversal
- Project root detection
- Circular dependency handling
- Import statement preview with `--show-code`
- Progress indicators for large codebases
- Support for Python 3.7+