# Sample Project for PyDepTree Enhanced Demo

This sample project demonstrates the enhanced PyDepTree features with a realistic Python project structure.

## Project Structure

```
sample_project/
├── main.py              # 🚀 Main entry point
├── utils/               # 🔧 Utility modules
│   ├── config.py        # Configuration management
│   ├── validators.py    # Input validation functions
│   └── http.py          # HTTP client utilities
├── models/              # 📊 Data models
│   ├── settings.py      # Settings data classes
│   └── response.py      # API response models
└── services/            # 🌐 Service layers
    └── api.py           # API client service
```

## ⚠️ Important: Intentional Code Quality Issues

**This sample project contains intentional linting errors and warnings** to demonstrate the enhanced PyDepTree lint checking features. These are NOT bugs but deliberate examples including:

### Lint Issues Included:
- **Missing imports** (e.g., `Optional` type hint without import)
- **Unused variables** (e.g., `debug_mode` in config.py)
- **Long lines** that exceed the configured line length
- **Inefficient code patterns** (e.g., string concatenation instead of f-strings)
- **Complex conditions** that could be simplified
- **Missing exception handling** in some cases

### Why These Issues Exist:
1. **Feature Demonstration**: Shows how PyDepTree Enhanced detects and reports code quality issues
2. **Real-world Examples**: Represents common code quality problems found in projects
3. **Visual Testing**: Allows you to see the enhanced CLI's lint reporting in action

## Running the Demo

To see the enhanced PyDepTree in action with this sample project:

```bash
# Basic enhanced analysis
python -m pydeptree.cli_enhanced sample_project/main.py --depth 2

# With detailed import information
python -m pydeptree.cli_enhanced sample_project/main.py --depth 2 --show-code

# Run the full interactive demo
python demo_enhanced.py
```

## Expected Output Features

When you run the enhanced CLI on this sample project, you should see:

- **Color-coded file types** with appropriate icons
- **File statistics** (size, lines, import count) for each file
- **Lint error/warning counts** displayed as badges (E:n, W:n)
- **Summary statistics table** showing aggregated information by file type
- **Lint issues section** listing files with the most problems

This demonstrates how the enhanced PyDepTree can help you understand both your project's dependency structure and code quality at a glance.