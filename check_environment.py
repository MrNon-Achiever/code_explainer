#!/usr/bin/env python3
"""
Environment checker for Simplified Codebase-to-Course Generator

This script checks if the environment is properly set up
and all dependencies are installed.
"""

import sys
import os
import platform
import subprocess
import importlib
from pathlib import Path

def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("  ❌ Python 3.7 or higher is required!")
        return False
    
    print("  ✅ Python version OK")
    return True

def check_system_info():
    """Check system information."""
    print("\n💻 System Information:")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Processor: {platform.processor()}")
    
    # Check available disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_gb = free / (1024**3)
        print(f"  Free disk space: {free_gb:.1f} GB")
        
        if free_gb < 1:
            print("  ⚠️  Low disk space!")
        else:
            print("  ✅ Disk space OK")
    except:
        print("  ⚠️  Could not check disk space")
    
    return True

def check_pip():
    """Check if pip is available."""
    print("\n📦 Checking pip...")
    
    try:
        import pip
        print(f"  pip version: {pip.__version__}")
        print("  ✅ pip available")
        return True
    except ImportError:
        print("  ❌ pip not found!")
        print("  Please install pip: https://pip.pypa.io/en/stable/installation/")
        return False

def check_required_packages():
    """Check if required packages are installed."""
    print("\n📚 Checking required packages...")
    
    required_packages = [
        ("ast", "Built-in AST module"),
        ("pathlib", "Path handling"),
        ("argparse", "Command line parsing"),
        ("json", "JSON handling"),
        ("tempfile", "Temporary files"),
        ("shutil", "File operations"),
    ]
    
    all_ok = True
    
    for package, description in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package} - {description}")
        except ImportError:
            print(f"  ❌ {package} - {description} - MISSING!")
            all_ok = False
    
    return all_ok

def check_optional_packages():
    """Check optional packages."""
    print("\n🔧 Checking optional packages...")
    
    optional_packages = [
        ("streamlit", "Streamlit web interface"),
        ("pandas", "Data manipulation"),
        ("numpy", "Numerical computing"),
        ("black", "Code formatting"),
        ("flake8", "Code linting"),
        ("pytest", "Testing framework"),
    ]
    
    for package, description in optional_packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package} - {description}")
        except ImportError:
            print(f"  ⚠️  {package} - {description} - Not installed (optional)")
    
    return True

def check_project_files():
    """Check if project files exist."""
    print("\n📁 Checking project files...")
    
    required_files = [
        "main.py",
        "README.md",
        "USAGE.md",
        "requirements.txt",
    ]
    
    optional_files = [
        "streamlit_app.py",
        "example_usage.py",
        "test_generator.py",
        "demo.py",
        "config.json",
    ]
    
    all_ok = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING!")
            all_ok = False
    
    for file in optional_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} - Not found (optional)")
    
    return all_ok

def check_example_codebase():
    """Check if example codebase exists."""
    print("\n📂 Checking example codebase...")
    
    example_path = Path("example_codebase")
    
    if not example_path.exists():
        print("  ⚠️  Example codebase not found")
        return False
    
    python_files = list(example_path.rglob("*.py"))
    
    if not python_files:
        print("  ⚠️  No Python files found in example codebase")
        return False
    
    print(f"  ✅ Example codebase found with {len(python_files)} Python files")
    
    for py_file in python_files[:3]:  # Show first 3
        print(f"    - {py_file.name}")
    
    if len(python_files) > 3:
        print(f"    ... and {len(python_files) - 3} more")
    
    return True

def test_main_script():
    """Test if main script works."""
    print("\n🧪 Testing main script...")
    
    try:
        # Test help command
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("  ✅ main.py --help works")
            return True
        else:
            print(f"  ❌ main.py --help failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ❌ main.py --help timed out")
        return False
    except Exception as e:
        print(f"  ❌ Error testing main.py: {e}")
        return False

def test_imports():
    """Test if core imports work."""
    print("\n🔗 Testing imports...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from main import CodebaseAnalyzer, CourseGenerator
        
        print("  ✅ CodebaseAnalyzer imported")
        print("  ✅ CourseGenerator imported")
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error testing imports: {e}")
        return False

def run_all_checks():
    """Run all environment checks."""
    print("🚀 Environment Checker for Codebase-to-Course Generator")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("System Info", check_system_info),
        ("pip", check_pip),
        ("Required Packages", check_required_packages),
        ("Optional Packages", check_optional_packages),
        ("Project Files", check_project_files),
        ("Example Codebase", check_example_codebase),
        ("Main Script", test_main_script),
        ("Imports", test_imports),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ {name} check failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Environment Check Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Environment is ready.")
        print("\nYou can now run:")
        print("  python main.py /path/to/your/codebase")
        print("  python demo.py")
        print("  python example_usage.py")
        return 0
    elif passed >= total - 2:
        print("\n⚠️  Most checks passed. You should be able to run the generator.")
        print("Some optional features may not be available.")
        return 0
    else:
        print("\n❌ Many checks failed. Please fix the issues above.")
        print("See README.md for installation instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_checks())
