@echo off
REM Simplified Codebase-to-Course Generator - Windows Batch File
REM This script provides a convenient way to run the generator on Windows

setlocal enabledelayedexpansion

REM Colors for output (limited in batch)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%Python is not installed or not in PATH%NC%
    echo Please install Python and add it to your PATH
    pause
    exit /b 1
)

REM Main menu
:menu
cls
echo %BLUE%🚀 Simplified Codebase-to-Course Generator%NC%
echo ==========================================
echo.
echo Choose an option:
echo.
echo 1. Install dependencies
echo 2. Run demo with example codebase
echo 3. Run with example codebase
echo 4. Run with custom codebase
echo 5. Run tests
echo 6. Start Streamlit web interface
echo 7. Clean generated files
echo 8. Show help
echo 9. Exit
echo.
set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto demo
if "%choice%"=="3" goto run_example
if "%choice%"=="4" goto run_custom
if "%choice%"=="5" goto test
if "%choice%"=="6" goto streamlit
if "%choice%"=="7" goto clean
if "%choice%"=="8" goto help
if "%choice%"=="9" goto exit

echo %RED%Invalid choice. Please try again.%NC%
pause
goto menu

:install
echo.
echo %YELLOW%📦 Installing dependencies...%NC%
pip install -r requirements.txt
if errorlevel 1 (
    echo %RED%Failed to install dependencies%NC%
) else (
    echo %GREEN%✅ Dependencies installed%NC%
)
pause
goto menu

:demo
echo.
echo %YELLOW%🎮 Running demo...%NC%
python demo.py
if errorlevel 1 (
    echo %RED%Demo failed%NC%
) else (
    echo %GREEN%✅ Demo completed%NC%
)
pause
goto menu

:run_example
echo.
echo %YELLOW%🚀 Running with example codebase...%NC%
python main.py example_codebase ./course-output
if errorlevel 1 (
    echo %RED%Generation failed%NC%
) else (
    echo %GREEN%✅ Generation completed%NC%
    echo %BLUE%📂 Output: ./course-output/index.html%NC%
)
pause
goto menu

:run_custom
echo.
echo %YELLOW%🚀 Running with custom codebase...%NC%
set /p codebase="Enter codebase path: "
if "%codebase%"=="" (
    echo %RED%No path specified%NC%
    pause
    goto menu
)

set /p output="Enter output directory (or press Enter for ./course-output): "
if "%output%"=="" set output=./course-output

python main.py "%codebase%" "%output%"
if errorlevel 1 (
    echo %RED%Generation failed%NC%
) else (
    echo %GREEN%✅ Generation completed%NC%
    echo %BLUE%📂 Output: %output%/index.html%NC%
)
pause
goto menu

:test
echo.
echo %YELLOW%🧪 Running tests...%NC%
python test_generator.py
if errorlevel 1 (
    echo %RED%Tests failed%NC%
) else (
    echo %GREEN%✅ Tests completed%NC%
)
pause
goto menu

:streamlit
echo.
echo %YELLOW%🌐 Starting Streamlit interface...%NC%
where streamlit >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%⚠️  Streamlit not found. Installing...%NC%
    pip install streamlit
)
streamlit run streamlit_app.py
if errorlevel 1 (
    echo %RED%Streamlit failed to start%NC%
) else (
    echo %GREEN%✅ Streamlit started%NC%
)
pause
goto menu

:clean
echo.
echo %YELLOW%🧹 Cleaning generated files...%NC%
if exist "course-output" rd /s /q "course-output"
if exist "example_course_output" rd /s /q "example_course_output"
if exist "demo_course_output" rd /s /q "demo_course_output"
if exist "output" rd /s /q "output"
if exist "__pycache__" rd /s /q "__pycache__"
if exist ".pytest_cache" rd /s /q ".pytest_cache"
del /q *.pyc 2>nul
echo %GREEN%✅ Cleanup completed%NC%
pause
goto menu

:help
echo.
echo %BLUE%🚀 Simplified Codebase-to-Course Generator%NC%
echo ==========================================
echo.
echo This tool analyzes Python codebases and generates
echo interactive HTML courses.
echo.
echo Commands:
echo   install      - Install dependencies
echo   demo         - Run demo with example codebase
echo   run          - Run with example codebase
echo   run-custom   - Run with custom codebase
echo   test         - Run tests
echo   streamlit    - Start Streamlit web interface
echo   clean        - Clean generated files
echo.
echo Examples:
echo   python main.py /path/to/your/project
echo   python main.py /path/to/your/project ./output
echo   python main.py /path/to/your/project -v
echo.
echo For more information, see README.md
echo.
pause
goto menu

:exit
echo.
echo %GREEN%Goodbye! 👋%NC%
exit /b 0
