#!/usr/bin/env python3
"""
Example usage of the Simplified Codebase-to-Course Generator

This script demonstrates how to use the generator to analyze
a Python codebase and generate an interactive HTML course.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Simplified Codebase-to-Course Generator - Example Usage")
    print("=" * 60)
    
    # Check if example codebase exists
    example_codebase = Path("example_codebase")
    if not example_codebase.exists():
        print("❌ Example codebase not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check if main.py exists
    main_script = Path("main.py")
    if not main_script.exists():
        print("❌ main.py not found. Please ensure you're in the correct directory.")
        sys.exit(1)
    
    print("\n📁 Found example codebase: example_codebase/")
    print("📄 Main script: main.py")
    
    # Run the generator
    output_dir = "example_course_output"
    
    print(f"\n🔨 Generating course for example codebase...")
    print(f"📂 Output directory: {output_dir}")
    
    try:
        # Run the generator
        result = subprocess.run(
            [sys.executable, "main.py", "example_codebase", output_dir, "-v"],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("\n✅ Course generated successfully!")
        print("\n" + "=" * 60)
        print("📊 Generation Output:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("\n⚠️  Warnings/Errors:")
            print(result.stderr)
        
        # Check if output was created
        output_path = Path(output_dir)
        if output_path.exists():
            print(f"\n📂 Output files created in: {output_path.absolute()}")
            
            # List generated files
            print("\n📄 Generated files:")
            for file in sorted(output_path.rglob("*")):
                if file.is_file():
                    size = file.stat().st_size
                    print(f"  {file.relative_to(output_path)} ({size} bytes)")
            
            # Show how to view the course
            index_file = output_path / "index.html"
            if index_file.exists():
                print(f"\n🌐 To view the course, open in your browser:")
                print(f"   {index_file.absolute()}")
                
                # Try to open in browser (optional)
                try:
                    import webbrowser
                    print("\n🔄 Attempting to open in browser...")
                    webbrowser.open(f"file://{index_file.absolute()}")
                    print("✅ Browser opened (if supported)")
                except Exception as e:
                    print(f"⚠️  Could not auto-open browser: {e}")
                    print("   Please manually open the file in your browser.")
        else:
            print(f"\n❌ Output directory not found: {output_path}")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running generator:")
        print(f"Command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("📚 Example Usage Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open the generated index.html in your browser")
    print("2. Explore the interactive course")
    print("3. Try analyzing your own codebase:")
    print("   python main.py /path/to/your/codebase")
    print("\nFor more options, run: python main.py --help")

if __name__ == "__main__":
    main()
