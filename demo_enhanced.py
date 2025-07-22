#!/usr/bin/env python3
"""
Demo script to showcase PyDepTree enhanced features
"""
import subprocess
import sys
from pathlib import Path
import time

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    """Run a command and display it"""
    print(f"\n🔹 {description}")
    print(f"   Command: {' '.join(cmd)}")
    print("-" * 60)
    time.sleep(1)  # Brief pause for readability
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    """Run demo of PyDepTree features"""
    print_header("PyDepTree Enhanced Features Demo")
    
    # Check if we're in the right directory
    sample_dir = Path("sample_project")
    if not sample_dir.exists():
        print("❌ Error: sample_project directory not found!")
        print("   Please run this script from the pydeptree-package directory")
        return 1
    
    main_file = sample_dir / "main.py"
    if not main_file.exists():
        print("❌ Error: sample_project/main.py not found!")
        return 1
    
    print("✅ Found sample project")
    print(f"   Location: {sample_dir.resolve()}")
    
    # Demo 1: Basic dependency tree (original CLI)
    print_header("Demo 1: Basic Dependency Tree (Original CLI)")
    run_command(
        ["python", "-m", "pydeptree.cli", str(main_file), "--depth", "2"],
        "Running original PyDepTree with depth=2"
    )
    
    input("\n⏸  Press Enter to continue to enhanced version...")
    
    # Demo 2: Enhanced with all features
    print_header("Demo 2: Enhanced PyDepTree with All Features")
    run_command(
        ["python", "-m", "pydeptree.cli_enhanced", str(main_file), "--depth", "2"],
        "Running enhanced PyDepTree with file colors, lint checking, and statistics"
    )
    
    input("\n⏸  Press Enter to see more features...")
    
    # Demo 3: Show import statements
    print_header("Demo 3: Display Import Statements")
    run_command(
        ["python", "-m", "pydeptree.cli_enhanced", str(main_file), "--depth", "1", "--show-code"],
        "Showing actual import statements from files"
    )
    
    input("\n⏸  Press Enter to continue...")
    
    # Demo 4: Deeper analysis
    print_header("Demo 4: Deep Dependency Analysis")
    run_command(
        ["python", "-m", "pydeptree.cli_enhanced", str(main_file), "--depth", "3"],
        "Analyzing dependencies 3 levels deep"
    )
    
    # Summary
    print_header("Feature Summary")
    print("🌟 Enhanced PyDepTree Features:")
    print()
    print("  📊 Color-coded file types:")
    print("     • Models (cyan) 📊")
    print("     • Services (green) 🌐")  
    print("     • Utils (yellow) 🔧")
    print("     • Tests (magenta) 🧪")
    print("     • Main files (blue) 🚀")
    print()
    print("  📈 File statistics:")
    print("     • File size badges")
    print("     • Line count")
    print("     • Import count")
    print()
    print("  🔍 Code quality:")
    print("     • Lint error detection (E:n)")
    print("     • Lint warning detection (W:n)")
    print("     • Summary statistics table")
    print()
    print("  🎯 Additional features:")
    print("     • Circular dependency detection")
    print("     • Import statement preview")
    print("     • Progress indicators")
    print("     • Customizable depth analysis")
    print()
    print("✨ All features help you understand and improve your codebase!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())