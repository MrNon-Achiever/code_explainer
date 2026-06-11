#!/bin/bash
# Installation script for Simplified Codebase-to-Course Generator

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

# Function to check Python version
check_python_version() {
    if ! command_exists python3; then
        if ! command_exists python; then
            print_color $RED "❌ Python is not installed."
            echo "Please install Python 3.7 or higher:"
            echo "  - macOS: brew install python3"
            echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip"
            echo "  - CentOS/RHEL: sudo yum install python3"
            echo "  - Windows: Download from https://www.python.org/downloads/"
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        print_color $RED "❌ Python 3.7 or higher is required. Found: $PYTHON_VERSION"
        echo "Please upgrade Python."
        exit 1
    fi
    
    print_color $GREEN "✅ Python $PYTHON_VERSION found"
}

# Function to install pip if needed
install_pip() {
    if ! command_exists pip3; then
        if ! command_exists pip; then
            print_color $YELLOW "⚠️  pip not found. Installing..."
            $PYTHON_CMD -m ensurepip --upgrade
            if ! command_exists pip3; then
                print_color $RED "❌ Failed to install pip."
                echo "Please install pip manually:"
                echo "  - macOS: brew install pip3"
                echo "  - Ubuntu/Debian: sudo apt-get install python3-pip"
                echo "  - Windows: pip is usually included with Python"
                exit 1
            fi
        else
            PIP_CMD="pip"
        fi
    else
        PIP_CMD="pip3"
    fi
    
    print_color $GREEN "✅ pip found"
}

# Function to create virtual environment
create_venv() {
    print_color $YELLOW "🐍 Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_color $YELLOW "⚠️  Virtual environment already exists. Skipping creation."
    else
        $PYTHON_CMD -m venv venv
        print_color $GREEN "✅ Virtual environment created"
    fi
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_color $GREEN "✅ Virtual environment activated"
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
        print_color $GREEN "✅ Virtual environment activated"
    else
        print_color $YELLOW "⚠️  Could not activate virtual environment."
        echo "Please activate it manually:"
        echo "  - macOS/Linux: source venv/bin/activate"
        echo "  - Windows: venv\\Scripts\\activate"
    fi
}

# Function to install dependencies
install_dependencies() {
    print_color $YELLOW "📦 Installing dependencies..."
    
    # Upgrade pip
    $PIP_CMD install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        $PIP_CMD install -r requirements.txt
        print_color $GREEN "✅ Core dependencies installed"
    fi
    
    # Install Streamlit requirements (optional)
    if [ -f "requirements_streamlit.txt" ]; then
        read -p "Install Streamlit for web interface? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            $PIP_CMD install -r requirements_streamlit.txt
            print_color $GREEN "✅ Streamlit dependencies installed"
        fi
    fi
    
    # Install development dependencies (optional)
    read -p "Install development tools (black, flake8, pytest)? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        $PIP_CMD install black flake8 pytest
        print_color $GREEN "✅ Development tools installed"
    fi
}

# Function to verify installation
verify_installation() {
    print_color $YELLOW "🔍 Verifying installation..."
    
    # Test main script
    if $PYTHON_CMD main.py --help > /dev/null 2>&1; then
        print_color $GREEN "✅ Main script works"
    else
        print_color $RED "❌ Main script failed"
        exit 1
    fi
    
    # Test demo script
    if $PYTHON_CMD -c "from main import CodebaseAnalyzer, CourseGenerator" > /dev/null 2>&1; then
        print_color $GREEN "✅ Core modules import correctly"
    else
        print_color $RED "❌ Core modules failed to import"
        exit 1
    fi
    
    # Test example codebase
    if [ -d "example_codebase" ]; then
        print_color $GREEN "✅ Example codebase found"
    else
        print_color $YELLOW "⚠️  Example codebase not found"
    fi
}

# Function to show post-installation instructions
show_instructions() {
    echo ""
    print_color $BLUE "🎉 Installation complete!"
    echo "=========================================="
    echo ""
    echo "Quick start:"
    echo ""
    echo "1. Run with example codebase:"
    echo "   python main.py example_codebase"
    echo ""
    echo "2. Run demo:"
    echo "   python demo.py"
    echo ""
    echo "3. Run tests:"
    echo "   python test_generator.py"
    echo ""
    echo "4. Start Streamlit interface (if installed):"
    echo "   streamlit run streamlit_app.py"
    echo ""
    echo "5. Analyze your own codebase:"
    echo "   python main.py /path/to/your/python/project"
    echo ""
    echo "6. Use Makefile (if available):"
    echo "   make help"
    echo ""
    echo "For more information, see:"
    echo "  - README.md"
    echo "  - USAGE.md"
    echo ""
    echo "=========================================="
}

# Main installation process
main() {
    print_color $BLUE "🚀 Simplified Codebase-to-Course Generator - Installation"
    echo "========================================================"
    echo ""
    
    # Check Python
    check_python_version
    
    # Check/install pip
    install_pip
    
    # Create virtual environment
    create_venv
    
    # Install dependencies
    install_dependencies
    
    # Verify installation
    verify_installation
    
    # Show instructions
    show_instructions
    
    # Ask to run demo
    read -p "Would you like to run the demo now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_color $YELLOW "🎮 Running demo..."
        $PYTHON_CMD demo.py
    fi
}

# Run main function
main "$@"
