# Makefile for Simplified Codebase-to-Course Generator

.PHONY: help install test demo run streamlit docker clean

# Default target
help:
	@echo "🚀 Simplified Codebase-to-Course Generator"
	@echo "=========================================="
	@echo ""
	@echo "Available targets:"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run tests"
	@echo "  demo         - Run demo with example codebase"
	@echo "  run          - Run CLI with example codebase"
	@echo "  streamlit    - Run Streamlit web interface"
	@echo "  docker       - Build and run with Docker"
	@echo "  docker-clean - Clean Docker resources"
	@echo "  clean        - Clean generated files"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make demo"
	@echo "  make run CODEBASE=./your-project"
	@echo "  make streamlit"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Run tests
test:
	@echo "🧪 Running tests..."
	python test_generator.py
	@echo "✅ Tests completed"

# Run demo
demo:
	@echo "🎮 Running demo..."
	python demo.py
	@echo "✅ Demo completed"

# Run CLI with example codebase
run:
	@echo "🚀 Running generator with example codebase..."
	python main.py example_codebase ./course-output
	@echo "✅ Generation completed"
	@echo "📂 Output: ./course-output/index.html"

# Run with custom codebase
run-custom:
	@echo "🚀 Running generator with custom codebase..."
	python main.py $(CODEBASE) $(OUTPUT)
	@echo "✅ Generation completed"

# Run Streamlit interface
streamlit:
	@echo "🌐 Starting Streamlit interface..."
	streamlit run streamlit_app.py
	@echo "✅ Streamlit started"

# Docker commands
docker:
	@echo "🐳 Building Docker image..."
	docker build -t codebase-to-course .
	@echo "✅ Docker image built"
	@echo "🚀 Running with Docker..."
	docker run -v $(PWD)/your-project:/app/input -v $(PWD)/output:/app/output codebase-to-course python main.py /app/input /app/output

# Docker Streamlit
docker-streamlit:
	@echo "🐳 Building Docker image..."
	docker build -t codebase-to-course .
	@echo "✅ Docker image built"
	@echo "🌐 Starting Streamlit with Docker..."
	docker run -p 8501:8501 -v $(PWD)/your-project:/app/input codebase-to-course streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0

# Docker Compose
docker-compose:
	@echo "🐳 Running with Docker Compose..."
	docker-compose up

# Docker cleanup
docker-clean:
	@echo "🧹 Cleaning Docker resources..."
	docker-compose down --rmi all --volumes --remove-orphans
	docker system prune -f
	@echo "✅ Docker resources cleaned"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	rm -rf course-output
	rm -rf example_course_output
	rm -rf demo_course_output
	rm -rf output
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	@echo "✅ Cleanup completed"

# Build and open course
open:
	@echo "🌐 Opening course in browser..."
	@if [ -f "./course-output/index.html" ]; then \
		open ./course-output/index.html; \
	else \
		echo "❌ Course not found. Run 'make run' first"; \
	fi

# Lint code (if tools available)
lint:
	@echo "🔍 Linting code..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 main.py streamlit_app.py test_generator.py demo.py; \
	else \
		echo "⚠️  flake8 not found. Install with: pip install flake8"; \
	fi

# Format code (if tools available)
format:
	@echo "🎨 Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black main.py streamlit_app.py test_generator.py demo.py; \
	else \
		echo "⚠️  black not found. Install with: pip install black"; \
	fi

# Generate example course
example:
	@echo "📚 Generating example course..."
	python main.py example_codebase ./example-course
	@echo "✅ Example course generated"
	@echo "📂 Open: ./example-course/index.html"

# Run with verbose output
verbose:
	@echo "🔍 Running with verbose output..."
	python main.py example_codebase ./verbose-output -v
	@echo "✅ Verbose run completed"

# Show project structure
tree:
	@echo "📁 Project structure:"
	@if command -v tree >/dev/null 2>&1; then \
		tree -I '__pycache__|*.pyc|*.pyo|.git|.vscode|.idea'; \
	else \
		echo "⚠️  tree command not found"; \
		echo "Files:"; \
		find . -type f -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.yml" | head -20; \
	fi

# Show file sizes
sizes:
	@echo "📊 File sizes:"
	@find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.txt" \) -exec wc -l {} \; | sort -n

# Run all checks
check: test lint
	@echo "✅ All checks passed"

# Quick start
quick-start: install demo
	@echo "🎉 Quick start completed!"
	@echo "📖 Read README.md for more information"
