# PyDepTree

[![PyPI version](https://badge.fury.io/py/pydeptree.svg)](https://badge.fury.io/py/pydeptree)
[![Python Support](https://img.shields.io/pypi/pyversions/pydeptree.svg)](https://pypi.org/project/pydeptree/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python dependency analyzer that visualizes module dependencies in your Python projects as a beautiful tree structure. Built with Rich for gorgeous terminal output.

![Demo](https://user-images.githubusercontent.com/placeholder/demo.gif)

## Features

- 🎯 **Smart Import Detection**: Uses AST parsing to accurately find all imports
- 🌳 **Beautiful Tree Visualization**: Rich-powered colorful dependency trees  
- 🔍 **Configurable Depth**: Control how deep to analyze dependencies
- 🚀 **Fast & Efficient**: Skips standard library and external packages
- 🎨 **Import Preview**: See actual import statements with `--show-code`
- 📊 **Progress Tracking**: Real-time progress for large codebases
- 🔄 **Circular Dependency Detection**: Identifies and handles circular imports

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

## Usage

### Basic Usage

Analyze a Python file and see its direct dependencies:

```bash
pydeptree myapp.py
```

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

## Command Line Options

- `FILE_PATH`: Path to the Python file to analyze (required)
- `-d, --depth INTEGER`: Maximum depth to traverse (default: 1)
- `-r, --project-root PATH`: Project root directory (default: file's parent)
- `-c, --show-code`: Display import statements from each file
- `--help`: Show help message and exit

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
# Run tests
pytest

# Run with coverage
pytest --cov=pydeptree

# Run linting
ruff check .
black --check .
mypy pydeptree
```

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