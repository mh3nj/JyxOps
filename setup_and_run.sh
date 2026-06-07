#!/bin/bash

# JyxOps - YAML | JSON | XML Converter Auto-Setup and Launcher
# For Linux and macOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Store the starting directory
STARTDIR=$(pwd)

echo -e "${BLUE}          JyxOps - YAML | JSON | XML Converter${NC}"
echo "                  Auto-Setup and Launcher"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed!${NC}"
    echo ""
    echo "Please install Python 3.8+ from:"
    echo "  - Linux: sudo apt install python3 python3-pip python3-venv"
    echo "  - macOS: brew install python3"
    echo "  - Or download from https://python.org"
    echo ""
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo -e "${RED}[ERROR] Python 3.8+ is required. Detected: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}[OK] Python found: $PYTHON_VERSION${NC}"

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}[ERROR] pip3 is not available!${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] pip found${NC}"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}[SETUP] Creating Python virtual environment...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}[OK] Virtual environment created${NC}"
else
    echo -e "${GREEN}[OK] Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}[SETUP] Activating virtual environment...${NC}"
source .venv/bin/activate
echo -e "${GREEN}[OK] Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${BLUE}[SETUP] Upgrading pip...${NC}"
pip install --upgrade pip
echo ""

# Check for requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}[WARNING] requirements.txt not found!${NC}"
    echo "Creating default requirements.txt..."
    cat > requirements.txt << EOF
PyQt6>=6.6.0
PyYAML>=6.0
xmltodict>=0.13.0
dicttoxml>=1.7.4
pygments>=2.0.0
markdown>=3.4.0
EOF
    echo -e "${GREEN}[OK] Created requirements.txt${NC}"
fi

# Install dependencies
echo -e "${BLUE}[SETUP] Installing/updating dependencies...${NC}"
echo "This may take a few minutes. Please wait..."
echo ""

if pip install -r requirements.txt; then
    echo -e "${GREEN}[OK] All dependencies installed successfully${NC}"
else
    echo -e "${RED}[ERROR] Failed to install dependencies!${NC}"
    echo "Trying to install individually..."
    echo ""
    
    pip install PyQt6 || true
    pip install PyYAML || true
    pip install xmltodict || true
    pip install dicttoxml || true
    pip install pygments || true
    pip install markdown || true
    
    echo -e "${YELLOW}[WARNING] Some dependencies may have failed${NC}"
fi

echo ""
echo -e "${BLUE}[CHECK] Verifying critical files...${NC}"

# Check for required Python files
REQUIRED_FILES=(
    "main.py"
    "indented_edit.py"
    "highlighter.py"
    "find_replace_dialog.py"
    "themes.py"
    "settings_manager.py"
    "about_dialog.py"
    "batch_converter.py"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}[ERROR] $file not found!${NC}"
        MISSING_FILES=1
    else
        echo -e "${GREEN}[OK] $file found${NC}"
    fi
done

if [ $MISSING_FILES -eq 1 ]; then
    echo ""
    echo -e "${RED}[ERROR] Missing required files!${NC}"
    exit 1
fi

# Check for learning_center.py (optional but recommended)
if [ ! -f "learning_center.py" ]; then
    echo -e "${YELLOW}[WARNING] learning_center.py not found${NC}"
    echo "The Learning Center feature may not work properly"
else
    echo -e "${GREEN}[OK] learning_center.py found${NC}"
fi

# Check for LearnHub directory
if [ ! -d "LearnHub" ]; then
    echo -e "${YELLOW}[WARNING] LearnHub directory not found${NC}"
    echo "Creating LearnHub directory..."
    mkdir -p LearnHub
    echo -e "${YELLOW}[INFO] Please add yaml.md, json.md, and xml.md to the LearnHub folder${NC}"
else
    echo -e "${GREEN}[OK] LearnHub directory found${NC}"
fi

echo ""
echo "============================================================"
echo -e "${GREEN}         Setup Complete! Launching JyxOps...${NC}"
echo "============================================================"
echo ""

# Start the application
echo -e "${BLUE}[LAUNCH] Starting JyxOps Converter...${NC}"
echo "Tip: Press Ctrl+L to open the Learning Center"
echo ""
python3 main.py

echo ""
echo -e "${GREEN}   JyxOps has been closed${NC}"
echo "   Thanks for using JyxOps - YAML | JSON | XML Converter"
echo ""
echo "You can re-run this file anytime to:"
echo "  - Update dependencies"
echo "  - Check for missing files"
echo "  - Launch the application"
echo ""

# Return to original directory
cd "$STARTDIR"