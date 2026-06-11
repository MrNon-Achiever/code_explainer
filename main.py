#!/usr/bin/env python3
"""
Simplified Codebase-to-Course Generator

A simplified version of the codebase-to-course skill that analyzes a Python codebase
and generates an interactive HTML course. This is a simplified version that demonstrates
the core concepts of the original skill.

Usage:
    python main.py <path_to_codebase> [output_directory]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast
import re

class CodebaseAnalyzer:
    """Analyzes a Python codebase to extract structure and key components."""
    
    def __init__(self, codebase_path: str):
        self.codebase_path = Path(codebase_path)
        self.modules = {}
        self.classes = {}
        self.functions = {}
        self.imports = []
        self.main_files = []
        
    def analyze(self) -> Dict[str, Any]:
        """Analyze the codebase and return structured information."""
        print(f"🔍 Analyzing codebase: {self.codebase_path}")
        
        # Find Python files
        python_files = list(self.codebase_path.rglob("*.py"))
        print(f"📁 Found {len(python_files)} Python files")
        
        for file_path in python_files:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                print(f"⚠️  Warning: Could not analyze {file_path}: {e}")
        
        # Identify main entry points
        self._identify_main_files()
        
        # Generate analysis summary
        analysis = {
            "codebase_info": {
                "path": str(self.codebase_path),
                "total_files": len(python_files),
                "analyzed_files": len(self.modules)
            },
            "modules": self.modules,
            "classes": self.classes,
            "functions": self.functions,
            "imports": self.imports,
            "main_files": self.main_files,
            "structure": self._generate_structure()
        }
        
        return analysis
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Extract information
            file_info = {
                "path": str(file_path.relative_to(self.codebase_path)),
                "full_path": str(file_path),
                "size": file_path.stat().st_size,
                "lines": len(content.split('\n')),
                "imports": self._extract_imports(tree),
                "classes": self._extract_classes(tree),
                "functions": self._extract_functions(tree),
                "docstring": ast.get_docstring(tree),
                "is_main": self._is_main_file(content, file_path)
            }
            
            # Store module info
            module_name = file_path.stem
            self.modules[module_name] = file_info
            
            # Extract classes and functions for global tracking
            for class_info in file_info["classes"]:
                class_name = class_info["name"]
                self.classes[class_name] = {
                    **class_info,
                    "module": module_name,
                    "file": file_info["path"]
                }
            
            for func_info in file_info["functions"]:
                func_name = func_info["name"]
                self.functions[func_name] = {
                    **func_info,
                    "module": module_name,
                    "file": file_info["path"]
                }
            
            # Track imports
            self.imports.extend(file_info["imports"])
            
            print(f"✅ Analyzed: {file_info['path']}")
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
    
    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract imports from AST."""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "asname": alias.asname
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "type": "from",
                        "module": module,
                        "name": alias.name,
                        "asname": alias.asname
                    })
        
        return imports
    
    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions from AST."""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "lineno": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "methods": [],
                    "bases": [self._get_name(base) for base in node.bases],
                    "decorators": [self._get_name(dec) for dec in node.decorator_list]
                }
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = {
                            "name": item.name,
                            "lineno": item.lineno,
                            "docstring": ast.get_docstring(item),
                            "args": self._extract_function_args(item),
                            "is_private": item.name.startswith('_'),
                            "decorators": [self._get_name(dec) for dec in item.decorator_list]
                        }
                        class_info["methods"].append(method_info)
                
                classes.append(class_info)
        
        return classes
    
    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions from AST."""
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Only top-level functions (not methods)
                if not self._is_method(node, tree):
                    func_info = {
                        "name": node.name,
                        "lineno": node.lineno,
                        "docstring": ast.get_docstring(node),
                        "args": self._extract_function_args(node),
                        "is_private": node.name.startswith('_'),
                        "decorators": [self._get_name(dec) for dec in node.decorator_list],
                        "returns": self._get_annotation(node.returns)
                    }
                    functions.append(func_info)
        
        return functions
    
    def _is_method(self, node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if a function is a method inside a class."""
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef):
                if node in parent.body:
                    return True
        return False
    
    def _extract_function_args(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Extract function arguments."""
        args = []
        
        # Regular arguments
        for arg in node.args.args:
            arg_info = {
                "name": arg.arg,
                "annotation": self._get_annotation(arg.annotation)
            }
            args.append(arg_info)
        
        # *args
        if node.args.vararg:
            args.append({
                "name": f"*{node.args.vararg.arg}",
                "annotation": self._get_annotation(node.args.vararg.annotation)
            })
        
        # **kwargs
        if node.args.kwarg:
            args.append({
                "name": f"**{node.args.kwarg.arg}",
                "annotation": self._get_annotation(node.args.kwarg.annotation)
            })
        
        return args
    
    def _get_annotation(self, node: Optional[ast.AST]) -> Optional[str]:
        """Get string representation of annotation."""
        if node is None:
            return None
        try:
            return ast.dump(node)
        except:
            return str(node)
    
    def _get_name(self, node: ast.AST) -> str:
        """Get name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        else:
            return str(node)
    
    def _is_main_file(self, content: str, file_path: Path) -> bool:
        """Check if file is a main entry point."""
        # Check for if __name__ == "__main__"
        if 'if __name__ == "__main__"' in content:
            return True
        
        # Check for common main function patterns
        main_patterns = [
            'def main():',
            'def main(args):',
            'app = FastAPI()',
            'app = Flask(__name__)',
            'app = Sanic(',
            'app = create_app()'
        ]
        
        for pattern in main_patterns:
            if pattern in content:
                return True
        
        # Check filename
        main_filenames = ['main.py', 'app.py', 'run.py', 'server.py', 'manage.py']
        if file_path.name in main_filenames:
            return True
        
        return False
    
    def _identify_main_files(self):
        """Identify main entry point files."""
        for module_name, module_info in self.modules.items():
            if module_info["is_main"]:
                self.main_files.append({
                    "module": module_name,
                    "file": module_info["path"],
                    "reason": self._get_main_reason(module_info)
                })
    
    def _get_main_reason(self, module_info: Dict[str, Any]) -> str:
        """Get reason why file is considered main."""
        content = Path(module_info["full_path"]).read_text()
        
        if 'if __name__ == "__main__"' in content:
            return "Contains `if __name__ == '__main__'` block"
        
        if 'def main(' in content:
            return "Contains `main()` function"
        
        if 'app = FastAPI()' in content:
            return "FastAPI application entry point"
        
        if 'app = Flask(__name__)' in content:
            return "Flask application entry point"
        
        if module_info["path"].endswith('app.py'):
            return "Application entry point file"
        
        return "Main entry point"
    
    def _generate_structure(self) -> Dict[str, Any]:
        """Generate codebase structure overview."""
        structure = {
            "directories": {},
            "file_types": {},
            "complexity_score": 0
        }
        
        # Count directories
        for module_name, module_info in self.modules.items():
            file_path = Path(module_info["path"])
            directory = str(file_path.parent)
            if directory not in structure["directories"]:
                structure["directories"][directory] = 0
            structure["directories"][directory] += 1
            
            # Count file types
            file_type = file_path.suffix
            if file_type not in structure["file_types"]:
                structure["file_types"][file_type] = 0
            structure["file_types"][file_type] += 1
        
        # Calculate complexity score (simple heuristic)
        total_lines = sum(module["lines"] for module in self.modules.values())
        total_classes = len(self.classes)
        total_functions = len(self.functions)
        
        structure["complexity_score"] = min(100, 
            total_lines // 10 + 
            total_classes * 5 + 
            total_functions * 2
        )
        
        return structure


class CourseGenerator:
    """Generates HTML course from codebase analysis."""
    
    def __init__(self, analysis: Dict[str, Any]):
        self.analysis = analysis
        
    def generate(self, output_dir: str):
        """Generate the complete course."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📝 Generating course in: {output_path}")
        
        # Generate course structure
        self._generate_structure_files(output_path)
        self._generate_modules(output_path)
        self._generate_index(output_path)
        
        print(f"✅ Course generated successfully!")
        print(f"📂 Open {output_path / 'index.html'} in your browser")
    
    def _generate_structure_files(self, output_path: Path):
        """Generate CSS, JS, and base files."""
        # Create CSS file (simplified version)
        css_content = self._generate_css()
        (output_path / "styles.css").write_text(css_content)
        
        # Create JS file (simplified version)
        js_content = self._generate_js()
        (output_path / "main.js").write_text(js_content)
        
        # Create base HTML
        base_html = self._generate_base_html()
        (output_path / "_base.html").write_text(base_html)
        
        # Create footer HTML
        footer_html = self._generate_footer_html()
        (output_path / "_footer.html").write_text(footer_html)
        
        # Create build script
        build_sh = self._generate_build_script()
        (output_path / "build.sh").write_text(build_sh)
        
        print("📁 Generated structure files")
    
    def _generate_modules(self, output_path: Path):
        """Generate module HTML files."""
        modules_dir = output_path / "modules"
        modules_dir.mkdir(exist_ok=True)
        
        # Generate intro module
        self._generate_intro_module(modules_dir)
        
        # Generate architecture module
        self._generate_architecture_module(modules_dir)
        
        # Generate components module
        self._generate_components_module(modules_dir)
        
        # Generate data flow module
        self._generate_data_flow_module(modules_dir)
        
        # Generate interactive module
        self._generate_interactive_module(modules_dir)
        
        print("📚 Generated course modules")
    
    def _generate_index(self, output_path: Path):
        """Generate index.html by assembling parts."""
        build_sh_content = (output_path / "build.sh").read_text()
        
        # Create a simple build script that works on all platforms
        build_script = """#!/bin/bash
# Assembles the course from parts
set -e
cat _base.html modules/*.html _footer.html > index.html
echo "Built index.html — open it in your browser."
"""
        
        (output_path / "build.sh").write_text(build_script)
        
        # Assemble the HTML
        base_html = (output_path / "_base.html").read_text()
        footer_html = (output_path / "_footer.html").read_text()
        
        # Read all module files
        modules_dir = output_path / "modules"
        module_files = sorted(modules_dir.glob("*.html"))
        
        modules_html = ""
        for module_file in module_files:
            modules_html += module_file.read_text() + "\n"
        
        # Combine everything
        index_html = base_html + modules_html + footer_html
        (output_path / "index.html").write_text(index_html)
        
        print("📄 Generated index.html")
    
    def _generate_css(self) -> str:
        """Generate simplified CSS."""
        return """
/* Simplified Codebase-to-Course Styles */
:root {
  --color-bg: #FAF7F2;
  --color-bg-warm: #F5F0E8;
  --color-bg-code: #1E1E2E;
  --color-text: #2C2A28;
  --color-text-secondary: #6B6560;
  --color-accent: #D94F30;
  --color-accent-hover: #C4432A;
  --color-accent-light: #FDEEE9;
  --color-border: #E5DFD6;
  --color-surface: #FFFFFF;
  --font-display: 'Bricolage Grotesque', Georgia, serif;
  --font-body: 'DM Sans', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-2xl: 1.5rem;
  --text-4xl: 2.25rem;
  --space-4: 1rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --radius-md: 12px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-text);
  line-height: 1.6;
  background: var(--color-bg);
}

.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 50px;
  background: rgba(250,247,242,0.92);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-border);
  z-index: 1000;
}

.nav-inner {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 var(--space-8);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 600;
}

.nav-dots {
  display: flex;
  gap: var(--space-4);
}

.nav-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid var(--color-accent);
  background: transparent;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-dot:hover {
  background: var(--color-accent-light);
}

.nav-dot.active {
  background: var(--color-accent);
}

.module {
  min-height: 100vh;
  padding: var(--space-12) var(--space-8);
  padding-top: calc(50px + var(--space-12));
  scroll-snap-align: start;
}

.module:nth-child(even) {
  background: var(--color-bg-warm);
}

.module-content {
  max-width: 800px;
  margin: 0 auto;
}

.module-header {
  margin-bottom: var(--space-12);
}

.module-number {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: 800;
  color: var(--color-accent);
  opacity: 0.15;
  line-height: 1;
}

.module-title {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: 700;
  margin-top: var(--space-4);
}

.module-subtitle {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  margin-top: var(--space-4);
}

.screen {
  margin-bottom: var(--space-12);
}

.screen-heading {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 600;
  margin-bottom: var(--space-8);
}

.translation-block {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(44,42,40,0.08);
  margin: var(--space-8) 0;
}

.translation-code {
  background: var(--color-bg-code);
  color: #CDD6F4;
  padding: var(--space-8);
  font-family: var(--font-mono);
  font-size: 0.875rem;
  line-height: 1.7;
}

.translation-english {
  background: var(--color-surface);
  padding: var(--space-8);
  font-size: 0.875rem;
  line-height: 1.7;
  border-left: 3px solid var(--color-accent);
}

.translation-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.5;
  margin-bottom: var(--space-4);
}

.quiz-container {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-8);
  box-shadow: 0 4px 12px rgba(44,42,40,0.08);
  margin: var(--space-8) 0;
}

.quiz-question {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 600;
  margin-bottom: var(--space-8);
}

.quiz-options {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.quiz-option {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  cursor: pointer;
  transition: all 0.3s;
}

.quiz-option:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

.quiz-option.selected {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

.quiz-option.correct {
  border-color: #2D8B55;
  background: #E8F5EE;
}

.quiz-option.incorrect {
  border-color: #C93B3B;
  background: #FDE8E8;
}

.quiz-feedback {
  margin-top: var(--space-4);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  display: none;
}

.quiz-feedback.show {
  display: block;
}

.quiz-feedback.success {
  background: #E8F5EE;
  color: #2D8B55;
}

.quiz-feedback.error {
  background: #FDE8E8;
  color: #C93B3B;
}

.pattern-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-8);
  margin: var(--space-8) 0;
}

.pattern-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-8);
  box-shadow: 0 4px 12px rgba(44,42,40,0.08);
  transition: transform 0.3s;
}

.pattern-card:hover {
  transform: translateY(-4px);
}

.pattern-icon {
  font-size: 2rem;
  margin-bottom: var(--space-4);
}

.pattern-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: var(--space-4);
}

.pattern-desc {
  color: var(--color-text-secondary);
}

.callout {
  display: flex;
  gap: var(--space-8);
  padding: var(--space-8);
  border-radius: var(--radius-md);
  margin: var(--space-8) 0;
  border-left: 4px solid var(--color-accent);
  background: var(--color-accent-light);
}

.callout-icon {
  font-size: 1.5rem;
}

.callout-title {
  font-weight: 700;
  margin-bottom: var(--space-4);
}

.callout-content {
  color: var(--color-text-secondary);
}

.animate-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s cubic-bezier(0.16,1,0.3,1), 
              transform 0.5s cubic-bezier(0.16,1,0.3,1);
}

.animate-in.visible {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 768px) {
  .translation-block {
    grid-template-columns: 1fr;
  }
  
  .translation-english {
    border-left: none;
    border-top: 3px solid var(--color-accent);
  }
}
"""
    
    def _generate_js(self) -> str:
        """Generate simplified JavaScript."""
        return """
/**
 * Simplified Codebase-to-Course JavaScript
 */
(function() {
  'use strict';
  
  // Navigation
  const progressBar = document.getElementById('progress-bar');
  const navDots = document.querySelectorAll('.nav-dot');
  const modules = document.querySelectorAll('.module');
  
  function updateProgress() {
    if (!progressBar) return;
    const scrollTop = window.scrollY;
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    progressBar.style.width = pct + '%';
    updateNavDots();
  }
  
  function updateNavDots() {
    const scrollMid = window.scrollY + window.innerHeight / 2;
    modules.forEach((mod, i) => {
      const dot = navDots[i];
      if (!dot) return;
      const top = mod.offsetTop;
      const bottom = top + mod.offsetHeight;
      if (scrollMid >= top && scrollMid < bottom) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
  }
  
  window.addEventListener('scroll', () => requestAnimationFrame(updateProgress), { passive: true });
  updateProgress();
  
  // Nav dot click
  navDots.forEach(dot => {
    dot.addEventListener('click', () => {
      const target = document.getElementById(dot.dataset.target);
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });
  
  // Keyboard navigation
  document.addEventListener('keydown', e => {
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;
    
    function currentModuleIndex() {
      const scrollMid = window.scrollY + window.innerHeight / 2;
      for (let i = 0; i < modules.length; i++) {
        const top = modules[i].offsetTop;
        const bottom = top + modules[i].offsetHeight;
        if (scrollMid >= top && scrollMid < bottom) return i;
      }
      return 0;
    }
    
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
      const next = modules[currentModuleIndex() + 1];
      if (next) { next.scrollIntoView({ behavior: 'smooth' }); e.preventDefault(); }
    }
    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
      const prev = modules[currentModuleIndex() - 1];
      if (prev) { prev.scrollIntoView({ behavior: 'smooth' }); e.preventDefault(); }
    }
  });
  
  // Scroll animations
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  
  document.querySelectorAll('.animate-in').forEach(el => observer.observe(el));
  
  // Quiz functionality
  window.selectOption = function(btn) {
    const block = btn.closest('.quiz-question-block');
    block.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
    btn.classList.add('selected');
  };
  
  window.checkQuiz = function(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.querySelectorAll('.quiz-question-block').forEach(q => {
      const selected = q.querySelector('.quiz-option.selected');
      const feedback = q.querySelector('.quiz-feedback');
      const correct = q.dataset.correct;
      
      if (!selected) {
        feedback.textContent = 'Pick an answer first!';
        feedback.className = 'quiz-feedback show warning';
        return;
      }
      
      q.querySelectorAll('.quiz-option').forEach(o => o.disabled = true);
      
      if (selected.dataset.value === correct) {
        selected.classList.add('correct');
        feedback.innerHTML = '<strong>Exactly!</strong> ' + (q.dataset.explanationRight || '');
        feedback.className = 'quiz-feedback show success';
      } else {
        selected.classList.add('incorrect');
        const correctBtn = q.querySelector(`.quiz-option[data-value="${correct}"]`);
        if (correctBtn) correctBtn.classList.add('correct');
        feedback.innerHTML = '<strong>Not quite.</strong> ' + (q.dataset.explanationWrong || '');
        feedback.className = 'quiz-feedback show error';
      }
    });
  };
  
  window.resetQuiz = function(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.querySelectorAll('.quiz-option').forEach(o => {
      o.classList.remove('selected', 'correct', 'incorrect');
      o.disabled = false;
    });
    
    container.querySelectorAll('.quiz-feedback').forEach(f => {
      f.className = 'quiz-feedback';
      f.textContent = '';
    });
  };
})();
"""
    
    def _generate_base_html(self) -> str:
        """Generate base HTML template."""
        codebase_info = self.analysis["codebase_info"]
        course_title = f"Codebase Course: {codebase_info['path'].split('/')[-1]}"
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{course_title}</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400;1,9..40,500&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="styles.css">
  
  <style>
    :root {{
      --color-accent: #D94F30;
      --color-accent-hover: #C4432A;
      --color-accent-light: #FDEEE9;
      --color-accent-muted: #E8836C;
    }}
  </style>
  
  <script src="main.js" defer></script>
