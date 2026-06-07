@echo off
title JyxOps - YAML | JSON | XML Converter Auto-Setup and Launcher
color 0A

setlocal enabledelayedexpansion

REM Store the starting directory
set STARTDIR=%CD%

echo            JyxOps - YAML ^| JSON ^| XML Converter
echo                    Auto-Setup and Launcher
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check Python version (must be 3.8+)
for /f "tokens=2 delims= " %%v in ('python --version') do set PYVER=%%v
for /f "tokens=1,2 delims=." %%a in ("!PYVER!") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if !MAJOR! LSS 3 (
    echo [ERROR] Python 3.8+ is required. Detected: !PYVER!
    pause
    exit /b 1
)
if !MAJOR! EQU 3 if !MINOR! LSS 8 (
    echo [ERROR] Python 3.8+ is required. Detected: !PYVER!
    pause
    exit /b 1
)

echo [OK] Python found: !PYVER!
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available!
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)
echo [OK] pip found
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [SETUP] Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [SETUP] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Check for requirements.txt
if not exist "requirements.txt" (
    echo [WARNING] requirements.txt not found!
    echo Creating default requirements.txt...
    (
        echo PyQt6>=6.6.0
        echo PyYAML>=6.0
        echo xmltodict>=0.13.0
        echo dicttoxml>=1.7.4
        echo pygments>=2.0.0
        echo markdown>=3.4.0
    ) > requirements.txt
    echo [OK] Created requirements.txt
)

REM Install dependencies
echo [SETUP] Installing/updating dependencies...
echo This may take a few minutes. Please wait...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install some dependencies!
    echo Trying to install individually...
    echo.
    
    REM Try installing each package individually
    pip install PyQt6
    pip install PyYAML
    pip install xmltodict
    pip install dicttoxml
    pip install pygments
    pip install markdown
    
    if errorlevel 1 (
        echo [ERROR] Still having issues with dependencies!
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
) else (
    echo [OK] All dependencies installed successfully
)

echo.
echo [CHECK] Verifying critical files...

REM Check for required Python files
if not exist "main.py" (
    echo [ERROR] main.py not found!
    echo Please make sure you are in the correct directory.
    pause
    exit /b 1
)

if not exist "learning_center.py" (
    echo [WARNING] learning_center.py not found
    echo The Learning Center feature may not work properly
) else (
    echo [OK] learning_center.py found
)

if not exist "indented_edit.py" (
    echo [ERROR] indented_edit.py not found!
    pause
    exit /b 1
)

if not exist "highlighter.py" (
    echo [ERROR] highlighter.py not found!
    pause
    exit /b 1
)

if not exist "find_replace_dialog.py" (
    echo [ERROR] find_replace_dialog.py not found!
    pause
    exit /b 1
)

if not exist "themes.py" (
    echo [ERROR] themes.py not found!
    pause
    exit /b 1
)

if not exist "settings_manager.py" (
    echo [ERROR] settings_manager.py not found!
    pause
    exit /b 1
)

if not exist "about_dialog.py" (
    echo [ERROR] about_dialog.py not found!
    pause
    exit /b 1
)

if not exist "batch_converter.py" (
    echo [ERROR] batch_converter.py not found!
    pause
    exit /b 1
)

echo [OK] All required files present
echo.

REM Check for LearnHub directory and create if missing
if not exist "LearnHub" (
    echo [WARNING] LearnHub directory not found!
    echo Creating LearnHub directory...
    mkdir LearnHub
    echo [INFO] Please add yaml.md, json.md, and xml.md to the LearnHub folder
    echo For tutorials, visit: https://github.com/mh3nj/jyxops/learnhub
) else (
    echo [OK] LearnHub directory found
)

echo.
echo              Setup Complete! Launching JyxOps...
echo.

REM Start the application
echo [LAUNCH] Starting JyxOps Converter...
echo Tip: Press Ctrl+L to open the Learning Center
echo.
python main.py

echo.
echo ============================================================
echo    JyxOps has been closed
echo    Thanks for using JyxOps - YAML ^| JSON ^| XML Converter
echo ============================================================
echo.
echo You can re-run this file anytime to:
echo   - Update dependencies
echo   - Check for missing files
echo   - Launch the application
echo.
echo Press any key to exit...
pause >nul

REM Return to original directory
cd /d "%STARTDIR%"
endlocal