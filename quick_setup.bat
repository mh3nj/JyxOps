@echo off
title JyxOps Quick Setup
color 0A

echo            JyxOps Quick Setup - One-Click Install
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Install Python 3.8+ first
    pause
    exit /b 1
)

REM Create virtual environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate and install
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install PyQt6 PyYAML xmltodict dicttoxml pygments markdown

echo.
echo Setup complete! Run 'python main.py' to start
echo.
pause