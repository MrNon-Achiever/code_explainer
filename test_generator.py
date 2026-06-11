#!/usr/bin/env python3
"""
Test script for the Simplified Codebase-to-Course Generator

This script tests the generator functionality with a simple example.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import CodebaseAnalyzer, CourseGenerator

def test_analyzer():
    """Test the CodebaseAnalyzer class."""
    print("🧪 Testing CodebaseAnalyzer...")
    
    # Create a temporary test file
    test_code = '''
class TestClass:
    """A test class."""
    
    def __init__(self, name):
        """Initialize with name."""
        self.name = name
    
    def greet(self):
        """Return greeting."""
        return f"Hello, {self.name}!"


def test_function(x, y):
    """Add two numbers."""
    return x + y


if __name__ == "__main__":
    obj = TestClass("World")
    print(obj.greet())
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # Test analyzer
        analyzer = CodebaseAnalyzer(os.path.dirname(temp_file))
        analysis = analyzer.analyze()
        
        # Basic assertions
        assert "codebase_info" in analysis
        assert "modules" in analysis
        assert "classes" in analysis
        assert "functions" in analysis
        
        # Check if our test class was found
        found_class = False
        for class_name, class_info in analysis["classes"].items():
            if class_name == "TestClass":
                found_class = True
                assert len(class_info["methods"]) >= 2  # __init__ and greet
                break
        
        assert found_class, "TestClass not found in analysis"
        
        # Check if test function was found
        found_function = False
        for func_name, func_info in analysis["functions"].items():
            if func_name == "test_function":
                found_function = True
                assert len(func_info["args"]) == 2  # x and y
                break
        
        assert found_function, "test_function not found in analysis"
        
        print("✅ CodebaseAnalyzer tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ CodebaseAnalyzer test failed: {e}")
        return False
    finally:
        # Clean up
        os.unlink(temp_file)

def test_generator():
    """Test the CourseGenerator class."""
    print("\n🧪 Testing CourseGenerator...")
    
    # Create a simple analysis
    analysis = {
        "codebase_info": {
            "path": "/test/path",
            "total_files": 1,
            "analyzed_files": 1
        },
        "modules": {
            "test_module": {
                "path": "test_module.py",
                "full_path": "/test/path/test_module.py",
                "size": 100,
                "lines": 10,
                "imports": [],
                "classes": [],
                "functions": [],
                "docstring": "Test module",
                "is_main": True
            }
        },
        "classes": {},
        "functions": {
            "test_func": {
                "name": "test_func",
                "lineno": 1,
                "docstring": "A test function",
                "args": [{"name": "x", "annotation": None}],
                "is_private": False,
                "decorators": [],
                "returns": None,
                "module": "test_module",
                "file": "test_module.py"
            }
        },
        "imports": [],
        "main_files": [
            {
                "module": "test_module",
                "file": "test_module.py",
                "reason": "Contains if __name__ == '__main__' block"
            }
        ],
        "structure": {
            "directories": {".": 1},
            "file_types": {".py": 1},
            "complexity_score": 10
        }
    }
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Test generator
            generator = CourseGenerator(analysis)
            generator.generate(temp_dir)
            
            # Check if files were created
            output_path = Path(temp_dir)
            
            # Check required files
            required_files = [
                "styles.css",
                "main.js",
                "_base.html",
                "_footer.html",
                "build.sh",
                "index.html"
            ]
            
            for file_name in required_files:
                file_path = output_path / file_name
                assert file_path.exists(), f"Missing required file: {file_name}"
                assert file_path.stat().st_size > 0, f"Empty file: {file_name}"
            
            # Check modules directory
            modules_dir = output_path / "modules"
            assert modules_dir.exists(), "Missing modules directory"
            
            # Check module files
            module_files = list(modules_dir.glob("*.html"))
            assert len(module_files) >= 5, f"Expected at least 5 module files, got {len(module_files)}"
            
            # Check if index.html contains expected content
            index_content = (output_path / "index.html").read_text()
            assert "module-1" in index_content, "Missing module-1 in index.html"
            assert "module-2" in index_content, "Missing module-2 in index.html"
            
            print("✅ CourseGenerator tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ CourseGenerator test failed: {e}")
            return False

def main():
    """Run all tests."""
    print("🚀 Running tests for Simplified Codebase-to-Course Generator")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_analyzer()
    test2_passed = test_generator()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print("=" * 60)
    print(f"CodebaseAnalyzer: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"CourseGenerator: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed!")
        print("\nThe generator is working correctly.")
        print("\nTo generate a course from a real codebase:")
        print("python main.py /path/to/your/codebase")
        return 0
    else:
        print("\n💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
