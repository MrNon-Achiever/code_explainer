#!/usr/bin/env python3
"""
Streamlit Web Interface for Codebase-to-Course Generator

This provides a web-based interface for analyzing Python codebases
and generating interactive HTML courses.
"""

import streamlit as st
import os
import sys
import tempfile
import shutil
from pathlib import Path
import base64

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import CodebaseAnalyzer, CourseGenerator

def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Codebase-to-Course Generator",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #D94F30;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B6560;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #F5F0E8;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #D94F30;
    }
    .stat-box {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(44,42,40,0.08);
    }
    .download-btn {
        background: #D94F30;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">📚 Codebase-to-Course Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform any Python codebase into an interactive HTML course</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Analysis options
        st.subheader("Analysis Options")
        verbose = st.checkbox("Verbose output", value=False, help="Show detailed analysis information")
        
        # Course options
        st.subheader("Course Options")
        course_title = st.text_input("Course title (optional)", help="Custom title for the generated course")
        
        # Accent color
        st.subheader("Accent Color")
        accent_color = st.selectbox(
            "Choose accent color",
            ["Vermillion (default)", "Coral", "Teal", "Amber", "Forest"],
            help="Primary color for the course design"
        )
        
        # Color mapping
        color_map = {
            "Vermillion (default)": "#D94F30",
            "Coral": "#E06B56",
            "Teal": "#2A7B9B",
            "Amber": "#D4A843",
            "Forest": "#2D8B55"
        }
        
        selected_color = color_map[accent_color]
        
        st.markdown("---")
        st.markdown("### 📖 About")
        st.markdown("""
        This tool analyzes Python codebases and generates beautiful, interactive HTML courses.
        
        **Features:**
        - Automatic code analysis
        - Interactive quizzes
        - Code ↔ Plain English translations
        - Beautiful responsive design
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Codebase Input")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["Upload files", "Enter path", "Use example"],
            horizontal=True
        )
        
        codebase_path = None
        uploaded_files = None
        
        if input_method == "Upload files":
            uploaded_files = st.file_uploader(
                "Upload Python files",
                type=["py"],
                accept_multiple_files=True,
                help="Upload one or more Python files to analyze"
            )
            
            if uploaded_files:
                # Save uploaded files to temporary directory
                temp_dir = tempfile.mkdtemp()
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                codebase_path = temp_dir
                
                st.success(f"✅ Uploaded {len(uploaded_files)} files")
        
        elif input_method == "Enter path":
            codebase_path = st.text_input(
                "Enter path to codebase",
                placeholder="/path/to/your/python/project",
                help="Enter the path to a directory containing Python files"
            )
            
            if codebase_path:
                if os.path.exists(codebase_path):
                    st.success(f"✅ Path exists: {codebase_path}")
                else:
                    st.error("❌ Path does not exist")
                    codebase_path = None
        
        else:  # Use example
            st.info("Using the included example calculator codebase")
            codebase_path = "example_codebase"
            
            # Show example code
            example_file = Path("example_codebase/calculator.py")
            if example_file.exists():
                with st.expander("View example code"):
                    st.code(example_file.read_text(), language="python")
        
        # Generate button
        if codebase_path:
            if st.button("🚀 Generate Course", type="primary", use_container_width=True):
                with st.spinner("Analyzing codebase and generating course..."):
                    try:
                        # Create temporary output directory
                        output_dir = tempfile.mkdtemp()
                        
                        # Analyze codebase
                        analyzer = CodebaseAnalyzer(codebase_path)
                        analysis = analyzer.analyze()
                        
                        # Generate course
                        generator = CourseGenerator(analysis)
                        generator.generate(output_dir)
                        
                        # Store results in session state
                        st.session_state.analysis = analysis
                        st.session_state.output_dir = output_dir
                        st.session_state.course_generated = True
                        
                        st.success("✅ Course generated successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating course: {str(e)}")
                        if verbose:
                            st.exception(e)
    
    with col2:
        st.header("📊 Analysis Results")
        
        if 'analysis' in st.session_state:
            analysis = st.session_state.analysis
            
            # Display statistics
            st.subheader("Codebase Statistics")
            
            col_stats1, col_stats2 = st.columns(2)
            
            with col_stats1:
                st.metric("Files", analysis["codebase_info"]["total_files"])
                st.metric("Classes", len(analysis["classes"]))
            
            with col_stats2:
                st.metric("Functions", len(analysis["functions"]))
                st.metric("Complexity", analysis["structure"]["complexity_score"])
            
            # Show main files
            if analysis["main_files"]:
                st.subheader("Main Entry Points")
                for main_file in analysis["main_files"]:
                    st.markdown(f"""
                    <div class="feature-card">
                        <strong>{main_file['file']}</strong><br>
                        <small>{main_file['reason']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show classes
            if analysis["classes"]:
                st.subheader("Key Classes")
                for class_name, class_info in list(analysis["classes"].items())[:5]:
                    methods_count = len(class_info.get("methods", []))
                    st.markdown(f"""
                    <div class="feature-card">
                        <strong>{class_name}</strong><br>
                        <small>{methods_count} methods</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            st.info("Upload or specify a codebase to see analysis results")
    
    # Download section
    if 'course_generated' in st.session_state and st.session_state.course_generated:
        st.markdown("---")
        st.header("📥 Download Course")
        
        output_dir = st.session_state.output_dir
        
        # Show generated files
        st.subheader("Generated Files")
        
        output_path = Path(output_dir)
        files = []
        
        for file in sorted(output_path.rglob("*")):
            if file.is_file():
                size = file.stat().st_size
                files.append({
                    "name": str(file.relative_to(output_path)),
                    "path": str(file),
                    "size": size
                })
        
        # Display files in a table
        if files:
            st.dataframe(
                files,
                column_config={
                    "name": "File Name",
                    "size": st.column_config.NumberColumn("Size (bytes)", format="%d")
                },
                hide_index=True,
                use_container_width=True
            )
        
        # Download buttons
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            # Download index.html
            index_file = output_path / "index.html"
            if index_file.exists():
                with open(index_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                st.download_button(
                    label="📄 Download index.html",
                    data=html_content,
                    file_name="codebase-course.html",
                    mime="text/html",
                    use_container_width=True
                )
        
        with col_dl2:
            # Download as zip
            import zipfile
            import io
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file in files:
                    zip_file.write(file["path"], file["name"])
            
            st.download_button(
                label="📦 Download as ZIP",
                data=zip_buffer.getvalue(),
                file_name="codebase-course.zip",
                mime="application/zip",
                use_container_width=True
            )
        
        # Preview section
        st.subheader("👁️ Preview")
        
        if st.button("Show Course Preview"):
            index_file = output_path / "index.html"
            if index_file.exists():
                with open(index_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
                
                # Display in iframe
                st.components.v1.html(html_content, height=800, scrolling=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B6560; font-size: 0.9rem;">
        <p>Built with ❤️ using Streamlit • Simplified Codebase-to-Course Generator</p>
        <p>Based on the <a href="https://github.com/user/codebase-to-course" target="_blank">Codebase-to-Course</a> skill</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