</head>
<body>

  <nav class="nav" id="nav">
    <div class="progress-bar" id="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
    <div class="nav-inner">
      <span class="nav-title">{course_title}</span>
      <div class="nav-dots" id="nav-dots" role="tablist">
        <button class="nav-dot" data-target="module-1" data-tooltip="Introduction" role="tab" aria-label="Module 1: Introduction"></button>
        <button class="nav-dot" data-target="module-2" data-tooltip="Architecture" role="tab" aria-label="Module 2: Architecture"></button>
        <button class="nav-dot" data-target="module-3" data-tooltip="Components" role="tab" aria-label="Module 3: Components"></button>
        <button class="nav-dot" data-target="module-4" data-tooltip="Data Flow" role="tab" aria-label="Module 4: Data Flow"></button>
        <button class="nav-dot" data-target="module-5" data-tooltip="Interactive" role="tab" aria-label="Module 5: Interactive"></button>
      </div>
    </div>
  </nav>

  <main id="main">
"""
    
    def _generate_footer_html(self) -> str:
        """Generate footer HTML."""
        return """  </main>

</body>
</html>
"""
    
    def _generate_build_script(self) -> str:
        """Generate build script."""
        return """#!/bin/bash
# Assembles the course from parts.
# Run from the course directory: bash build.sh
set -e
cat _base.html modules/*.html _footer.html > index.html
echo "Built index.html — open it in your browser."
"""
    
    def _generate_intro_module(self, modules_dir: Path):
        """Generate introduction module."""
        codebase_info = self.analysis["codebase_info"]
        structure = self.analysis["structure"]
        
        html = f"""
<section class="module" id="module-1" style="background: var(--color-bg)">
  <div class="module-content">
    <header class="module-header animate-in">
      <span class="module-number">01</span>
      <h1 class="module-title">Welcome to the Codebase</h1>
      <p class="module-subtitle">Understanding what this project does and how it's structured</p>
    </header>

    <div class="module-body">
      <section class="screen animate-in">
        <h2 class="screen-heading">What is this project?</h2>
        <p>This is an interactive course about the codebase located at <strong>{codebase_info['path']}</strong>.</p>
        <p>The project contains <strong>{codebase_info['total_files']}</strong> Python files with a complexity score of <strong>{structure['complexity_score']}</strong>.</p>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Project Structure</h2>
        <div class="translation-block">
          <div class="translation-code">
            <span class="translation-label">CODE</span>
            <pre><code>
# Main entry points
{self._format_main_files()}

# Directory structure
{self._format_directory_structure()}
            </code></pre>
          </div>
          <div class="translation-english">
            <span class="translation-label">PLAIN ENGLISH</span>
            <div class="translation-lines">
              <p class="tl">Here are the main files that start the application...</p>
              <p class="tl">The code is organized into {len(structure['directories'])} directories...</p>
            </div>
          </div>
        </div>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Key Statistics</h2>
        <div class="pattern-cards">
          <div class="pattern-card">
            <div class="pattern-icon">📁</div>
            <h4 class="pattern-title">Files</h4>
            <p class="pattern-desc">{codebase_info['total_files']} Python files analyzed</p>
          </div>
          <div class="pattern-card">
            <div class="pattern-icon">🏗️</div>
            <h4 class="pattern-title">Classes</h4>
            <p class="pattern-desc">{len(self.analysis['classes'])} classes defined</p>
          </div>
          <div class="pattern-card">
            <div class="pattern-icon">⚡</div>
            <h4 class="pattern-title">Functions</h4>
            <p class="pattern-desc">{len(self.analysis['functions'])} functions defined</p>
          </div>
          <div class="pattern-card">
            <div class="pattern-icon">📊</div>
            <h4 class="pattern-title">Complexity</h4>
            <p class="pattern-desc">Score: {structure['complexity_score']}/100</p>
          </div>
        </div>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Quick Quiz</h2>
        <div class="quiz-container" id="quiz-intro">
          <div class="quiz-question-block" data-correct="option-b" data-explanation-right="Exactly! Understanding the structure helps you navigate and modify the code effectively." data-explanation-wrong="Not quite. Think about why you'd want to know how files are organized...">
            <h3 class="quiz-question">Why is it important to understand the project structure?</h3>
            <div class="quiz-options">
              <button class="quiz-option" data-value="option-a" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>To memorize file names for no reason</span>
              </button>
              <button class="quiz-option" data-value="option-b" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>To know where to find and modify code effectively</span>
              </button>
              <button class="quiz-option" data-value="option-c" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>To impress other developers with your knowledge</span>
              </button>
            </div>
            <div class="quiz-feedback"></div>
          </div>
          
          <button class="quiz-check-btn" onclick="checkQuiz('quiz-intro')">Check Answer</button>
          <button class="quiz-reset-btn" onclick="resetQuiz('quiz-intro')">Try Again</button>
        </div>
      </section>
    </div>
  </div>
</section>
"""
        (modules_dir / "01-introduction.html").write_text(html)
    
    def _generate_architecture_module(self, modules_dir: Path):
        """Generate architecture module."""
        classes = self.analysis["classes"]
        
        # Get top 5 classes by method count
        top_classes = sorted(classes.items(), key=lambda x: len(x[1].get("methods", [])), reverse=True)[:5]
        
        class_cards = ""
        for class_name, class_info in top_classes:
            methods_count = len(class_info.get("methods", []))
            class_cards += f"""
              <div class="pattern-card">
                <div class="pattern-icon">🏗️</div>
                <h4 class="pattern-title">{class_name}</h4>
                <p class="pattern-desc">{methods_count} methods defined</p>
              </div>
"""
        
        html = f"""
<section class="module" id="module-2" style="background: var(--color-bg-warm)">
  <div class="module-content">
    <header class="module-header animate-in">
      <span class="module-number">02</span>
      <h1 class="module-title">Architecture Overview</h1>
      <p class="module-subtitle">Understanding how the codebase is organized and structured</p>
    </header>

    <div class="module-body">
      <section class="screen animate-in">
        <h2 class="screen-heading">Main Components</h2>
        <p>This codebase has <strong>{len(classes)}</strong> classes that form the backbone of the application.</p>
        
        <div class="pattern-cards">
          {class_cards}
        </div>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Code Structure</h2>
        <div class="callout">
          <div class="callout-icon">💡</div>
          <div class="callout-content">
            <strong class="callout-title">Key Insight</strong>
            <p>The architecture follows a modular pattern where each class has specific responsibilities, making the code easier to understand and maintain.</p>
          </div>
        </div>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Quiz: Architecture</h2>
        <div class="quiz-container" id="quiz-architecture">
          <div class="quiz-question-block" data-correct="option-a" data-explanation-right="Correct! Modular architecture makes code easier to maintain and understand." data-explanation-wrong="Not quite. Think about what makes code easier to work with over time...">
            <h3 class="quiz-question">What is the main benefit of the modular architecture shown here?</h3>
            <div class="quiz-options">
              <button class="quiz-option" data-value="option-a" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>Easier maintenance and understanding of code</span>
              </button>
              <button class="quiz-option" data-value="option-b" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>Making the code look more complex</span>
              </button>
              <button class="quiz-option" data-value="option-c" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>Adding more files to the project</span>
              </button>
            </div>
            <div class="quiz-feedback"></div>
          </div>
          
          <button class="quiz-check-btn" onclick="checkQuiz('quiz-architecture')">Check Answer</button>
          <button class="quiz-reset-btn" onclick="resetQuiz('quiz-architecture')">Try Again</button>
        </div>
      </section>
    </div>
  </div>
</section>
"""
        (modules_dir / "02-architecture.html").write_text(html)
    
    def _generate_components_module(self, modules_dir: Path):
        """Generate components module."""
        classes = self.analysis["classes"]
        
        # Get some classes to showcase
        showcase_classes = list(classes.items())[:3]
        
        class_examples = ""
        for class_name, class_info in showcase_classes:
            methods = class_info.get("methods", [])[:3]  # First 3 methods
            method_list = ", ".join([m["name"] for m in methods])
            
            class_examples += f"""
              <div class="callout">
                <div class="callout-icon">🏗️</div>
                <div class="callout-content">
                  <strong class="callout-title">{class_name}</strong>
                  <p>Methods: {method_list}</p>
                </div>
              </div>
"""
        
        html = f"""
<section class="module" id="module-3" style="background: var(--color-bg)">
  <div class="module-content">
    <header class="module-header animate-in">
      <span class="module-number">03</span>
      <h1 class="module-title">Key Components</h1>
      <p class="module-subtitle">Understanding the main classes and their responsibilities</p>
    </header>

    <div class="module-body">
      <section class="screen animate-in">
        <h2 class="screen-heading">Component Deep Dive</h2>
        <p>Let's examine some of the key components in this codebase:</p>
        
        {class_examples}
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">How Components Interact</h2>
        <div class="translation-block">
          <div class="translation-code">
            <span class="translation-label">CODE</span>
            <pre><code>
# Example interaction pattern
{self._generate_interaction_example()}
            </code></pre>
          </div>
          <div class="translation-english">
            <span class="translation-label">PLAIN ENGLISH</span>
            <div class="translation-lines">
              <p class="tl">Components often work together to accomplish tasks...</p>
              <p class="tl">One component creates or uses another component...</p>
              <p class="tl">This creates a flow of data through the system...</p>
            </div>
          </div>
        </div>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Quiz: Components</h2>
        <div class="quiz-container" id="quiz-components">
          <div class="quiz-question-block" data-correct="option-c" data-explanation-right="Exactly! Understanding component responsibilities helps you know where to make changes." data-explanation-wrong="Not quite. Think about what helps you navigate a codebase...">
            <h3 class="quiz-question">When you need to modify a specific feature, why is it helpful to know which component handles it?</h3>
            <div class="quiz-options">
              <button class="quiz-option" data-value="option-a" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>So you can delete all other files</span>
              </button>
              <button class="quiz-option" data-value="option-b" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>So you can add random code everywhere</span>
              </button>
              <button class="quiz-option" data-value="option-c" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>So you can make targeted changes without breaking other parts</span>
              </button>
            </div>
            <div class="quiz-feedback"></div>
          </div>
          
          <button class="quiz-check-btn" onclick="checkQuiz('quiz-components')">Check Answer</button>
          <button class="quiz-reset-btn" onclick="resetQuiz('quiz-components')">Try Again</button>
        </div>
      </section>
    </div>
  </div>
</section>
"""
        (modules_dir / "03-components.html").write_text(html)
    
    def _generate_data_flow_module(self, modules_dir: Path):
        """Generate data flow module."""
        html = f"""
<section class="module" id="module-4" style="background: var(--color-bg-warm)">
  <div class="module-content">
    <header class="module-header animate-in">
      <span class="module-number">04</span>
      <h1 class="module-title">Data Flow</h1>
      <p class="module-subtitle">Understanding how data moves through the system</p>
    </header>

    <div class="module-body">
      <section class="screen animate-in">
        <h2 class="screen-heading">How Data Moves</h2>
        <p>In most applications, data flows through several stages before reaching the user. Here's a simplified example:</p>
        
        <div class="callout">
          <div class="callout-icon">🔄</div>
          <div class="callout-content">
            <strong class="callout-title">Data Flow Pattern</strong>
            <p>Data typically flows from input → processing → storage → output, with each stage handled by different components.</p>
          </div>
        </div>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Example: Request Processing</h2>
        <div class="translation-block">
          <div class="translation-code">
            <span class="translation-label">CODE</span>
            <pre><code>
# Typical request handling pattern
def handle_request(request):
    # 1. Parse the incoming data
    data = parse_request(request)
    
    # 2. Process the data
    result = process_data(data)
    
    # 3. Store if needed
    if should_store(result):
        store_data(result)
    
    # 4. Return response
    return create_response(result)
            </code></pre>
          </div>
          <div class="translation-english">
            <span class="translation-label">PLAIN ENGLISH</span>
            <div class="translation-lines">
              <p class="tl">This function handles incoming requests...</p>
              <p class="tl">First, it extracts the useful information from the request...</p>
              <p class="tl">Then it does something useful with that data...</p>
              <p class="tl">If needed, it saves the result for later...</p>
              <p class="tl">Finally, it sends back a response to whoever asked...</p>
            </div>
          </div>
        </div>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Quiz: Data Flow</h2>
        <div class="quiz-container" id="quiz-dataflow">
          <div class="quiz-question-block" data-correct="option-b" data-explanation-right="Correct! Understanding data flow helps you track down issues and add new features." data-explanation-wrong="Not quite. Think about what helps you debug problems...">
            <h3 class="quiz-question">Why is it important to understand how data flows through your application?</h3>
            <div class="quiz-options">
              <button class="quiz-option" data-value="option-a" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>To make the code more complicated</span>
              </button>
              <button class="quiz-option" data-value="option-b" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>To track down issues and add new features effectively</span>
              </button>
              <button class="quiz-option" data-value="option-c" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>To confuse other developers</span>
              </button>
            </div>
            <div class="quiz-feedback"></div>
          </div>
          
          <button class="quiz-check-btn" onclick="checkQuiz('quiz-dataflow')">Check Answer</button>
          <button class="quiz-reset-btn" onclick="resetQuiz('quiz-dataflow')">Try Again</button>
        </div>
      </section>
    </div>
  </div>
</section>
"""
        (modules_dir / "04-data-flow.html").write_text(html)
    
    def _generate_interactive_module(self, modules_dir: Path):
        """Generate interactive module."""
        functions = self.analysis["functions"]
        
        # Get some functions to showcase
        showcase_functions = list(functions.items())[:3]
        
        function_examples = ""
        for func_name, func_info in showcase_functions:
            args = func_info.get("args", [])
            arg_list = ", ".join([a["name"] for a in args])
            
            function_examples += f"""
              <div class="callout">
                <div class="callout-icon">⚡</div>
                <div class="callout-content">
                  <strong class="callout-title">{func_name}({arg_list})</strong>
                  <p>{func_info.get('docstring', 'No description available.')}</p>
                </div>
              </div>
"""
        
        html = f"""
<section class="module" id="module-5" style="background: var(--color-bg)">
  <div class="module-content">
    <header class="module-header animate-in">
      <span class="module-number">05</span>
      <h1 class="module-title">Interactive Elements</h1>
      <p class="module-subtitle">Exploring key functions and their usage</p>
    </header>

    <div class="module-body">
      <section class="screen animate-in">
        <h2 class="screen-heading">Key Functions</h2>
        <p>This codebase contains <strong>{len(functions)}</strong> functions. Here are some important ones:</p>
        
        {function_examples}
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Function Example</h2>
        <div class="translation-block">
          <div class="translation-code">
            <span class="translation-label">CODE</span>
            <pre><code>
# Example function implementation
def process_data(input_data, options=None):
    \"\"\"
    Process input data with optional configuration.
    
    Args:
        input_data: The data to process
        options: Optional configuration dictionary
    
    Returns:
        Processed data result
    \"\"\"
    if options is None:
        options = {{}}
    
    # Apply processing logic
    result = apply_processing(input_data, options)
    
    return result
            </code></pre>
          </div>
          <div class="translation-english">
            <span class="translation-label">PLAIN ENGLISH</span>
            <div class="translation-lines">
              <p class="tl">This function takes data and optional settings...</p>
              <p class="tl">If no settings are provided, use empty defaults...</p>
              <p class="tl">It applies some processing to the data...</p>
              <p class="tl">Finally, it returns the processed result...</p>
            </div>
          </div>
        </div>
      </section>

      <section class="screen animate-in">
        <h2 class="screen-heading">Final Quiz</h2>
        <div class="quiz-container" id="quiz-final">
          <div class="quiz-question-block" data-correct="option-a" data-explanation-right="Excellent! You now have a good understanding of this codebase." data-explanation-wrong="Not quite. Review what you've learned in this course...">
            <h3 class="quiz-question">Based on this course, what's the most important skill for working with codebases?</h3>
            <div class="quiz-options">
              <button class="quiz-option" data-value="option-a" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>Understanding structure, components, and data flow</span>
              </button>
              <button class="quiz-option" data-value="option-b" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>Memorizing every line of code</span>
              </button>
              <button class="quiz-option" data-value="option-c" onclick="selectOption(this)">
                <div class="quiz-option-radio"></div>
                <span>Ignoring the architecture completely</span>
              </button>
            </div>
            <div class="quiz-feedback"></div>
          </div>
          
          <button class="quiz-check-btn" onclick="checkQuiz('quiz-final')">Check Answer</button>
          <button class="quiz-reset-btn" onclick="resetQuiz('quiz-final')">Try Again</button>
        </div>
      </section>
    </div>
  </div>
</section>
"""
        (modules_dir / "05-interactive.html").write_text(html)
    
    def _format_main_files(self) -> str:
        """Format main files for display."""
        main_files = self.analysis["main_files"]
        if not main_files:
            return "# No main entry points found"
        
        lines = []
        for main_file in main_files[:3]:  # Show first 3
            lines.append(f"# {main_file['file']} - {main_file['reason']}")
        
        return "\n".join(lines)
    
    def _format_directory_structure(self) -> str:
        """Format directory structure for display."""
        structure = self.analysis["structure"]
        directories = structure["directories"]
        
        if not directories:
            return "# Single directory structure"
        
        lines = []
        for directory, count in sorted(directories.items())[:5]:  # Show first 5
            lines.append(f"# {directory}/ ({count} files)")
        
        return "\n".join(lines)
    
    def _generate_interaction_example(self) -> str:
        """Generate example of component interaction."""
        classes = list(self.analysis["classes"].items())[:2]
        
        if len(classes) < 2:
            return """
# Simple interaction example
class ServiceA:
    def do_something(self):
        return "Result from A"

class ServiceB:
    def __init__(self, service_a):
        self.service_a = service_a
    
    def process(self):
        result = self.service_a.do_something()
        return f"Processed: {result}"
"""
        
        class1_name, class1_info = classes[0]
        class2_name, class2_info = classes[1]
        
        method1 = class1_info["methods"][0]["name"] if class1_info["methods"] else "do_something"
        method2 = class2_info["methods"][0]["name"] if class2_info["methods"] else "process"
        
        return f"""
# Example interaction between {class1_name} and {class2_name}
class {class1_name}:
    def {method1}(self):
        # Does something useful
        return "Result"

class {class2_name}:
    def __init__(self, {class1_name.lower()}):
        self.{class1_name.lower()} = {class1_name.lower()}
    
    def {method2}(self):
        # Uses {class1_name} to do work
        result = self.{class1_name.lower()}.{method1}()
        return f"Processed: {{result}}"
"""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Simplified Codebase-to-Course Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py ./my_project
  python main.py ./my_project ./output_course
  python main.py /path/to/codebase
        """
    )
    
    parser.add_argument(
        "codebase_path",
        help="Path to the codebase to analyze"
    )
    
    parser.add_argument(
        "output_directory",
        nargs="?",
        default="./course-output",
        help="Output directory for the generated course (default: ./course-output)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input path
    codebase_path = Path(args.codebase_path)
    if not codebase_path.exists():
        print(f"❌ Error: Codebase path does not exist: {codebase_path}")
        sys.exit(1)
    
    if not codebase_path.is_dir():
        print(f"❌ Error: Path is not a directory: {codebase_path}")
        sys.exit(1)
    
    try:
        # Analyze codebase
        print("🚀 Starting codebase analysis...")
        analyzer = CodebaseAnalyzer(str(codebase_path))
        analysis = analyzer.analyze()
        
        # Generate course
        print("\n📝 Generating course...")
        generator = CourseGenerator(analysis)
        generator.generate(args.output_directory)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 Course Generation Summary")
        print("="*60)
        print(f"📁 Codebase: {analysis['codebase_info']['path']}")
        print(f"📄 Files analyzed: {analysis['codebase_info']['total_files']}")
        print(f"🏗️  Classes found: {len(analysis['classes'])}")
        print(f"⚡ Functions found: {len(analysis['functions'])}")
        print(f"📂 Output: {args.output_directory}")
        print(f"🌐 Open {Path(args.output_directory) / 'index.html'} in your browser")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during course generation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
