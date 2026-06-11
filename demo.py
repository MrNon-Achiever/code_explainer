#!/usr/bin/env python3
"""
Demo script for Simplified Codebase-to-Course Generator

This script demonstrates the generator with the included example codebase
and shows how to use it programmatically.
"""

import os
import sys
import webbrowser
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import CodebaseAnalyzer, CourseGenerator

def demo_analysis():
    """Demonstrate codebase analysis."""
    print("🔍 DEMO: Codebase Analysis")
    print("=" * 50)
    
    # Analyze the example codebase
    codebase_path = "example_codebase"
    
    print(f"📁 Analyzing: {codebase_path}")
    
    # Create analyzer
    analyzer = CodebaseAnalyzer(codebase_path)
    
    # Run analysis
    analysis = analyzer.analyze()
    
    # Display results
    print(f"\n📊 Analysis Results:")
    print(f"  Files analyzed: {analysis['codebase_info']['total_files']}")
    print(f"  Classes found: {len(analysis['classes'])}")
    print(f"  Functions found: {len(analysis['functions'])}")
    print(f"  Main files: {len(analysis['main_files'])}")
    print(f"  Complexity score: {analysis['structure']['complexity_score']}")
    
    # Show some classes
    if analysis['classes']:
        print(f"\n🏗️  Key Classes:")
        for class_name, class_info in list(analysis['classes'].items())[:3]:
            methods_count = len(class_info.get('methods', []))
            print(f"  - {class_name}: {methods_count} methods")
    
    # Show some functions
    if analysis['functions']:
        print(f"\n⚡ Key Functions:")
        for func_name, func_info in list(analysis['functions'].items())[:3]:
            args_count = len(func_info.get('args', []))
            print(f"  - {func_name}({args_count} args)")
    
    return analysis

def demo_generation(analysis):
    """Demonstrate course generation."""
    print(f"\n\n📝 DEMO: Course Generation")
    print("=" * 50)
    
    output_dir = "demo_course_output"
    
    print(f"📂 Generating course in: {output_dir}")
    
    # Create generator
    generator = CourseGenerator(analysis)
    
    # Generate course
    generator.generate(output_dir)
    
    # List generated files
    output_path = Path(output_dir)
    print(f"\n📄 Generated files:")
    
    total_size = 0
    for file in sorted(output_path.rglob("*")):
        if file.is_file():
            size = file.stat().st_size
            total_size += size
            print(f"  {file.relative_to(output_path)} ({size:,} bytes)")
    
    print(f"\n📊 Total size: {total_size:,} bytes")
    
    # Show how to view the course
    index_file = output_path / "index.html"
    print(f"\n🌐 To view the course, open in your browser:")
    print(f"   {index_file.absolute()}")
    
    return output_dir

def demo_interactive_features():
    """Demonstrate interactive features."""
    print(f"\n\n🎮 DEMO: Interactive Features")
    print("=" * 50)
    
    print("The generated course includes:")
    print("  ✅ Scroll-based navigation with progress tracking")
    print("  ✅ Code ↔ Plain English translations")
    print("  ✅ Multiple-choice quizzes with instant feedback")
    print("  ✅ Visual component cards and diagrams")
    print("  ✅ Responsive design for all devices")
    print("  ✅ Smooth animations and transitions")
    
    print(f"\n🎯 Course Modules:")
    print("  1. Introduction - What the project does")
    print("  2. Architecture - How it's structured")
    print("  3. Components - Key classes and responsibilities")
    print("  4. Data Flow - How data moves through the system")
    print("  5. Interactive Elements - Key functions and usage")

def demo_customization():
    """Demonstrate customization options."""
    print(f"\n\n🎨 DEMO: Customization Options")
    print("=" * 50)
    
    print("You can customize the generated course:")
    print("\n1. Change accent colors:")
    print("   Edit _base.html and modify CSS variables:")
    print("   --color-accent: #D94F30  (Vermillion - default)")
    print("   --color-accent: #E06B56  (Coral)")
    print("   --color-accent: #2A7B9B  (Teal)")
    print("   --color-accent: #D4A843  (Amber)")
    print("   --color-accent: #2D8B55  (Forest)")
    
    print("\n2. Modify course content:")
    print("   Edit HTML files in modules/ directory")
    print("   Add new interactive elements")
    print("   Customize quiz questions")
    
    print("\n3. Rebuild the course:")
    print("   Run: bash build.sh")
    print("   Or manually assemble: cat _base.html modules/*.html _footer.html > index.html")

def main():
    """Run the demo."""
    print("🚀 Simplified Codebase-to-Course Generator - DEMO")
    print("=" * 60)
    
    try:
        # Run analysis demo
        analysis = demo_analysis()
        
        # Run generation demo
        output_dir = demo_generation(analysis)
        
        # Show interactive features
        demo_interactive_features()
        
        # Show customization options
        demo_customization()
        
        print(f"\n\n" + "=" * 60)
        print("✅ DEMO COMPLETE!")
        print("=" * 60)
        
        # Try to open in browser
        index_file = Path(output_dir) / "index.html"
        if index_file.exists():
            print(f"\n🌐 Opening course in browser...")
            try:
                webbrowser.open(f"file://{index_file.absolute()}")
                print("✅ Browser opened successfully!")
            except Exception as e:
                print(f"⚠️  Could not auto-open browser: {e}")
                print("   Please manually open the file in your browser.")
        
        print(f"\n📚 Next steps:")
        print("  1. Explore the generated course in your browser")
        print("  2. Try analyzing your own codebase:")
        print("     python main.py /path/to/your/python/project")
        print("  3. Use the Streamlit web interface:")
        print("     streamlit run streamlit_app.py")
        print("  4. Read the documentation:")
        print("     README.md and USAGE.md")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
