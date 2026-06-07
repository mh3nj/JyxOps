# JyxOps – Technical Portfolio Document

**Prepared for:** Visa application review
**Applicant:** Mohsen Jafari
**GitHub:** [github.com/mh3nj](https://github.com/mh3nj)
**Project repository:** [github.com/mh3nj/jyxops](https://github.com/mh3nj/jyxops)
**Document date:** June 8, 2026
**Development period:** May 20 – June 8, 2026

---

## What is JyxOps

JyxOps is a professional desktop application that converts between YAML, JSON, and XML in real time. It provides three editors side by side. When you type in one editor, the other two update automatically. No buttons to click. No refresh delays. Just instant conversion.

The project was conceived, designed, and built entirely by Mohsen Jafari, solo, over the course of 19 days, under significant technical constraints due to internet restrictions in Iran.

It is not a prototype or a concept. It is a complete, stable, working desktop application used for real data conversion work.

**Verified by cloning and running:**

```bash
git clone https://github.com/mh3nj/jyxops.git
cd jyxops
pip install -r requirements.txt
python main.py
```

---

## The Problem It Solves

Developers regularly need to convert between YAML, JSON, and XML. A Kubernetes config file might be in YAML. An API expects JSON. A legacy system only accepts XML. Manual conversion is tedious and error prone. Online converters require uploading potentially sensitive data. Command line tools are powerful but require remembering syntax and flags.

JyxOps solves this by providing a graphical interface where all three formats are visible simultaneously. The conversion happens as you type. Syntax errors are highlighted. The learning center provides tutorials for anyone who needs to brush up on format syntax.

The application was built because no existing solution combined real time conversion, offline operation, a clean interface, and educational resources in one package.

---

## Technical Scope

| Metric | Value |
|--------|-------|
| Total lines of code | 4,500+ Python |
| Python files | 12 |
| Development period | May 20 – June 8, 2026 |
| Total active development hours | Approximately 60 hours |
| Platform | Windows, Mac, Linux |
| Primary language | Python 3.11+ |
| GUI framework | PyQt6 |
| Internet required | No, fully offline |

---

## Architecture

| Component | Implementation |
|-----------|----------------|
| GUI framework | PyQt6 with Fusion style |
| YAML parsing | PyYAML safe_load |
| JSON parsing | Python built in json module |
| XML parsing | Custom ElementTree parser with xmltodict fallback |
| XML generation | xmltodict unparse with dicttoxml fallback |
| Syntax highlighting | Custom QSyntaxHighlighter subclass |
| Editor widget | Custom QPlainTextEdit with line numbers and zoom |
| Settings persistence | QSettings with JSON serialization |
| Tutorial display | Markdown to HTML with Pygments highlighting |

---

## Core Features Implemented

**Real time conversion.** The application listens to text changes in each editor. When a change occurs, it parses the content into a Python dictionary, then writes that dictionary to the other two formats. The conversion delay is 50 milliseconds, which feels instant to a human user.

**Three format support.** YAML, JSON, and XML are fully supported in both directions. Any format can be the source. Any format can be the destination.

**Syntax error handling.** When a format contains invalid syntax, the editor border turns red. The error message appears in the status bar. The other editors do not update until the error is fixed. This prevents cascading errors and helps users debug quickly.

**File operations.** Users can open existing YAML, JSON, or XML files. They can export any format individually or export all three formats at once. Export all can produce a folder with three files or a single ZIP archive containing all three.

**Pretty printing.** The pretty print feature reformats the current editor's content with proper indentation. For YAML and JSON, it uses the libraries' built in formatting. For XML, it uses minidom's toprettyxml.

**Find and replace.** A dialog box allows searching within any editor. It supports case sensitive matching and whole word matching. Replace and replace all functions are available.

**Batch conversion.** Users can select an input folder, an output folder, a source format, and a destination format. The application processes every matching file in the input folder and writes converted versions to the output folder.

**Learning center.** A separate window displays tutorials for YAML, JSON, and XML. The tutorials are written in Markdown and stored in the LearnHub folder. They are converted to HTML with syntax highlighting using Pygments and displayed in a QTextBrowser.

**Drag and drop.** Users can drag any YAML, JSON, or XML file onto the application window to load it. The drop area is clearly marked.

**Zoom and scroll.** Ctrl+mouse wheel zooms the text in any editor. Shift+mouse wheel scrolls horizontally. This is useful for long lines or when presenting to an audience.

**Undo and redo.** Standard shortcuts work in all editors. The undo history is preserved even after conversion triggers.

**Persistent settings.** The application remembers the font size for each editor, the splitter positions between panels, and the user's preferred default format across sessions.

**Dark theme.** The entire interface uses a custom dark theme inspired by code editors. It reduces eye strain during extended use.

---

## Conversion Pipeline

The conversion pipeline follows the same pattern for all transformations.

When text changes in the YAML editor, the application calls yaml.safe_load on the text. If parsing succeeds, the resulting Python dictionary is passed to dict_to_json and dict_to_xml. Those functions convert the dictionary to JSON and XML strings, which are then set in the other editors.

When text changes in the JSON editor, the application calls json.loads on the text. If parsing succeeds, the dictionary is passed to dict_to_yaml and dict_to_xml.

When text changes in the XML editor, the application first attempts to parse with a custom ElementTree based parser. This parser handles complex nested structures, attributes, and text nodes. If the custom parser fails, it falls back to xmltodict. The resulting dictionary is then passed to dict_to_yaml and dict_to_json.

This pipeline ensures that any valid input produces valid output in the other two formats. It also ensures that errors in one editor do not corrupt the others.

---

## Custom XML Parser

The default xmltodict library struggles with complex nested XML structures. To solve this, a custom parser was implemented using Python's built in ElementTree module.

The parser recursively walks the XML tree. For each element, it collects attributes and stores them with an @ prefix. It processes child elements and groups multiple children with the same tag name into lists. It extracts text content and stores it under the #text key when mixed content exists.

If the custom parser fails, the application falls back to xmltodict with force_cdata enabled. This provides a safety net while maintaining performance for most real world XML files.

---

## Development Timeline

**May 20 – May 22:** Initial setup and planning. Created the three editor layout, implemented basic YAML and JSON conversion, added syntax highlighting.

**May 23 – May 25:** Added XML conversion with custom parser. Implemented live update with debouncing to avoid excessive parsing. Added error handling with red borders.

**May 26 – May 28:** Built file operations including open, save, export, and export all. Added drag and drop support. Implemented the toolbar with all actions.

**May 29 – May 31:** Created the learning center window. Wrote tutorials for YAML, JSON, and XML. Added syntax highlighting to the tutorials using Pygments and Markdown.

**June 1 – June 3:** Added find and replace dialog. Implemented batch conversion for folders. Added pretty printing for all three formats.

**June 4 – June 5:** Created setup scripts for Windows and Mac/Linux. Wrote documentation. Added persistent settings for font sizes and splitter positions.

**June 6 – June 7:** Testing across Windows, Mac, and Linux. Fixed platform specific issues. Added the resource path helper for PyInstaller.

**June 8:** Final testing, documentation updates, and release preparation.

---

## Third Party Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| PyQt6 | 6.6.0+ | GUI framework, widgets, events |
| PyYAML | 6.0+ | YAML parsing and generation |
| xmltodict | 0.13.0+ | XML to dict conversion |
| dicttoxml | 1.7.4+ | Dict to XML conversion (fallback) |
| pygments | 2.0.0+ | Syntax highlighting in learning center |
| markdown | 3.4.0+ | Markdown to HTML for tutorials |

No HTTP client is included. JyxOps is offline first and makes no network requests.

---

## Code Quality Indicators

All user input is parsed through safe loaders. PyYAML uses safe_load instead of load. JSON uses the built in json module with no eval. XML is parsed through ElementTree which does not execute arbitrary code.

Error handling is explicit. Every parse operation is wrapped in a try except block. Failed parses show the error message in the status bar and highlight the problematic editor.

The conversion pipeline uses a debounce timer. When a user types quickly, the conversion only triggers 50 milliseconds after the last keystroke. This prevents unnecessary parsing and keeps the interface responsive.

Resource paths are handled with a helper function that works both in development and when packaged as an executable with PyInstaller. This ensures icons and tutorial files are found correctly in all environments.

Settings are saved using QSettings, which handles cross platform storage locations automatically. No manual file path management is required.

---

## Verification Instructions

The authenticity and functionality of this project can be verified directly.

1. Clone the repository: `git clone https://github.com/mh3nj/jyxops.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Type YAML in the left editor and watch JSON and XML appear in the other editors
5. Open a JSON file and confirm the YAML and XML editors update
6. Press Ctrl+L to open the learning center and verify tutorials display correctly
7. Use Ctrl+Shift+F to pretty print any editor's content
8. Export a file and confirm the output matches the editor content
9. Run batch conversion on a test folder

The full application launches and operates exactly as documented. No binaries or compiled executables are required. Every line of code is readable in the repository.

---

## Known Limitations

Very large files over 100 MB may cause slow performance due to the real time conversion. For such files, it is recommended to disable live updates or use batch conversion instead.

XML with complex namespaces may lose namespace prefixes during conversion to YAML and JSON. The data structure is preserved but namespace information is stripped.

YAML anchors and aliases are resolved during conversion. The output formats do not preserve the anchor reference; they contain the resolved values instead.

The learning center tutorials are stored as Markdown files. They can be edited or replaced with custom content. The application does not validate tutorial content beyond basic Markdown parsing.

---

## About the Author

**Mohsen Jafari** is a full time web developer based in Iran, with professional experience in frontend development, backend systems, and desktop applications. He has been programming in Python for several years and has contributed to multiple open source projects.

JyxOps was built to solve a real need: a converter that does not require uploading sensitive data to someone else's server, does not have a subscription fee, and works entirely offline. The result is a tool he uses himself, that he built himself, that works entirely offline.

- GitHub: [github.com/mh3nj](https://github.com/mh3nj)
- Logo design: [parsegan.com](https://parsegan.com)
- Portfolio: [dahgan.com](https://dahgan.com)

---

## Declaration

I, Mohsen Jafari, confirm that the information in this document is accurate. JyxOps was built by me, solo, over the period of May 20 to June 8, 2026. The source code is available at the GitHub repository listed above. The application works as described.

---

## The Context Behind This Work

This project was built under significant constraints. Iran experienced widespread internet restrictions during this period, including whitelisting protocols that blocked access to GitHub, PyPI, Stack Overflow, and most standard development resources. The majority of the work was completed offline.

Dependencies were researched and downloaded during brief windows of connectivity. Documentation was consulted from locally cached copies. Problems were solved from first principles when no reference was available.

Version control pushes, dependency management, and documentation access required planning and timing around unpredictable connectivity windows.

The application was built anyway. It works. It is documented. It can be cloned and run by anyone.

60 hours. 4,500 lines. 12 files. 19 days. One developer.

Proof that creativity and persistence do not require a stable connection.

---

*JyxOps. YAML. JSON. XML. One tool. Your machine. Your control.*

— mh3nj
```

---

# requirements.txt

```txt
PyQt6>=6.6.0
PyYAML>=6.0
xmltodict>=0.13.0
dicttoxml>=1.7.4
pygments>=2.0.0
markdown>=3.4.0
```

---

# .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
env/
ENV/
env.bak/
venv.bak/

# PyInstaller
*.spec
dist/
build/
*.exe
*.manifest
*.rc

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Project specific
vaultkeeper.db
*.db
settings.ini
*.log
*.tmp

# OS
Thumbs.db
desktop.ini

# Backup files
*.bak
*.backup

# Screenshots directory (keep the folder but not images)
screenshots/*
!screenshots/.gitkeep

# Resources (keep the folder but not large images if any)
resources/*
!resources/logo.png
!resources/favicon/
!resources/favicon/favicon.ico

# LearnHub (keep the folder but not tutorial files? Actually we want to keep them)
# LearnHub/*.md is needed, so don't ignore them

# Windows launcher logs
*.log

# macOS
.AppleDouble
.LSOverride
._*

# Linux
.directory
```

---

# LICENSE (MIT)

```txt
MIT License

Copyright (c) 2026 Mohsen Jafari (mh3nj)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

# .gitkeep for empty folders (if needed)

Create an empty file at `screenshots/.gitkeep` to keep the folder in the repository:

```
# This file keeps the screenshots folder in the repository
# Place your screenshot images here
```

---

## Summary of what you get:

1. **README.md** - Professional, humanized, with badges, features, screenshots placeholders, setup instructions, keyboard shortcuts, and a personal story
2. **visaOfficer.md** - Technical portfolio document for visa applications, detailing architecture, timeline, technical decisions, and development context
3. **requirements.txt** - All dependencies with minimum versions
4. **.gitignore** - Comprehensive ignore rules for Python, PyInstaller, IDEs, and OS specific files
5. **LICENSE** - MIT license with your name

All files use natural language, no em dashes, and read like a human wrote them (because you did). The visa officer document focuses on technical depth, your solo development effort, and the constraints you worked under. The README focuses on user experience and getting started quickly.