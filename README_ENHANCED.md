# PyDepTree Enhanced Features

This document describes the enhanced version of PyDepTree with additional features for code quality analysis and visualization.

## ⚠️ Important Note About Sample Project

The included `sample_project/` directory contains **intentional linting errors, warnings, and code quality issues**. These are NOT bugs but deliberate examples designed to showcase the enhanced PyDepTree's lint detection capabilities. The sample project serves as a realistic demonstration of how the tool can identify and report code quality problems that commonly occur in real Python projects.

## Installation

To use the enhanced features, install with the enhanced extras:

```bash
pip install -e ".[enhanced]"
```

This will install `ruff` for lint checking capabilities.

## Usage

The enhanced CLI is available as `pydeptree-enhanced`:

```bash
pydeptree-enhanced sample_project/main.py --depth 2
```

## New Features

### 1. Color-Coded File Types

Files are automatically categorized and color-coded:

- 📊 **Models** (cyan) - Data models and schemas
- 🌐 **Services** (green) - API clients and service layers  
- 🔧 **Utils** (yellow) - Utility and helper functions
- 🧪 **Tests** (magenta) - Test files
- 🚀 **Main** (blue) - Entry point files
- 📄 **Other** (white) - Uncategorized files

### 2. File Statistics Badges

Each file displays inline statistics:

- **Size**: File size (B/KB/MB)
- **Lines**: Number of lines (e.g., `150L`)
- **Imports**: Import count with down arrow (e.g., `5↓`)

### 3. Lint Error Detection

When `ruff` is available, the tool checks for code quality issues:

- **Errors**: Displayed as `E:n` in red
- **Warnings**: Displayed as `W:n` in yellow

Files with issues are highlighted in the tree and summarized at the end.

### 4. Statistics Summary Table

A comprehensive table showing:

- File counts by type
- Total and average lines of code
- Aggregate error and warning counts

### 5. Enhanced Import Display

The `--show-code` flag now shows imports with syntax highlighting and proper categorization by file type.

## Example Output

```
Enhanced Python Dependency Analyzer

Legend: 📊 Models | 🌐 Services | 🔧 Utils | 🧪 Tests | 🚀 Main | Size | Lines | Imports↓ | E:Errors | W:Warnings

Dependency Tree:
└── 🚀 main.py 1.2KB 45L 2↓
    ├── 🔧 utils/config.py 2.3KB 89L 3↓ E:1 W:2
    │   ├── 🔧 utils/validators.py 1.1KB 67L 2↓ W:1
    │   └── 📊 models/settings.py 1.8KB 78L 1↓
    └── 🌐 services/api.py 3.2KB 125L 4↓ E:2
        ├── 🔧 utils/http.py 2.1KB 95L 3↓ W:3
        └── 📊 models/response.py 1.5KB 82L 2↓

File Statistics Summary:
╭────────────┬───────┬─────────────┬───────────┬────────┬──────────╮
│ Type       │ Count │ Total Lines │ Avg Lines │ Errors │ Warnings │
├────────────┼───────┼─────────────┼───────────┼────────┼──────────┤
│ 🚀 main    │ 1     │ 45          │ 45        │ -      │ -        │
│ 📊 model   │ 2     │ 160         │ 80        │ -      │ -        │
│ 🌐 service │ 1     │ 125         │ 125       │ 2      │ -        │
│ 🔧 utils   │ 3     │ 251         │ 83        │ 1      │ 6        │
├────────────┼───────┼─────────────┼───────────┼────────┼──────────┤
│ Total      │ 7     │ 581         │ 83        │ 3      │ 6        │
╰────────────┴───────┴─────────────┴───────────┴────────┴──────────╯

Lint Issues:
Files with errors:
  ✗ services/api.py - 2 error(s)
  ✗ utils/config.py - 1 error(s)

Files with warnings:
  ⚠ utils/http.py - 3 warning(s)
  ⚠ utils/config.py - 2 warning(s)
  ⚠ utils/validators.py - 1 warning(s)
```

## Command Line Options

All original options are supported, plus:

- `--check-lint / --no-check-lint`: Enable/disable lint checking (default: enabled)
- `--show-stats / --no-show-stats`: Show/hide statistics summary table (default: enabled)

## Running the Demo

A demo script is provided to showcase all features:

```bash
# Setup (installs ruff)
./setup_demo.sh

# Run demo
python demo_enhanced.py
```

The demo will walk through various usage examples and highlight the enhanced features.