#!/usr/bin/env python3
"""
Script to capture PyDepTree Advanced output in various formats for documentation
"""
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.text import Text
import tempfile
import os

def run_pydeptree_command(args):
    """Run pydeptree-advanced command and return stdout"""
    cmd = ['python', '-m', 'pydeptree.cli_advanced'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
    return result.stdout, result.stderr, result.returncode

def save_as_html(content, filename):
    """Save content as HTML with Rich formatting"""
    # Ensure docs directory exists
    Path("docs").mkdir(exist_ok=True)
    filepath = Path("docs") / filename
    console = Console(record=True, width=100)
    console.print(content, markup=False, highlight=False)
    console.save_html(str(filepath))
    print(f"HTML saved to: {filepath}")

def save_as_svg(content, filename):
    """Save content as SVG with Rich formatting"""
    # Ensure docs directory exists
    Path("docs").mkdir(exist_ok=True)
    filepath = Path("docs") / filename
    console = Console(record=True, width=100)
    console.print(content, markup=False, highlight=False)
    console.save_svg(str(filepath), title="PyDepTree Advanced Output")
    print(f"SVG saved to: {filepath}")

def save_as_text(content, filename):
    """Save content as plain text"""
    # Ensure docs directory exists
    Path("docs").mkdir(exist_ok=True)
    filepath = Path("docs") / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Text saved to: {filepath}")

def main():
    """Generate documentation outputs"""
    
    commands = [
        {
            'name': 'advanced_basic',
            'args': ['sample_project/main.py', '--depth', '2'],
            'description': 'Basic advanced analysis with complexity and metrics'
        },
        {
            'name': 'advanced_search_class',
            'args': ['sample_project/', '--search', 'Config', '--search-type', 'class'],
            'description': 'Search for classes containing "Config"'
        },
        {
            'name': 'advanced_search_function',
            'args': ['sample_project/', '--search', 'validate', '--search-type', 'function'],
            'description': 'Search for functions containing "validate"'
        },
        {
            'name': 'advanced_todos',
            'args': ['sample_project/main.py', '--depth', '2', '--show-todos'],
            'description': 'Show TODO comments and complexity metrics'
        },
        {
            'name': 'advanced_git_status',
            'args': ['sample_project/main.py', '--depth', '2', '--check-git'],
            'description': 'Show git status and file metrics'
        },
        {
            'name': 'advanced_requirements_preview',
            'args': ['sample_project/main.py', '--generate-requirements', '--no-interactive'],
            'description': 'Generate requirements.txt (preview mode)'
        },
        {
            'name': 'advanced_dependency_analysis',
            'args': ['sample_project/main.py', '--analyze-deps', '--dep-depth', '2'],
            'description': 'Show detailed dependency analysis like johnnydep'
        }
    ]
    
    print("🎬 Capturing PyDepTree Advanced CLI outputs for documentation...")
    print()
    
    for cmd_info in commands:
        print(f"📸 Capturing: {cmd_info['description']}")
        print(f"   Command: python -m pydeptree.cli_advanced {' '.join(cmd_info['args'])}")
        
        stdout, stderr, returncode = run_pydeptree_command(cmd_info['args'])
        
        if returncode != 0:
            print(f"   ❌ Error (exit code {returncode})")
            if stderr:
                print(f"   Error output: {stderr}")
            continue
        
        # Save in multiple formats
        base_name = f"advanced_output_{cmd_info['name']}"
        
        # Save as HTML (with colors)
        save_as_html(stdout, f"{base_name}.html")
        
        # Save as SVG (with colors, vector format)
        save_as_svg(stdout, f"{base_name}.svg")
        
        # Save as plain text
        save_as_text(stdout, f"{base_name}.txt")
        
        print(f"   ✅ Generated {base_name}.{{html,svg,txt}}")
        print()
    
    # Generate README snippet
    print("📝 Generating README snippet...")
    
    readme_snippet = """
## Advanced CLI Output Examples

### Basic Advanced Analysis with Complexity and Metrics

```bash
python -m pydeptree.cli_advanced sample_project/main.py --depth 2
```

![Advanced Output](docs/advanced_output_advanced_basic.svg)

### Search for Classes

```bash
python -m pydeptree.cli_advanced sample_project/ --search Config --search-type class
```

![Search Classes](docs/advanced_output_advanced_search_class.svg)

### Search for Functions

```bash
python -m pydeptree.cli_advanced sample_project/ --search validate --search-type function
```

![Search Functions](docs/advanced_output_advanced_search_function.svg)

### Requirements Generation (with Safety Features)

```bash
python -m pydeptree.cli_advanced sample_project/main.py --generate-requirements --no-interactive
```

![Requirements Generation](docs/advanced_output_advanced_requirements_preview.svg)

### Detailed Dependency Analysis

```bash
python -m pydeptree.cli_advanced sample_project/main.py --analyze-deps --dep-depth 2
```

![Dependency Analysis](docs/advanced_output_advanced_dependency_analysis.svg)

### Available Output Formats

For documentation purposes, you can also capture the output as:
- **HTML**: `console.save_html("output.html")` - Full Rich formatting for web display
- **SVG**: `console.save_svg("output.svg")` - Vector format perfect for GitHub/docs
- **Text**: Plain text format for embedding in documentation

"""
    
    with open("docs/README_ADVANCED_SNIPPET.md", "w") as f:
        f.write(readme_snippet)
    
    print("✅ README snippet saved to: docs/README_ADVANCED_SNIPPET.md")
    print()
    print("🎉 All outputs generated! You can now:")
    print("   - View HTML files in docs/ directory for full colors")
    print("   - Use SVG files in GitHub README (they preserve colors)")
    print("   - Include text files in code blocks")
    print("   - Copy content from docs/README_ADVANCED_SNIPPET.md to main README")

if __name__ == "__main__":
    main()