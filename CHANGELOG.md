# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.20] - 2025-07-25

## [0.3.19] - 2025-07-25

## [0.3.18] - 2025-07-23

## [0.3.17] - 2025-07-23

## [0.3.17] - 2025-07-23

### Changed
- Reorganized demo files into a dedicated `demos/` directory for cleaner project structure
- Updated `demos.zip` to include the new directory structure
- Updated README instructions to reflect the new demo file locations
- Cleaned up project root by moving all demo_*.py files to demos/ subdirectory

## [0.3.16] - 2025-07-23

## [0.3.15] - 2025-07-23

## [0.3.15] - 2025-07-23

### Added
- Added demos.zip file for easy access to demo scripts and sample project
- Added instructions in README for downloading demos after pip/pipx installation

### Changed
- Improved demo accessibility for users who install via package managers

## [0.3.14] - 2025-07-23

### Fixed
- Fixed distribution packaging to include demo files and sample_project directory
- Updated MANIFEST.in to ensure demo_*.py files and sample_project/ are included in PyPI distribution

## [0.3.13] - 2025-07-23

## [0.3.12] - 2025-07-23

## [0.3.11] - 2025-07-23

## [0.3.10] - 2025-07-23

## [0.3.9] - 2025-01-23

### Enhanced
- **Simplified Installation**: Moved `ruff` from optional to main dependencies
  - Lint checking now works out of the box with `pip install pydeptree` or `pipx install pydeptree`
  - Removed confusing `[enhanced]` installation instructions from README
  - All enhanced and advanced CLI features now work immediately after installation
  - No more silent failures when lint checking is expected but ruff is missing

## [0.3.8] - 2025-01-23

### Fixed
- **Advanced CLI --show-code Option**: Resolved Click option conflict that prevented `--show-code=inline` from working
  - Fixed parameter mapping issue that caused "Option '--show-code' does not take a value" error
  - All show-code modes now work correctly: inline, below, both
  - Maintains backward compatibility with existing usage patterns

## [0.3.7] - 2025-01-23

### Fixed
- **Installation Documentation**: Removed incorrect Homebrew installation instructions
  - Removed misleading `brew install pydeptree` command that doesn't work
  - Clarified that pipx is the recommended installation method for CLI tools

## [0.3.6] - 2025-01-23

### Enhanced
- **Installation Documentation**: Added comprehensive pipx installation instructions
  - Platform-specific instructions for macOS, Windows, and Linux
  - Multiple installation methods (Homebrew, pip, package managers)
  - Clear explanation of pipx benefits (isolated environments)
  - Step-by-step guidance from installation to usage

## [0.3.5] - 2025-01-23

### Fixed
- **PyPI Image Display**: Updated all image URLs in README to use raw GitHub content URLs
  - Images now display properly on the PyPI package page
  - Changed from relative paths (`images/file.png`) to full URLs (`https://raw.githubusercontent.com/tfaucheux/pydeptree/main/images/file.png`)

## [0.3.4] - 2025-01-23

### Fixed
- **PyPI Image Display**: Updated all image URLs in README to use raw GitHub content URLs
  - Images now display properly on the PyPI package page
  - Changed from relative paths (`images/file.png`) to full URLs (`https://raw.githubusercontent.com/tfaucheux/pydeptree/main/images/file.png`)

## [0.3.3] - 2025-01-23

### Added
- **Flexible Import Display**: Enhanced `--show-code` with three display modes
  - `--show-code=inline`: Shows import statements directly in the dependency tree
  - `--show-code=below`: Shows imports after the tree (default, backward compatible)
  - `--show-code=both`: Shows imports in both locations
  - Displays actual import statements from source code with syntax highlighting
- **Enhanced GIF Generator**: Improved animated demo generation
  - Support for 4th image (Requirements Generation demo)
  - Configurable width/height parameters (`--width`, `--height`)
  - Adjustable frame duration (`--duration`)
  - Smart image resizing with aspect ratio preservation

### Fixed
- **--analyze-deps Independence**: Fixed issue where `--analyze-deps` required `--generate-requirements`
  - Can now use dependency analysis without generating requirements.txt files
  - Maintains backward compatibility with combined usage

### Enhanced
- **README Documentation**: Comprehensive documentation for new import display features
- **Feature Comparison Table**: Updated to show flexible import display capabilities
- **Visual Examples**: Added examples showing inline import display in trees

## [0.3.2] - 2025-01-22

### Added
- **Requirements.txt Safety Features**: Comprehensive protection against overwriting existing files
  - Interactive prompts with four options: overwrite, backup_and_overwrite, save_as_new, cancel
  - Automatic timestamped backups (e.g., requirements.20250122_143021.backup)
  - Preview of changes before overwriting showing first 5 lines of current vs new content
  - Safe non-interactive mode that auto-generates numbered filenames (requirements_1.txt, requirements_2.txt, etc.)
  - Unique backup name generation to prevent backup conflicts

### Enhanced
- `write_requirements_file()` function now includes comprehensive safety mechanisms
- Better user experience with clear choices and previews when requirements.txt exists
- Improved error handling for file operations

## [0.3.1] - 2025-01-22

### Added
- **Table of Contents**: Added comprehensive table of contents to README for better navigation

### Changed
- Improved README organization and readability

## [0.3.0] - 2025-01-22

### Added
- **Advanced CLI** (`pydeptree-advanced`) with powerful new features:
  - **Search/Grep functionality**: Search for classes, functions, imports, or any text pattern
  - **Complexity metrics**: Cyclomatic complexity analysis with visual indicators (C:1-5 dim, C:6-10 yellow, C:11+ red)
  - **TODO/FIXME detection**: Automatically finds and displays TODO, FIXME, HACK, XXX, NOTE, OPTIMIZE, and BUG comments
  - **Code structure metrics**: Function and class counts per file (e.g., [2c/5f] = 2 classes, 5 functions)
  - **Git integration**: Shows file modification status in version control ([M] modified, [A] added, [D] deleted)
  - **Enhanced search display**: Inline display of search matches with line numbers
- **New command-line options**:
  - `--search TEXT`: Search for text/pattern in files
  - `--search-type [text|class|function|import]`: Type of search to perform
  - `--show-todos/--no-show-todos`: Control TODO comment display
  - `--check-git/--no-check-git`: Enable/disable git status checking
  - `--show-metrics/--no-show-metrics`: Control inline metrics display
- **Requirements generation**: Generate requirements.txt from detected external dependencies
  - Smart detection excludes stdlib and project modules
  - Version detection from installed packages
  - File usage references in comments
  - Safe auto-naming to avoid overwriting existing files
  - Rich table display of dependencies
- **Enhanced dependency analysis**: johnnydep-style dependency trees
  - Transitive dependency analysis (package dependencies of dependencies)
  - Package summaries and descriptions
  - Rich tree visualization showing dependency relationships
  - Configurable analysis depth
- **Documentation**: Added comprehensive examples and metric explanations in README

### New Command-line Options (v0.3.0)
- `-R, --generate-requirements`: Generate requirements.txt from dependencies
- `-o, --requirements-output PATH`: Specify output path for requirements file
- `--no-versions`: Generate requirements without version numbers
- `--no-interactive`: Skip prompts when requirements.txt exists
- `--analyze-deps`: Show detailed dependency analysis like johnnydep
- `--dep-depth INTEGER`: Maximum depth for dependency analysis

### Changed
- Git status detection now properly finds the git repository root
- Search results are displayed inline in the dependency tree with context
- TODO comments show line numbers for easy navigation

### Fixed
- Git status now works correctly when project root differs from git root

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