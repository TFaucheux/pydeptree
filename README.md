# PyDepTree

[![PyPI version](https://badge.fury.io/py/pydeptree.svg)](https://badge.fury.io/py/pydeptree)
[![Python Support](https://img.shields.io/pypi/pyversions/pydeptree.svg)](https://pypi.org/project/pydeptree/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python dependency analyzer that visualizes module dependencies in your Python projects as a beautiful tree structure. Built with Rich for colorful terminal output.

![Demo](demo.png)

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

### Advanced Options

```bash
# Analyze dependencies up to 3 levels deep
pydeptree myapp.py --depth 3

# Show import statements from each file  
pydeptree myapp.py --show-code

# Specify a custom project root
pydeptree myapp.py --project-root /path/to/project
```

### Example Output

```
Analyzing dependencies for: /home/user/project/main.py
Project root: /home/user/project
Max depth: 2

Dependency tree:
└── main.py
    ├── utils/config.py
    │   ├── utils/validators.py
    │   └── models/settings.py
    └── services/api.py
        ├── utils/http.py
        └── models/response.py

Found 6 files with 8 total dependencies
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

### Testing the Enhanced Features
```bash
# Run the interactive demo
python demo_enhanced.py

# Try on the sample project (contains intentional lint errors for demo)
pydeptree-enhanced sample_project/main.py --depth 2

# Compare with original CLI
pydeptree sample_project/main.py --depth 2
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

## How It Works

PyDepTree uses Python's built-in AST (Abstract Syntax Tree) module to parse Python files and extract import statements. It then:

1. Identifies which imports are part of your project (vs external libraries)
2. Recursively analyzes imported modules up to the specified depth
3. Builds a dependency graph while detecting circular imports
4. Renders a beautiful tree visualization using Rich

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

## Notes
 - [GITHUB INSTRUCTIONS](GITHUB_INSTRUCTIONS.md)
 - [PYPI INSTRUCTIONS](DISTRIBUTION.md)

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
