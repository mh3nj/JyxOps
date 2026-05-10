# JyxOps – Universal Data Format Converter Development Timeline

**Project Start:** May 3, 2026  
**Completion Date:** May 3, 2026  
**Version:** 1.0.0

---

## Development Journey

### Day 1 – May 3, 2026 (Single Day Intensive)

#### Morning Session (3 hours)
- Project planning and architecture design
- Technology stack selection (PyQt6, PyYAML, xmltodict, dicttoxml)
- Repository setup and virtual environment configuration
- Basic conversion functions (YAML ↔ JSON ↔ XML)
- Testing conversion accuracy with sample data

#### Late Morning Session (2 hours)
- PyQt6 main window with three panel layout
- Live conversion signals and textChanged handlers
- Drag and drop file loading support
- Dark theme implementation (Fusion style + custom QSS)

#### Early Afternoon Session (2 hours)
- Line numbers for each editor (custom QPlainTextEdit subclass)
- Zoom in/out with Ctrl+Mouse Wheel
- Horizontal scroll with Shift+Mouse Wheel
- Current line highlighting

#### Afternoon Session (2.5 hours)
- Syntax highlighting for YAML, JSON, and XML (QSyntaxHighlighter)
- Dracula-inspired color palette (pink keywords, green keys, cyan numbers, purple XML tags)
- Find/Replace dialog with regex, case‑sensitive, and whole word options

#### Late Afternoon Session (2 hours)
- Pretty Print for all three formats (json.dumps, yaml.dump, minidom)
- Export individual formats (YAML, JSON, XML)
- Export All (timestamped folder + ZIP archive options)

#### Evening Session (2.5 hours)
- Batch conversion dialog (QThread, progress bar, folder selection)
- Settings persistence (QSettings – font sizes, splitter positions, last export folder)
- Per‑panel font size memory (zoom survives restart)
- Undo/Redo system (Ctrl+Z, Ctrl+Y / Ctrl+Shift+Z) with focus tracking

#### Late Evening Session (2 hours)
- Shortcut cheat sheet dialog (Ctrl+?)
- About dialog and branding
- Bug fixes and edge case handling
- Cross‑platform testing preparation

**Day 1 Total:** ~16 hours | **Status:** COMPLETE

---

## Feature Count Summary

| Category | Features |
|----------|----------|
| Conversion Core | 3 formats (YAML, JSON, XML) |
| Live Sync | Bidirectional conversion |
| Editor Features | Line numbers, zoom, scroll, highlight |
| Syntax Highlighting | 3 formats, 7 color rules |
| Search & Replace | 4 options (case, whole word, regex) |
| Export System | 4 modes (per format + All) |
| Batch Conversion | 4 combinations (from/to any format) |
| Settings | 4 persistent values |
| **Total** | **~25 core features** |

---

## Total Development Time

| Metric | Value |
|--------|-------|
| **Total days** | 1 day (May 3, 2026) |
| **Total hours** | ~16 hours |
| **Average per session** | ~2 hours |
| **Lines of code** | ~2,500+ (Python, QSS) |
| **Files created** | 11 files |
| **Key classes** | MegaConverter, IndentedTextEdit, YamlJsonHighlighter, FindReplaceDialog, BatchConverterDialog, SettingsManager |
| **Keyboard shortcuts** | 12+ |

---

## Key Achievements

- Built **2,500+ lines** of production‑ready Python code in a single day
- Integrated **3 data formats** with live bidirectional conversion
- Implemented **custom QPlainTextEdit** with line numbers, zoom, and horizontal scroll
- Created **Dracula‑inspired syntax highlighting** for YAML, JSON, and XML
- Built **batch conversion system** with threading and progress bar
- Added **Export All** with ZIP or timestamped folder options
- Achieved **100% dark theme** across all widgets (no light theme – intentional)
- Implemented **persistent settings** (QSettings) for 4 user preferences
- Added **12+ keyboard shortcuts** for power users

---

## Daily Breakdown Chart

```
May 3, 2026:

Morning:         ████████████  3 hrs  (Planning + Basic Conversion)
Late Morning:    ████████      2 hrs  (GUI + Drag & Drop)
Early Afternoon: ████████      2 hrs  (Line Numbers + Zoom)
Afternoon:       ██████████    2.5 hrs (Syntax Highlighting + Find/Replace)
Late Afternoon:  ████████      2 hrs  (Pretty Print + Export)
Evening:         ██████████    2.5 hrs (Batch Convert + Settings + Undo/Redo)
Late Evening:    ████████      2 hrs  (Polish + Documentation)
                 ─────────────────────
Total:           16 hours of focused development
```

---

## Lessons Learned

| Challenge | Solution |
|-----------|----------|
| XML lists losing `id` attributes | Custom recursion in `dict_to_xml` adds `@id` to each list item |
| Undo/Redo clearing on conversion | Never update the source editor – only the other two panels |
| File watcher unreliable on Windows | Removed and added polling fallback (later removed for simplicity) |
| PyQt6 clipboard COM errors | Create fresh `QMimeData` object instead of reusing system clipboard |
| QPlainTextEdit has no `QTextEdit.ExtraSelection` | Use `QPlainTextEdit.setExtraSelections` with `QTextEdit.ExtraSelection` (mixed inheritance hack) |
| Inconsistent indentation crashes YAML | Added automatic red border on syntax error |

---

## File Structure (v1.0)

```
JyxOps/
├── main.py                 # Entry point, main window logic
├── converters.py           # YAML/JSON/XML conversion functions
├── indented_edit.py        # Custom text editor with line numbers and zoom
├── highlighter.py          # Syntax highlighting (Dracula theme)
├── find_replace_dialog.py  # Find/Replace dialog
├── batch_converter.py      # Batch conversion dialog and worker thread
├── settings_manager.py     # Persistent settings (QSettings wrapper)
├── about_dialog.py         # Shortcut cheat sheet dialog
├── themes.py               # Dark theme QSS
├── LearnHub/               # Tutorials for YAML, JSON, XML
│   ├── YAML.md
│   ├── JSON.md
│   └── XML.md
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Future Enhancements (v1.1+)

- Light theme toggle (re‑enable after initial removal)
- File watcher with polling fallback
- Copy as HTML with Pygments syntax highlighting
- TOML format support
- Command-line interface (batch without GUI)
- Docker containerization

---

## Author

**Mohsen Jafari** - Creator, Developer, Designer

- GitHub: [mh3nj](https://github.com/mh3nj)
- LinkedIn: [mh3nj](https://linkedin.com/in/mh3nj)
- Websites: [Parsegan.com](https://parsegan.com) (logo design), [Dahgan.com](https://dahgan.com) (land surveying/portfolio)

---

*This project was created during internet restrictions in Iran – proof that creativity and persistence know no boundaries.*
