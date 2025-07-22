#!/usr/bin/env python3
"""
Script to capture PyDepTree output in various formats for documentation
"""
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.text import Text
import tempfile
import os

def run_pydeptree_command(args):
    """Run pydeptree command and return stdout"""
    cmd = ['python', '-m', 'pydeptree.cli_enhanced'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
    return result.stdout, result.stderr, result.returncode

def save_as_html(content, filename):
    """Save content as HTML with Rich formatting"""
    console = Console(record=True, width=100)
    console.print(content, markup=False, highlight=False)
    console.save_html(filename)
    print(f"HTML saved to: {filename}")

def save_as_svg(content, filename):
    """Save content as SVG with Rich formatting"""
    console = Console(record=True, width=100)
    console.print(content, markup=False, highlight=False)
    console.save_svg(filename, title="PyDepTree Enhanced Output")
    print(f"SVG saved to: {filename}")

def save_as_text(content, filename):
    """Save content as plain text"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Text saved to: {filename}")

def main():
    """Generate documentation outputs"""
    
    commands = [
        {
            'name': 'enhanced_basic',
            'args': ['sample_project/main.py', '--depth', '2'],
            'description': 'Basic enhanced analysis'
        },
        {
            'name': 'enhanced_with_code',
            'args': ['sample_project/main.py', '--depth', '3', '--show-code'],
            'description': 'Enhanced analysis with import statements'
        },
        {
            'name': 'enhanced_no_lint',
            'args': ['sample_project/main.py', '--depth', '2', '--no-check-lint'],
            'description': 'Enhanced analysis without lint checking'
        },
        {
            'name': 'enhanced_no_stats',
            'args': ['sample_project/main.py', '--depth', '2', '--no-show-stats'],
            'description': 'Enhanced analysis without statistics table'
        }
    ]
    
    print("🎬 Capturing PyDepTree Enhanced CLI outputs for documentation...")
    print()
    
    for cmd_info in commands:
        print(f"📸 Capturing: {cmd_info['description']}")
        print(f"   Command: python -m pydeptree.cli_enhanced {' '.join(cmd_info['args'])}")
        
        stdout, stderr, returncode = run_pydeptree_command(cmd_info['args'])
        
        if returncode != 0:
            print(f"   ❌ Error (exit code {returncode})")
            if stderr:
                print(f"   Error output: {stderr}")
            continue
        
        # Save in multiple formats
        base_name = f"docs_output_{cmd_info['name']}"
        
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
## Enhanced CLI Output Examples

### Basic Enhanced Analysis

```bash
python -m pydeptree.cli_enhanced sample_project/main.py --depth 2
```

![Enhanced Output](docs_output_enhanced_basic.svg)

### With Import Statements

```bash
python -m pydeptree.cli_enhanced sample_project/main.py --depth 3 --show-code
```

![Enhanced with Code](docs_output_enhanced_with_code.svg)

### Available Output Formats

For documentation purposes, you can also capture the output as:
- **HTML**: `console.save_html("output.html")` - Full Rich formatting for web display
- **SVG**: `console.save_svg("output.svg")` - Vector format perfect for GitHub/docs
- **Text**: Plain text format for embedding in documentation

"""
    
    with open("README_SNIPPET.md", "w") as f:
        f.write(readme_snippet)
    
    print("✅ README snippet saved to: README_SNIPPET.md")
    print()
    print("🎉 All outputs generated! You can now:")
    print("   - View HTML files in browser for full colors")
    print("   - Use SVG files in GitHub README (they preserve colors)")
    print("   - Include text files in code blocks")
    print("   - Copy content from README_SNIPPET.md to main README")

if __name__ == "__main__":
    main()