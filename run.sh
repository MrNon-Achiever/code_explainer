#!/bin/bash
# Simplified Codebase-to-Course Generator - Startup Script
# This script provides a convenient way to run the generator on Unix-like systems

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${1}${2}${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to show help
show_help() {
    print_color $BLUE "🚀 Simplified Codebase-to-Course Generator"
    echo "=========================================="
    echo ""
    echo "Usage: ./run.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  help        Show this help message"
    echo "  install     Install dependencies"
    echo "  demo        Run demo with example codebase"
    echo "  run         Run with example codebase"
    echo "  run-custom  Run with custom codebase (specify path)"
    echo "  test        Run tests"
    echo "  streamlit   Start Streamlit web interface"
    echo "  docker      Build and run with Docker"
    echo "  clean       Clean generated files"
    echo ""
    echo "Examples:"
    echo "  ./run.sh help"
    echo "  ./run.sh install"
    echo "  ./run.sh demo"
    echo "  ./run.sh run-custom /path/to/your/project"
    echo "  ./run.sh run-custom /path/to/your/project ./output"
    echo ""
    echo "Options:"
    echo "  --help, -h    Show this help message"
    echo "  --verbose, -v Enable verbose output"
}

# Function to install dependencies
install_deps() {
    print_color $YELLOW "📦 Installing dependencies..."
    
    # Check if pip is available
    if ! command_exists pip; then
        print_color $RED "❌ pip not found. Please install Python and pip first."
        exit 1
    fi
    
    # Install requirements
    pip install -r requirements.txt
    
    print_color $GREEN "✅ Dependencies installed"
}

# Function to run demo
run_demo() {
    print_color $YELLOW "🎮 Running demo..."
    python demo.py
    print_color $GREEN "✅ Demo completed"
}

# Function to run with example codebase
run_example() {
    print_color $YELLOW "🚀 Running with example codebase..."
    python main.py example_codebase ./course-output
    print_color $GREEN "✅ Generation completed"
    print_color $BLUE "📂 Output: ./course-output/index.html"
}

# Function to run with custom codebase
run_custom() {
    if [ -z "$1" ]; then
        print_color $RED "❌ Please specify codebase path"
        echo "Usage: ./run.sh run-custom /path/to/codebase [output_dir]"
        exit 1
    fi
    
    CODEBASE="$1"
    OUTPUT="${2:-./course-output}"
    
    print_color $YELLOW "🚀 Running with custom codebase..."
    python main.py "$CODEBASE" "$OUTPUT"
    print_color $GREEN "✅ Generation completed"
    print_color $BLUE "📂 Output: $OUTPUT/index.html"
}

# Function to run tests
run_tests() {
    print_color $YELLOW "🧪 Running tests..."
    python test_generator.py
    print_color $GREEN "✅ Tests completed"
}

# Function to start Streamlit
start_streamlit() {
    print_color $YELLOW "🌐 Starting Streamlit interface..."
    
    # Check if streamlit is installed
    if ! command_exists streamlit; then
        print_color $YELLOW "⚠️  Streamlit not found. Installing..."
        pip install streamlit
    fi
    
    streamlit run streamlit_app.py
    print_color $GREEN "✅ Streamlit started"
}

# Function to build and run with Docker
run_docker() {
    print_color $YELLOW "🐳 Building and running with Docker..."
    
    # Check if docker is available
    if ! command_exists docker; then
        print_color $RED "❌ Docker not found. Please install Docker first."
        exit 1
    fi
    
    # Build Docker image
    docker build -t codebase-to-course .
    
    # Run with example codebase
    docker run -v "$(pwd)/your-project:/app/input" -v "$(pwd)/output:/app/output" codebase-to-course python main.py /app/input /app/output
    
    print_color $GREEN "✅ Docker run completed"
}

# Function to clean generated files
clean_files() {
    print_color $YELLOW "🧹 Cleaning generated files..."
    
    rm -rf course-output
    rm -rf example_course_output
    rm -rf demo_course_output
    rm -rf output
    rm -rf __pycache__
    rm -rf .pytest_cache
    rm -rf *.pyc
    
    print_color $GREEN "✅ Cleanup completed"
}

# Main script logic
case "${1:-help}" in
    "help")
        show_help
        ;;
    "install")
        install_deps
        ;;
    "demo")
        run_demo
        ;;
    "run")
        run_example
        ;;
    "run-custom")
        shift
        run_custom "$@"
        ;;
    "test")
        run_tests
        ;;
    "streamlit")
        start_streamlit
        ;;
    "docker")
        run_docker
        ;;
    "clean")
        clean_files
        ;;
    *)
        print_color $RED "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
