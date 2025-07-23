#!/usr/bin/env python3
"""
Demo script that runs all PyDepTree demonstrations
Shows basic, enhanced, and advanced CLI features in sequence.
"""
import subprocess
import sys
import time
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f" {text}")
    print("="*70 + "\n")

def print_section(text):
    """Print a section divider"""
    print("\n" + "-"*50)
    print(f"🔸 {text}")
    print("-"*50)

def run_demo_script(script_name, description):
    """Run a demo script and return success status"""
    print_section(f"Running {script_name}")
    print(f"📋 {description}")
    print(f"   Script: {script_name}")
    print()
    
    time.sleep(2)  # Brief pause for readability
    
    try:
        result = subprocess.run([sys.executable, script_name], check=False)
        if result.returncode == 0:
            print(f"\n✅ {script_name} completed successfully!")
            return True
        else:
            print(f"\n❌ {script_name} failed with exit code {result.returncode}")
            return False
    except Exception as e:
        print(f"\n❌ Error running {script_name}: {e}")
        return False

def check_prerequisites():
    """Check if PyDepTree is installed and available"""
    print_section("Checking Prerequisites")
    
    commands_to_check = ["pydeptree", "pydeptree-enhanced", "pydeptree-advanced"]
    all_available = True
    
    for cmd in commands_to_check:
        try:
            result = subprocess.run([cmd, "--help"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                print(f"✅ {cmd} is available")
            else:
                print(f"❌ {cmd} is not working properly")
                all_available = False
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            print(f"❌ {cmd} is not available")
            all_available = False
    
    if not all_available:
        print("\n⚠️  Some PyDepTree commands are not available.")
        print("   Please ensure PyDepTree is properly installed:")
        print("   pip install pydeptree")
        print("   or")  
        print("   pipx install pydeptree")
        return False
    
    print("\n✅ All PyDepTree commands are available!")
    return True

def main():
    """Run all PyDepTree demonstrations"""
    print_header("PyDepTree Complete Demo Suite")
    print("This script demonstrates all PyDepTree features across three CLI versions:")
    print("• Basic CLI: Core dependency analysis")
    print("• Enhanced CLI: File types, statistics, and lint checking") 
    print("• Advanced CLI: Search, complexity, TODOs, and advanced features")
    print("\nEach demo creates its own temporary sample project, so this works")
    print("regardless of how PyDepTree was installed (pip, pipx, or from source).")
    
    # Check prerequisites
    if not check_prerequisites():
        return 1
    
    # Demo scripts to run
    demos = [
        ("demo_basic.py", "Basic CLI features - core dependency analysis"),
        ("demo_enhanced.py", "Enhanced CLI features - file types and statistics"),
        ("demo_advanced.py", "Advanced CLI features - search, complexity, and more")
    ]
    
    # Check if demo scripts exist
    print_section("Checking Demo Scripts")
    missing_scripts = []
    
    for script_name, _ in demos:
        script_path = Path(script_name)
        if script_path.exists():
            print(f"✅ Found {script_name}")
        else:
            print(f"❌ Missing {script_name}")
            missing_scripts.append(script_name)
    
    if missing_scripts:
        print(f"\n❌ Missing demo scripts: {', '.join(missing_scripts)}")
        print("   Please ensure all demo scripts are in the current directory.")
        return 1
    
    print("\n✅ All demo scripts found!")
    
    # Run demos
    successful_demos = 0
    total_demos = len(demos)
    
    print_header("Running All Demonstrations")
    
    for i, (script_name, description) in enumerate(demos, 1):
        print(f"\n📍 Demo {i}/{total_demos}: {script_name}")
        
        if run_demo_script(script_name, description):
            successful_demos += 1
        
        if i < total_demos:
            print(f"\n⏳ Preparing next demo...")
            time.sleep(3)  # Brief pause between demos
    
    # Summary
    print_header("Demo Suite Complete!")
    
    if successful_demos == total_demos:
        print("🎉 All demonstrations completed successfully!")
        print(f"\n📊 Results: {successful_demos}/{total_demos} demos passed")
        print("\n✨ You've seen all PyDepTree features in action!")
        print("\n🚀 Ready to use PyDepTree on your own projects:")
        
        print("\n   Basic usage:")
        print("   pydeptree your_file.py")
        
        print("\n   Enhanced features:")
        print("   pydeptree-enhanced your_file.py --check-lint --show-stats")
        
        print("\n   Advanced features:")
        print("   pydeptree-advanced your_file.py --search 'TODO' --show-metrics")
        
        print("\n📖 For more information:")
        print("   https://github.com/tfaucheux/pydeptree")
        
        return 0
    else:
        print(f"⚠️  Some demonstrations had issues.")
        print(f"📊 Results: {successful_demos}/{total_demos} demos passed")
        
        if successful_demos > 0:
            print("\n✅ The working demos show that PyDepTree is functional.")
            print("   Failed demos may be due to missing dependencies or environment issues.")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())