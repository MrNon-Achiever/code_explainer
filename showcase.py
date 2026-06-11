#!/usr/bin/env python3
"""
Project Showcase Script

This script demonstrates the Simplified Codebase-to-Course Generator
by showing its capabilities and generating example output.
"""

import os
import sys
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_header(text, width=60):
    """Print a formatted header."""
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)

def print_section(text):
    """Print a section header."""
    print(f"\n{'─' * 40}")
    print(f"  {text}")
    print(f"{'─' * 40}")

def showcase_analysis():
    """Demonstrate codebase analysis."""
    print_header("🔍 CODEBASE ANALYSIS SHOWCASE")
    
    print("The generator can analyze Python codebases and extract:")
    print("  📁 File structure and organization")
    print("  🏗️  Classes and their methods")
    print("  ⚡ Functions and their signatures")
    print("  📦 Import statements")
    print("  🎯 Main entry points")
    print("  📊 Complexity scores")
    
    print_section("Example Analysis")
    
    # Import the analyzer
    from main import CodebaseAnalyzer
    
    # Analyze the example codebase
    print("Analyzing example_codebase/calculator.py...")
    
    analyzer = CodebaseAnalyzer("example_codebase")
    analysis = analyzer.analyze()
    
    print(f"\n📊 Analysis Results:")
    print(f"  • Files analyzed: {analysis['codebase_info']['total_files']}")
    print(f"  • Classes found: {len(analysis['classes'])}")
    print(f"  • Functions found: {len(analysis['functions'])}")
    print(f"  • Main files: {len(analysis['main_files'])}")
    print(f"  • Complexity score: {analysis['structure']['complexity_score']}")
    
    # Show some classes
    if analysis['classes']:
        print(f"\n🏗️  Key Classes:")
        for class_name, class_info in list(analysis['classes'].items())[:3]:
            methods_count = len(class_info.get('methods', []))
            print(f"  • {class_name}: {methods_count} methods")
    
    return analysis

def showcase_generation(analysis):
    """Demonstrate course generation."""
    print_header("📝 COURSE GENERATION SHOWCASE")
    
    print("The generator creates interactive HTML courses with:")
    print("  📚 5 comprehensive modules")
    print("  🎨 Beautiful responsive design")
    print("  🎮 Interactive quizzes")
    print("  📖 Code ↔ Plain English translations")
    print("  📊 Progress tracking")
    print("  ⌨️  Keyboard navigation")
    
    print_section("Generating Course")
    
    # Import the generator
    from main import CourseGenerator
    
    # Generate course
    output_dir = "showcase_output"
    print(f"Generating course in: {output_dir}")
    
    generator = CourseGenerator(analysis)
    generator.generate(output_dir)
    
    # List generated files
    output_path = Path(output_dir)
    print(f"\n📄 Generated Files:")
    
    total_size = 0
    for file in sorted(output_path.rglob("*")):
        if file.is_file():
            size = file.stat().st_size
            total_size += size
            print(f"  • {file.relative_to(output_path)} ({size:,} bytes)")
    
    print(f"\n📊 Total size: {total_size:,} bytes")
    
    # Show how to view the course
    index_file = output_path / "index.html"
    print(f"\n🌐 To view the course, open in your browser:")
    print(f"   {index_file.absolute()}")
    
    return output_dir

def showcase_features():
    """Demonstrate course features."""
    print_header("✨ INTERACTIVE FEATURES SHOWCASE")
    
    print("The generated course includes:")
    print()
    print("  🎯 Scroll-Based Navigation")
    print("     • Progress bar showing completion")
    print("     • Module dots for quick navigation")
    print("     • Keyboard shortcuts (arrow keys)")
    print("     • Smooth scrolling between sections")
    print()
    print("  📖 Code Translations")
    print("     • Side-by-side code and explanations")
    print("     • Syntax highlighting")
    print("     • Line-by-line translations")
    print("     • Responsive layout")
    print()
    print("  🎮 Interactive Quizzes")
    print("     • Multiple-choice questions")
    print("     • Instant feedback")
    print("     • Progress tracking")
    print("     • Reset functionality")
    print()
    print("  🎨 Visual Elements")
    print("     • Component cards with icons")
    print("     • Architecture diagrams")
    print("     • Data flow visualizations")
    print("     • Callout boxes for insights")
    print()
    print("  📱 Responsive Design")
    print("     • Mobile-friendly layout")
    print("     • Touch-friendly interactions")
    print("     • Adaptive typography")
    print("     • Flexible grid systems")

def showcase_customization():
    """Show customization options."""
    print_header("🎨 CUSTOMIZATION OPTIONS")
    
    print("The course can be customized in several ways:")
    print()
    print("  🎨 Accent Colors")
    print("     • Vermillion (default): #D94F30")
    print("     • Coral: #E06B56")
    print("     • Teal: #2A7B9B")
    print("     • Amber: #D4A843")
    print("     • Forest: #2D8B55")
    print()
    print("  📝 Course Content")
    print("     • Edit HTML files in modules/ directory")
    print("     • Update styles in styles.css")
    print("     • Add interactivity in main.js")
    print("     • Customize quiz questions")
    print()
    print("  ⚙️  Configuration")
    print("     • config.json for settings")
    print("     • Command-line arguments")
    print("     • Environment variables")
    print("     • Streamlit web interface")

def showcase_interfaces():
    """Show available interfaces."""
    print_header("🌐 AVAILABLE INTERFACES")
    
    print("The generator provides multiple ways to use it:")
    print()
    print("  🖥️  Command Line Interface")
    print("     • Quick analysis and generation")
    print("     • Scriptable and automatable")
    print("     • Integration with other tools")
    print()
    print("  🌐 Streamlit Web Interface")
    print("     • Interactive web-based UI")
    print("     • File upload functionality")
    print("     • Real-time preview")
    print("     • Course download options")
    print()
    print("  🐳 Docker Support")
    print("     • Containerized deployment")
    print("     • Docker Compose configuration")
    print("     • Isolated environment")
    print("     • Easy scaling")
    print()
    print("  📦 Makefile")
    print("     • Build automation")
    print("     • Common tasks")
    print("     • Development workflow")
    print("     • Testing and deployment")

def main():
    """Run the showcase."""
    print_header("🚀 SIMPLIFIED CODEBASE-TO-COURSE GENERATOR")
    
    print("Welcome to the project showcase!")
    print("This demonstrates the key features and capabilities.")
    
    try:
        # Run analysis showcase
        analysis = showcase_analysis()
        
        # Run generation showcase
        output_dir = showcase_generation(analysis)
        
        # Run features showcase
        showcase_features()
        
        # Run customization showcase
        showcase_customization()
        
        # Run interfaces showcase
        showcase_interfaces()
        
        print_header("🎉 SHOWCASE COMPLETE!")
        
        print("You've seen the key features of the generator:")
        print("  ✅ Codebase analysis")
        print("  ✅ Course generation")
        print("  ✅ Interactive features")
        print("  ✅ Customization options")
        print("  ✅ Multiple interfaces")
        
        print("\n📖 Next Steps:")
        print("  1. Explore the generated course in your browser")
        print("  2. Try analyzing your own codebase:")
        print("     python main.py /path/to/your/python/project")
        print("  3. Use the Streamlit web interface:")
        print("     streamlit run streamlit_app.py")
        print("  4. Read the documentation:")
        print("     README.md, USAGE.md, PROJECT_SUMMARY.md")
        
        # Clean up
        import shutil
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print(f"\n🧹 Cleaned up: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ Showcase failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
