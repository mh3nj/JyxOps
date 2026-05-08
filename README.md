
# JyxOps - Universal Data Format Converter

^_^ Convert between YAML, JSON, and XML with zero hassle. ^_^

JyxOps is a desktop application that provides live, bidirectional conversion between three major data formats. Built for DevOps engineers, developers, and system administrators who regularly work with configuration files, API responses, and infrastructure definitions.

:-) No more manual reformatting. No more syntax guesswork. Just drag, drop, and convert. :-)


## Features

:-D

- **Live Conversion** - Edit in any panel (YAML, JSON, or XML), the other two update instantly
- **Dark Theme Only** - Designed for comfortable long sessions at the terminal (no eye strain)
- **Line Numbers** - Every editor shows line numbers for easy navigation and debugging
- **Zoom In/Out** - Ctrl + Mouse Wheel to adjust font size (per-panel memory preserved)
- **Horizontal Scroll** - Shift + Mouse Wheel for long lines that wrap beyond screen width
- **Find / Replace** - Ctrl+F and Ctrl+H with case-sensitive, whole word, and regex options
- **Pretty Print** - Ctrl+Shift+F to auto-format messy code in the current panel
- **Batch Conversion** - Convert entire folders from one format to another with progress bar
- **Drag & Drop** - Drop any .yaml, .yml, .json, or .xml file directly onto the window
- **Export Individual** - Save current data as YAML, JSON, or XML separately
- **Export All** - Create timestamped folder OR single ZIP archive with all three formats
- **Settings Persistence** - Remembers font sizes, splitter positions, and last export folder
- **Undo / Redo** - Ctrl+Z and Ctrl+Y (or Ctrl+Shift+Z) - history preserved even after conversion


## Supported Formats

:-O

| Format | Extension(s) | Direction | Notes                                      |
|--------|--------------|-----------|--------------------------------------------|
| YAML   | .yaml, .yml  | Read/Write | Standard YAML 1.2, no custom tags         |
| JSON   | .json        | Read/Write | Strict JSON, double quotes, no comments   |
| XML    | .xml         | Read/Write | Repeated sibling elements get id="1", id="2" attributes |


## Installation

>"<

### From Source

```bash
git clone https://github.com/parsegan/JyxOps.git
cd JyxOps
pip install -r requirements.txt
python main.py
```

## Requirements

^_^

- Python 3.10 or higher (for source installation)
- PyQt6
- PyYAML
- xmltodict
- dicttoxml

All dependencies are listed in `requirements.txt`.


## Usage

<3

### Basic Workflow

1. Launch JyxOps
2. Drag a YAML, JSON, or XML file onto the drop area (or use File > Open)
3. Edit any panel - the other two panels update automatically
4. Export individual formats or use Export All for a complete package

### Keyboard Shortcuts

:-P

| Action               | Shortcut                          |
|----------------------|-----------------------------------|
| Open file            | Ctrl+O                            |
| Export YAML          | Ctrl+Shift+Y or toolbar button    |
| Export JSON          | Ctrl+Shift+J or toolbar button    |
| Export XML           | Ctrl+Shift+X or toolbar button    |
| Export All (ZIP)     | Ctrl+Shift+E or toolbar button    |
| Pretty Print         | Ctrl+Shift+F                      |
| Find                 | Ctrl+F                            |
| Replace              | Ctrl+H                            |
| Undo                 | Ctrl+Z                            |
| Redo                 | Ctrl+Y or Ctrl+Shift+Z            |
| Zoom In              | Ctrl+Mouse Wheel Up               |
| Zoom Out             | Ctrl+Mouse Wheel Down             |
| Horizontal Scroll    | Shift+Mouse Wheel                 |
| Clear All            | Toolbar button or menu            |

### Batch Conversion

1. Click the "Batch Convert" button in the toolbar (or press Ctrl+B)
2. Select input folder (contains source files)
3. Select output folder (destination for converted files)
4. Choose input format (YAML, JSON, or XML)
5. Choose output format (YAML, JSON, or XML)
6. Click "Convert" - progress bar shows status

### Export All

Two export modes are available:

1. **ZIP Archive** - Creates a single compressed file containing data.yaml, data.json, and data.xml
2. **Timestamped Folder** - Creates a folder named export_YYYYMMDD_HHMMSS with all three files

Choose your preferred mode when prompted after clicking Export All.


## Screenshots

^_-

Screenshots will be added to the `/screenshots` folder in the repository.

- Main window with three panels (dark theme)
- Batch conversion dialog with progress
- Find/Replace dialog (regex mode)
- Export All ZIP file creation


## Project Structure

```
JyxOps/
├── main.py                 # Entry point, main window logic
├── converters.py           # YAML/JSON/XML conversion functions
├── indented_edit.py        # Custom text editor with line numbers and zoom
├── highlighter.py          # Syntax highlighting (Dracula theme)
├── find_replace_dialog.py  # Find/Replace dialog
├── batch_converter.py      # Batch conversion dialog and worker thread
├── settings_manager.py     # Persistent settings (QSettings wrapper)
├── about_dialog.py         # Shortcut cheat sheet
├── themes.py               # Dark theme CSS
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── screenshots/            # Application screenshots (to be added)
```


## Development

:-(

**Timeline:** Single day development (May 2, 2026) - approximately 5 hours of intensive coding.

**Status:** Complete, stable, ready for production use.

**Tested on:** Windows 11, Ubuntu 22.04 (planned), macOS (planned)


## Known Limitations

:-O

- No light theme (dark theme only - intentional for DevOps workflow)
- XML conversion wraps data in a default root tag if no root exists
- No file watcher (auto-reload on external changes)
- No Copy as HTML functionality


## Roadmap (Future Versions)

^_^ <3

- Light theme toggle (re-enable after initial removal)
- File watcher with polling fallback
- Copy as HTML with Pygments syntax highlighting
- TOML format support
- Command-line interface (batch without GUI)
- Docker containerization


## Contributing

:-P

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please ensure tests pass before submitting (tests to be added in v1.1).


## License

^_-

MIT License - Free for personal and commercial use with attribution.

Because tools should be free, not walled gardens. :-)


## Author

**Mohsen Jafari** - Creator, Developer, Designer

- GitHub: [github.com/parsegan](https://github.com/parsegan), [github.com/mh3nj](https://github.com/mh3nj)
- LinkedIn: [linkedin.com/in/parsegan](https://linkedin.com/in/parsegan)
- Websites: [Parsegan.com](https://parsegan.com) (logo design), [Dahgan.com](https://dahgan.com) (land surveying)
- Email: parsegan@proton.me

## Acknowledgements

- PyQt6 team for an amazing GUI framework
- PyYAML, xmltodict, and dicttoxml developers
- The DevOps community who suffer daily with YAML indentation
- Internet restrictions in Iran - you made me build things offline :-P


## Development Context

This project was completed during internet restrictions in Iran. All code was written offline without access to package repositories, documentation, or online resources. The application was developed entirely using local knowledge, memory, and AI assistance that was available before restrictions intensified.

:-) Proof of genuine software development activity is available through local Git commit history and file creation timestamps. :-)


## Support

For issues, questions, or feature requests, please open a GitHub issue. Responses may be delayed due to connectivity constraints, but all inquiries will be addressed.

:-D
