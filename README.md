# PyDepTree

[![PyPI version](https://badge.fury.io/py/pydeptree.svg)](https://badge.fury.io/py/pydeptree)
[![Python Support](https://img.shields.io/pypi/pyversions/pydeptree.svg)](https://pypi.org/project/pydeptree/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python dependency analyzer that visualizes module dependencies in your Python projects as a beautiful tree structure. Built with Rich for colorful terminal output.

![PyDepTree Enhanced Demo](https://raw.githubusercontent.com/TFaucheux/pydeptree/main/demo.png)

<!-- Alternative SVG demo if PNG doesn't load -->
<details>
<summary>📸 Alternative Demo (Click to expand)</summary>

![Enhanced Output](https://raw.githubusercontent.com/TFaucheux/pydeptree/main/docs/docs_output_enhanced_basic.svg)

</details>

> ✨ **Enhanced CLI Demo**: The screenshot above shows PyDepTree's enhanced features including color-coded file types, file statistics, lint detection, and summary tables.

## Features

### Core Features
- 🎯 **Smart Import Detection**: Uses AST parsing to accurately find all imports
- 🌳 **Beautiful Tree Visualization**: Rich-powered colorful dependency trees  
- 🔍 **Configurable Depth**: Control how deep to analyze dependencies
- 🚀 **Fast & Efficient**: Skips standard library and external packages
- 🎨 **Import Preview**: See actual import statements with `--show-code`
- 📊 **Progress Tracking**: Real-time progress for large codebases
- 🔄 **Circular Dependency Detection**: Identifies and handles circular imports

### Enhanced Features ✨
- 🎨 **Color-coded File Types**: Models (📊), Services (🌐), Utils (🔧), Tests (🧪), Main (🚀)
- 📈 **File Statistics**: Size, line count, and import count badges for each file
- 🔍 **Lint Integration**: Automatic error/warning detection using ruff (when available)
- 📊 **Summary Tables**: Aggregate statistics by file type with quality metrics
- 🎯 **Enhanced Visualization**: Rich terminal output with progress indicators and legends

### Advanced Features 🚀 (v0.3.0+)
- 🔎 **Search/Grep Integration**: Search for classes, functions, imports, or any text pattern
- 📐 **Complexity Metrics**: Cyclomatic complexity analysis with visual indicators
- 📌 **TODO/FIXME Detection**: Automatically finds and displays TODO comments
- 🏗️ **Code Structure Metrics**: Function and class counts per file
- 🔄 **Git Integration**: Shows file modification status in version control
- 📄 **Requirements Generation**: Automatically generate requirements.txt from detected dependencies

## Installation

### Using pip

```bash
pip install pydeptree
```

### Using pipx (recommended)

```bash
pipx install pydeptree
```

### From source

```bash
git clone https://github.com/tfaucheux/pydeptree.git
cd pydeptree
pip install -e .
```

### Enhanced Features Installation

For lint checking capabilities, install with enhanced dependencies:

```bash
pip install -e ".[enhanced]"
```

This installs `ruff` for code quality analysis.

## Usage

### Basic Usage

Analyze a Python file and see its direct dependencies:

```bash
pydeptree myapp.py
```

### Enhanced Usage

Use the enhanced CLI for additional features:

```bash
pydeptree-enhanced myapp.py --depth 2
```

The enhanced version provides color-coded file types, lint checking, and detailed statistics.

### Advanced Usage (v0.3.0+)

Use the advanced CLI for search, complexity analysis, and more:

```bash
pydeptree-advanced myapp.py --search "APIClient" --search-type class
```

The advanced version includes all enhanced features plus search capabilities, complexity metrics, TODO detection, and git integration.

### Advanced Options

```bash
# Analyze dependencies up to 3 levels deep
pydeptree myapp.py --depth 3

# Show import statements from each file  
pydeptree myapp.py --show-code

# Specify a custom project root
pydeptree myapp.py --project-root /path/to/project
```

### Enhanced CLI Example Output

```bash
python -m pydeptree.cli_enhanced sample_project/main.py --depth 2
```

```
╭───────── Analysis Settings ─────────╮
│ Enhanced Python Dependency Analyzer │
│                                     │
│ File: sample_project/main.py        │
│ Project root: sample_project        │
│ Max depth: 2                        │
│ Lint checking: enabled              │
╰─────────────────────────────────────╯

Legend:
📊 Models | 🌐 Services | 🔧 Utils | 🧪 Tests | 🚀 Main | Size | Lines | 
Imports↓ | E:Errors | W:Warnings

╭────────────────── Dependency Tree ──────────────────╮
│ 🚀 main.py 741B 31L 2↓ W:5                          │
│ ├── 🌐 services/api.py 2.1KB 71L 5↓ W:13            │
│ │   ├── 📊 models/response.py 1.4KB 54L 3↓ W:5      │
│ │   └── 🔧 utils/http.py 1.8KB 55L 3↓ E:2 W:14      │
│ └── 🔧 utils/config.py 1.4KB 53L 5↓ W:13            │
│     ├── 📊 models/settings.py 1.1KB 47L 2↓ W:4      │
│     └── 🔧 utils/validators.py 1.0KB 39L 2↓ E:1 W:3 │
╰─────────────────────────────────────────────────────╯

                      File Statistics Summary                       
┏━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ Type       ┃ Count ┃ Total Lines ┃ Avg Lines ┃ Errors ┃ Warnings ┃
┡━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ 🚀 main    │     1 │          31 │        31 │      - │        5 │
│ 📊 model   │     2 │         101 │        50 │      - │        9 │
│ 🌐 service │     1 │          71 │        71 │      - │       13 │
│ 🔧 utils   │     3 │         147 │        49 │      3 │       30 │
├────────────┼───────┼─────────────┼───────────┼────────┼──────────┤
│ Total      │     7 │         350 │        50 │      3 │       57 │
└────────────┴───────┴─────────────┴───────────┴────────┴──────────┘
```

### Advanced CLI Example Output

```bash
python -m pydeptree.cli_advanced sample_project/main.py --depth 2 --search "validate" --search-type function
```

```
╭───────────────────────────── Analysis Settings ──────────────────────────────╮
│ Advanced Python Dependency Analyzer                                          │
│                                                                              │
│ File: sample_project/main.py                                                 │
│ Project root: sample_project                                                 │
│ Max depth: 2                                                                 │
│ Lint checking: enabled                                                       │
│ Git status: enabled                                                          │
│ Search: validate (type: function)                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

Legend:
📊 Models | 🌐 Services | 🔧 Utils | 🧪 Tests | 🚀 Main | Size | Lines | 
Imports↓ | C:Complexity | [Nc/Nf] | E:Errors | W:Warnings | 📌TODOs | 🔍:Matches

╭────────────────────────────── Dependency Tree ───────────────────────────────╮
│ 🚀 main.py 741B 31L 2↓ C:4 [0c/1f] W:5                                       │
│ ├── 🌐 services/api.py 2.1KB 71L 5↓ C:4 [2c/4f] W:13                         │
│ │   ├── 📊 models/response.py 1.4KB 54L 3↓ C:2 [2c/3f] W:5                   │
│ │   └── 🔧 utils/http.py 1.8KB 55L 3↓ C:6 [2c/5f] E:2 W:14                   │
│ └── 🔧 utils/config.py 1.4KB 53L 5↓ C:6 [0c/2f] W:13 🔍1                     │
│     ├──   └─ Line 27: def validate_config(config: Dict[str, Any]) -> bool:   │
│     ├── 📊 models/settings.py 1.1KB 47L 2↓ C:3 [3c/3f] W:4 📌1 🔍1           │
│     │   └──   └─ Line 44: def validate(self) -> bool:                        │
│     └── 🔧 utils/validators.py 1.0KB 39L 2↓ C:6 [0c/4f] E:1 W:3 🔍4          │
│         ├──   └─ Line 8: def validate_url(url: str) -> bool:                 │
│         ├──   └─ Line 17: def validate_api_key(api_key: str) -> bool:        │
│         └──   └─ Line 28: def validate_timeout(timeout: int) -> bool:        │
╰──────────────────────────────────────────────────────────────────────────────╯

Found 7 files with 22 total dependencies

Search Results: Found 6 matches for 'validate'
```

## Quick Start Examples

### Basic Usage
```bash
# Analyze a Python file with the original CLI
pydeptree myapp.py

# Use the enhanced version with additional features
pydeptree-enhanced myapp.py --depth 2
```

### Enhanced Features Examples
```bash
# Disable lint checking
pydeptree-enhanced myapp.py --no-check-lint

# Disable statistics table
pydeptree-enhanced myapp.py --no-show-stats

# Show detailed import statements
pydeptree-enhanced myapp.py --show-code --depth 3
```

### Advanced Features Examples
```bash
# Search for a specific class
pydeptree-advanced myapp.py --search "UserModel" --search-type class

# Search for functions containing 'validate'
pydeptree-advanced myapp.py --search "validate" --search-type function --depth 3

# Find all TODO comments
pydeptree-advanced myapp.py --search "TODO|FIXME|HACK" --depth 2

# Minimal output with just file structure
pydeptree-advanced myapp.py --no-show-metrics --no-check-lint --no-show-stats

# Focus on complexity issues
pydeptree-advanced myapp.py --no-show-todos --no-check-git

# Generate requirements.txt from dependencies
pydeptree-advanced myapp.py --generate-requirements --depth 3

# Generate requirements without versions
pydeptree-advanced myapp.py --generate-requirements --no-versions --no-interactive

# Generate requirements to specific file
pydeptree-advanced myapp.py -R -o my-requirements.txt

# Show detailed dependency analysis like johnnydep
pydeptree-advanced myapp.py --generate-requirements --analyze-deps

# Deep dependency analysis
pydeptree-advanced myapp.py --analyze-deps --dep-depth 3
```

### Testing the Enhanced Features
```bash
# Run the interactive demo
python demo_enhanced.py

# Try on the sample project (contains intentional lint errors for demo)
pydeptree-enhanced sample_project/main.py --depth 2

# Try the advanced features
pydeptree-advanced sample_project/main.py --search "validate" --search-type function

# Compare all three CLIs
pydeptree sample_project/main.py --depth 2          # Basic
pydeptree-enhanced sample_project/main.py --depth 2  # Enhanced
pydeptree-advanced sample_project/main.py --depth 2  # Advanced
```

## Demo and Sample Project

PyDepTree includes a comprehensive sample project to demonstrate its enhanced features.

**⚠️ Note about Sample Project**: The `sample_project/` directory contains **intentional code quality issues** (linting errors, warnings, and code smells) to demonstrate the enhanced PyDepTree's lint checking capabilities. These are not bugs but deliberate examples that showcase how the tool can help identify code quality problems in real projects.

The sample project includes realistic examples of:
- Missing imports and type hints
- Unused variables
- Long lines exceeding style guidelines  
- Inefficient code patterns
- Complex conditions that could be simplified

This allows you to see how PyDepTree Enhanced detects and reports these issues with color-coded badges and summary statistics.

## Command Line Options

### Basic CLI (`pydeptree`)
- `FILE_PATH`: Path to the Python file to analyze (required)
- `-d, --depth INTEGER`: Maximum depth to traverse (default: 1)
- `-r, --project-root PATH`: Project root directory (default: file's parent)
- `-c, --show-code`: Display import statements from each file
- `--help`: Show help message and exit

### Enhanced CLI (`pydeptree-enhanced`)
All basic options plus:
- `-l, --check-lint / --no-check-lint`: Enable/disable lint checking (default: enabled)
- `-s, --show-stats / --no-show-stats`: Show/hide statistics summary table (default: enabled)

### Advanced CLI (`pydeptree-advanced`)
All enhanced options plus:
- `-S, --search TEXT`: Search for text/pattern in files
- `--search-type [text|class|function|import]`: Type of search to perform (default: text)
- `--show-todos / --no-show-todos`: Show/hide TODO comments (default: enabled)
- `--check-git / --no-check-git`: Show/hide git status (default: enabled)
- `--show-metrics / --no-show-metrics`: Show/hide inline metrics like size, complexity (default: enabled)
- `-R, --generate-requirements`: Generate requirements.txt from detected dependencies
- `-o, --requirements-output PATH`: Output path for requirements.txt (default: auto-generated)
- `--no-versions`: Generate requirements.txt without version numbers
- `--no-interactive`: Don't prompt for confirmation when requirements.txt exists
- `--analyze-deps`: Show detailed dependency analysis like johnnydep
- `--dep-depth INTEGER`: Maximum depth for dependency analysis (default: 2)

## Understanding the Metrics

### Inline Metrics (Advanced CLI)
- **Size**: File size (B/KB/MB)
- **Lines**: Total line count (e.g., `31L`)
- **Imports**: Number of import statements (e.g., `5↓`)
- **Complexity**: Cyclomatic complexity (e.g., `C:12`)
  - `C:1-5` (green/dim): Simple, easy to test
  - `C:6-10` (yellow): Moderate complexity
  - `C:11+` (red): High complexity, consider refactoring
- **Structure**: Class/function count (e.g., `[2c/5f]` = 2 classes, 5 functions)
- **Lint Issues**: 
  - `E:n` (red): Number of errors
  - `W:n` (yellow): Number of warnings
- **TODOs**: Number of TODO/FIXME comments (e.g., `📌3`)
- **Git Status**: `[M]` modified, `[A]` added, `[D]` deleted
- **Search Matches**: Number of search results (e.g., `🔍5`)

### Summary Table Columns
- **Type**: File category with icon
- **Count**: Number of files in category
- **Total/Avg Lines**: Code volume metrics
- **Functions/Classes**: Total count per category
- **Avg Complexity**: Average cyclomatic complexity
- **TODOs**: Total TODO comments found
- **Errors/Warnings**: Lint issue counts
- **Matches**: Search result counts (when searching)

## Requirements Generation

PyDepTree can automatically generate `requirements.txt` files from your project's external dependencies:

```bash
# Generate requirements.txt with versions
pydeptree-advanced myapp.py --generate-requirements

# Generate without versions
pydeptree-advanced myapp.py --generate-requirements --no-versions

# Specify output file
pydeptree-advanced myapp.py -R -o my-deps.txt
```

### Features:
- **Smart Detection**: Automatically identifies external packages (excludes stdlib and project modules)
- **Version Detection**: Attempts to detect installed package versions
- **File References**: Shows which files use each dependency
- **Safe Naming**: Automatically avoids overwriting existing requirements.txt
- **Rich Display**: Beautiful table showing dependencies with versions and usage
- **Dependency Tree Analysis**: Like johnnydep, shows transitive dependencies with descriptions
- **Package Summaries**: Displays what each package does

### Basic Example Output:
```
Found 2 external dependencies:
┏━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Package  ┃ Version   ┃ Used In             ┃
┡━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ requests │ 2.32.4    │ http.py             │
│ yaml     │ Not found │ config.py           │
└──────────┴───────────┴─────────────────────┘

✓ Requirements file written to: requirements_1.txt
```

### Enhanced Dependency Analysis (--analyze-deps):
```
Package Dependency Analysis:
📦 Dependencies
├── requests (2.32.4)
│   ├── Python HTTP for Humans.
│   ├── certifi (2025.7.14)
│   │   └── Python package for providing Mozilla's CA Bundle.
│   ├── charset_normalizer (3.4.2)
│   │   └── The Real First Universal Charset Detector.
│   ├── idna (3.10)
│   │   └── Internationalized Domain Names in Applications (IDNA)
│   └── urllib3 (2.5.0)
│       └── HTTP library with thread-safe connection pooling.
└── yaml (not installed)

Package Summary:
 Package                     Summary                                            
 certifi (2025.7.14)        Python package for providing Mozilla's CA Bundle.  
 charset_normalizer (3.4.2) The Real First Universal Charset Detector...       
 idna (3.10)                Internationalized Domain Names in Applications     
 requests (2.32.4)          Python HTTP for Humans.                            
 urllib3 (2.5.0)            HTTP library with thread-safe connection pooling.  
 yaml (not installed)       No description available                           

✓ Requirements file written to: requirements_1.txt
```

## How It Works

PyDepTree uses Python's built-in AST (Abstract Syntax Tree) module to parse Python files and extract import statements. It then:

1. Identifies which imports are part of your project (vs external libraries)
2. Recursively analyzes imported modules up to the specified depth
3. Builds a dependency graph while detecting circular imports
4. Renders a beautiful tree visualization using Rich

The Advanced CLI adds:
5. AST-based complexity analysis and code structure metrics
6. Pattern matching for search functionality
7. Git integration for version control awareness
8. Comment parsing for TODO detection

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/tfaucheux/pydeptree.git
cd pydeptree

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests (33 tests total: 5 basic + 28 enhanced)
pytest

# Run with coverage report (should show ~85% coverage)
pytest --cov=pydeptree --cov-report=term-missing

# Run only enhanced CLI tests
pytest tests/test_cli_enhanced.py

# Run linting (Note: sample_project/ contains intentional errors for demo purposes)
ruff check pydeptree/  # Check only the main package code (clean)
ruff check .           # Check everything (will show demo errors)
black --check .
mypy pydeptree
```

**Note**: The `sample_project/` directory contains intentional linting errors for demonstration purposes. When running linting tools on the entire project, you'll see these demo errors alongside any real issues in the main codebase.

### Building for Distribution

```bash
# Install build tools
pip install build twine

# Build distribution packages
python -m build

# Upload to TestPyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (for release)
twine upload dist/*
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Beautiful output powered by [Rich](https://github.com/Textualize/rich)
- Inspired by various dependency analysis tools in the Python ecosystem
