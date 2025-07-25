# PyDepTree

[![PyPI version](https://badge.fury.io/py/pydeptree.svg)](https://badge.fury.io/py/pydeptree)
[![Python Support](https://img.shields.io/pypi/pyversions/pydeptree.svg)](https://pypi.org/project/pydeptree/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python dependency analyzer that visualizes module dependencies in your Python projects as a beautiful tree structure. Built with Rich for colorful terminal output.

## 🎬 See PyDepTree in Action

![PyDepTree Demo](https://raw.githubusercontent.com/tfaucheux/pydeptree/main/images/pydeptree-demo.gif)

<details>
<summary>📸 View Individual Screenshots</summary>

### Basic CLI
![PyDepTree Basic](https://raw.githubusercontent.com/tfaucheux/pydeptree/main/images/pydeptree.png)

### Enhanced CLI with File Metrics
![PyDepTree Enhanced](https://raw.githubusercontent.com/tfaucheux/pydeptree/main/images/pydeptree-enhanced.png)

### Advanced CLI with All Features
![PyDepTree Advanced](https://raw.githubusercontent.com/tfaucheux/pydeptree/main/images/pydeptree-advanced.png)

### Advanced CLI with Dependency Analysis
![PyDepTree Requirements](https://raw.githubusercontent.com/tfaucheux/pydeptree/main/images/pydeptree-analyze-deps.png)

</details>

## 🚀 Three Powerful Versions

<details>
<summary>Compare Features Across Versions</summary>

| Feature | Basic CLI | Enhanced CLI | Advanced CLI |
|---------|-----------|--------------|--------------|
| Dependency Tree | ✅ | ✅ | ✅ |
| Configurable Depth | ✅ | ✅ | ✅ |
| Import Preview | ✅ | ✅ | ✅ |
| **Directory Input** | ✅ | ✅ | ✅ |
| Flexible Import Display | ❌ | ❌ | ✅ (inline/below/both) |
| File Type Colors | ❌ | ✅ | ✅ (+ Config) |
| File Metrics | ❌ | ✅ | ✅ |
| Lint Checking | ❌ | ✅ | ✅ |
| **Detailed Lint Reports** | ❌ | ❌ | ✅ (errors/warnings) |
| **Lint Rule Statistics** | ❌ | ❌ | ✅ |
| Summary Tables | ❌ | ✅ | ✅ |
| Search/Grep | ❌ | ❌ | ✅ |
| Complexity Analysis | ❌ | ❌ | ✅ |
| TODO Detection | ❌ | ❌ | ✅ |
| Git Integration | ❌ | ❌ | ✅ |
| Requirements.txt Gen | ❌ | ❌ | ✅ |
| Dependency Analysis | ❌ | ❌ | ✅ |

</details>

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Quick Start Examples](#quick-start-examples)
- [Demo and Sample Project](#demo-and-sample-project)
- [Command Line Options](#command-line-options)
- [Understanding the Metrics](#understanding-the-metrics)
- [Requirements Generation](#requirements-generation)
- [How It Works](#how-it-works)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

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
- 🎨 **Color-coded File Types**: Models (📊), Services (🌐), Utils (🔧), Tests (🧪), Main (🚀), Config (⚙️)
- 📈 **File Statistics**: Size, line count, and import count badges for each file
- 🔍 **Lint Integration**: Automatic error/warning detection using ruff (when available)
- 📊 **Summary Tables**: Aggregate statistics by file type with quality metrics
- 🎯 **Enhanced Visualization**: Rich terminal output with progress indicators and legends

### Advanced Features 🚀 (v0.3.0+)
- 🔎 **Search/Grep Integration**: Search for classes, functions, imports, or any text pattern
- 📐 **Complexity Metrics**: Cyclomatic complexity analysis with visual indicators
- 📍 **Flexible Import Display**: Show imports inline in tree, below tree, or both locations
- 📌 **TODO/FIXME Detection**: Automatically finds and displays TODO comments
- 🏗️ **Code Structure Metrics**: Function and class counts per file
- 🔄 **Git Integration**: Shows file modification status in version control
- 📄 **Requirements Generation**: Automatically generate requirements.txt from detected dependencies
- ⚙️ **Config File Detection** (v0.3.12+): Automatically detects and categorizes Python configuration files
- 📁 **Directory Input Support** (v0.3.19+): Analyze entire projects by passing a directory path
- 🔍 **Detailed Lint Reporting** (v0.3.19+): Show specific lint errors and warnings with file locations
- 📊 **Lint Rule Statistics** (v0.3.19+): Comprehensive statistics table showing lint issues by rule type

## Installation

### Using pip

```bash
pip install pydeptree
```

### Using pipx (recommended)

`pipx` installs CLI tools in isolated environments, preventing dependency conflicts.

#### If you already have pipx:
```bash
pipx install pydeptree
```

#### If you need to install pipx:

**macOS:**

```bash
# Option 1: Using Homebrew (recommended)
brew install pipx

# Option 2: Using pip
pip install pipx
pipx ensurepath
source ~/.zshrc  # or restart your terminal
```

**Windows:**

```bash
# Using pip
pip install pipx
pipx ensurepath
# Restart your command prompt/PowerShell
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install pipx

# Or using pip
pip install pipx
pipx ensurepath
source ~/.bashrc  # or restart your terminal
```

## 📦 Demo Files and Sample Project

If you installed PyDepTree via pip or pipx and want to run the demo scripts, download the demo package:

```bash
# Download the demos.zip file
curl -L https://github.com/TFaucheux/pydeptree/raw/main/demos.zip -o demos.zip

# Extract the demos
unzip demos.zip
```

The demos package includes:

- **demos/** - Directory containing all demo scripts:
  - **demo_basic.py** - Demonstrates basic dependency tree visualization
  - **demo_enhanced.py** - Shows enhanced features with file metrics and lint checking
  - **demo_advanced.py** - Showcases all advanced features including search, git integration, and complexity analysis
  - **demo_run_all.py** - Runs all demos sequentially for a complete overview
- **sample_project/** - A realistic Python project with intentional code issues for demonstration

After extracting, run the demos:
```bash
cd demos
python demo_basic.py
python demo_enhanced.py
python demo_advanced.py
python demo_run_all.py

# Or analyze the sample project
cd ..
pydeptree sample_project/main.py
```

Then install PyDepTree:
```bash
pipx install pydeptree
```

### From source

```bash
git clone https://github.com/tfaucheux/pydeptree.git
cd pydeptree
pip install -e .
```

## 🎬 Try the Interactive Demos

```bash
# Run all demos (basic → enhanced → advanced)
python demos/demo_run_all.py

# Or run individual demos
python demos/demo_basic.py      # Core dependency analysis features
python demos/demo_enhanced.py   # File types, statistics, lint checking  
python demos/demo_advanced.py   # Search, complexity, TODOs, and more
```

**Perfect for:**
- 🚀 **New users**: See all features in action with realistic examples
- 📚 **Learning**: Understand what each CLI version offers
- 🧪 **Testing**: Verify installation works correctly
- 🎯 **Evaluation**: Decide which features you need

Each demo creates temporary sample projects, so they work with pip, pipx, or source installations.

## Usage

### Basic Usage

Analyze a Python file and see its direct dependencies:

```bash
pydeptree myapp.py
```

Or analyze an entire project by passing a directory:

```bash
pydeptree sample_project --depth 2
```

### Enhanced Usage

Use the enhanced CLI for additional features:

```bash
pydeptree-enhanced myapp.py --depth 2
pydeptree-enhanced sample_project --depth 2  # Directory input
```

The enhanced version provides color-coded file types, lint checking, and detailed statistics.

### Advanced Usage (v0.3.19+)

Use the advanced CLI for search, complexity analysis, and comprehensive lint reporting:

```bash
pydeptree-advanced myapp.py --search "APIClient" --search-type class
pydeptree-advanced sample_project --depth 2  # Analyze entire project
```

The advanced version includes all enhanced features plus search capabilities, complexity metrics, TODO detection, git integration, detailed lint reporting, and lint rule statistics.

### Advanced Options

```bash
# Analyze dependencies up to 3 levels deep
pydeptree myapp.py --depth 3

# Show import statements from each file  
pydeptree myapp.py --show-code

# Specify a custom project root
pydeptree myapp.py --project-root /path/to/project
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
# Analyze entire project directory
pydeptree-advanced sample_project --depth 2

# Search for a specific class
pydeptree-advanced myapp.py --search "UserModel" --search-type class

# Search for functions containing 'validate'
pydeptree-advanced myapp.py --search "validate" --search-type function --depth 3

# Find all TODO comments
pydeptree-advanced myapp.py --search "TODO|FIXME|HACK" --depth 2

# Show detailed lint errors and warnings with file locations
pydeptree-advanced sample_project --show-errors --show-warnings

# Disable lint rule statistics (enabled by default)
pydeptree-advanced sample_project --no-show-lint-stats

# Minimal output with just file structure
pydeptree-advanced myapp.py --no-show-metrics --no-check-lint --no-show-stats

# Focus on complexity issues
pydeptree-advanced myapp.py --no-show-todos --no-check-git

# Generate requirements.txt from dependencies (with safety features)
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

## Advanced CLI Output Examples 

### Basic Advanced Analysis with Complexity and Metrics

```bash
pydeptree-advanced sample_project/main.py --depth 2
```
*Shows complexity metrics (C:4), function/class counts [0c/1f], lint warnings (W:5), file statistics, and comprehensive analysis with color-coded file types.*

### Requirements Generation with Safety Features

```bash
pydeptree-advanced sample_project/main.py --generate-requirements --no-interactive
```
*Demonstrates the safe requirements.txt generation feature with automatic backup protection and comprehensive dependency analysis.*

### Import Statement Display Options

The `--show-code` flag offers flexible ways to display import statements:

#### Inline Display (`--show-code=inline`)
Shows import statements directly in the dependency tree:

```bash
pydeptree-advanced myapp.py --show-code=inline
```

Example output:
```
🚀 main.py
├── 🌐 services/api.py
│   ├── 📊 models/response.py
│   ├──   └─ from models.response import APIResponse, ErrorResponse
│   └── 🔧 utils/http.py
└──   └─ from utils.http import HTTPClient, HTTPError
```

#### Below Display (`--show-code=below`)
Traditional display showing imports after the tree (default):

```bash
pydeptree-advanced myapp.py --show-code=below
# or simply:
pydeptree-advanced myapp.py --show-code
```

#### Both Locations (`--show-code=both`)
Displays imports both inline and at the bottom:

```bash
pydeptree-advanced myapp.py --show-code=both
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
- `FILE_OR_DIRECTORY`: Path to the Python file or directory to analyze (required)
- `-d, --depth INTEGER`: Maximum depth to traverse (default: 1)
- `-r, --project-root PATH`: Project root directory (default: file's parent or input directory)
- `-c, --show-code`: Display import statements from each file
- `--help`: Show help message and exit

### Enhanced CLI (`pydeptree-enhanced`)
All basic options plus:
- `-l, --check-lint / --no-check-lint`: Enable/disable lint checking (default: enabled)
- `-s, --show-stats / --no-show-stats`: Show/hide statistics summary table (default: enabled)

### Advanced CLI (`pydeptree-advanced`)
All enhanced options plus:
- `-c, --show-code [below|inline|both]`: Display import statements with flexible positioning
  - `below`: Show imports after the tree (default, backward compatible)
  - `inline`: Show imports directly in the tree structure
  - `both`: Show imports in both locations
- `-S, --search TEXT`: Search for text/pattern in files
- `--search-type [text|class|function|import]`: Type of search to perform (default: text)
- `--show-todos / --no-show-todos`: Show/hide TODO comments (default: enabled)
- `--check-git / --no-check-git`: Show/hide git status (default: enabled)
- `--show-metrics / --no-show-metrics`: Show/hide inline metrics like size, complexity (default: enabled)
- `--show-errors`: Show detailed lint errors with file names and line numbers
- `--show-warnings`: Show detailed lint warnings with file names and line numbers
- `--show-lint-stats / --no-show-lint-stats`: Show/hide lint rule statistics summary (default: enabled)
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

### File Type Detection
PyDepTree automatically categorizes Python files by analyzing their paths and names:

- **📊 Models**: Files in `/models/` directories or containing 'model' in the name
- **🌐 Services**: Files in `/services/` directories or containing 'service', 'api', 'client' in the name  
- **🔧 Utils**: Files in `/utils/` directories or containing 'util', 'helper' in the name
- **🧪 Tests**: Files in `/tests/` directories or starting with 'test_'
- **🚀 Main**: Files named 'main.py' or '__main__.py'
- **⚙️ Config**: Files like 'config.py', 'settings.py', 'env.py', or in `/config/` directories
- **📄 Other**: Files that don't match the above patterns

### Directory Input Support (v0.3.19+)
PyDepTree can analyze entire projects by accepting directory paths:

```bash
# Automatically finds entry point (main.py, app.py, etc.)
pydeptree-advanced sample_project --depth 2

# Entry point detection priority:
# 1. main.py
# 2. __main__.py  
# 3. app.py
# 4. run.py
# 5. start.py
# 6. index.py
# 7. __init__.py
# 8. First Python file found
```

When analyzing directories, PyDepTree automatically:
- Finds the most appropriate entry point file
- Sets the project root to the input directory
- Shows which entry point was selected
- Handles error cases gracefully (no Python files found)

### Advanced Lint Analysis (v0.3.19+)
PyDepTree now provides comprehensive lint analysis powered by ruff:

#### Lint Rule Statistics
Get project-wide statistics showing all lint issues by rule type:

```bash
pydeptree-advanced sample_project --show-lint-stats  # Default: enabled
```

Example output:
```
                           Lint Issues by Rule                           
╭──────────┬──────────────┬──────────┬──────────────────────────────────╮
│    Count │ Rule         │ Fixable  │ Description                      │
├──────────┼──────────────┼──────────┼──────────────────────────────────┤
│       35 │ W293         │    ✓     │ blank-line-with-whitespace       │
│       10 │ W292         │    ✓     │ missing-newline-at-end-of-file   │
│        6 │ I001         │    ✓     │ unsorted-imports                 │
│        5 │ B904         │    ✗     │ raise-without-from-inside-except │
╰──────────┴──────────────┴──────────┴──────────────────────────────────╯

Total issues: 67
```

#### Detailed Error and Warning Reports
Show specific lint issues with exact file locations:

```bash
# Show detailed errors with file:line:column locations
pydeptree-advanced sample_project --show-errors

# Show detailed warnings with file:line:column locations  
pydeptree-advanced sample_project --show-warnings

# Show both errors and warnings
pydeptree-advanced sample_project --show-errors --show-warnings
```

Example output:
```
Detailed Lint Errors:
  • sample_project/validators.py:25:13 - E722: bare-except
  • sample_project/http.py:45:1 - E501: line-too-long
  
  Total: 3 errors

Detailed Lint Warnings:  
  • sample_project/main.py:5:1 - W293: blank-line-with-whitespace
  • sample_project/api.py:22:1 - I001: unsorted-imports
  
  Total: 31 warnings
```

#### Lint Control Options
```bash
# Disable lint rule statistics (keep file-level lint summary)
pydeptree-advanced sample_project --no-show-lint-stats

# Disable all lint checking
pydeptree-advanced sample_project --no-check-lint

# Show only detailed errors/warnings (no statistics table)
pydeptree-advanced sample_project --show-errors --no-show-lint-stats
```

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
- **Advanced Safety Features**: Comprehensive protection against overwriting existing files:
  - **Interactive Prompts**: When requirements.txt exists, choose from: overwrite, backup_and_overwrite, save_as_new, or cancel
  - **Automatic Backups**: Creates timestamped backups (e.g., requirements.20250122_143021.backup)
  - **Change Preview**: Shows first 5 lines of current vs new content before overwriting
  - **Safe Non-Interactive Mode**: Auto-generates numbered filenames (requirements_1.txt, requirements_2.txt, etc.)
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
