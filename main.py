# main.py - with custom XML parser for complex structures
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import yaml
import xmltodict
from xml.dom import minidom
import zipfile
import tempfile
import copy
import re
from html import escape
import xml.etree.ElementTree as ET

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QFileDialog, QMessageBox, QLabel, QPushButton, QSplitter,
    QToolBar, QStatusBar, QGroupBox, QComboBox
)
from PyQt6.QtCore import Qt, QSettings, QTimer, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QAction, QKeySequence, QGuiApplication, QIcon

from learning_center import LearningCenterDialog
from indented_edit import IndentedTextEdit
from highlighter import YamlJsonHighlighter
from find_replace_dialog import FindReplaceDialog
from themes import DARK_THEME
from settings_manager import SettingsManager
from about_dialog import ShortcutDialog
from batch_converter import BatchConverterDialog


# ---------- Helper function for PyInstaller resource paths ----------
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ---------- Custom JSON Encoder ----------
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        if isinstance(obj, (set, frozenset)):
            return list(obj)
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)


# ---------- Custom XML to Dict parser (handles complex nesting) ----------
def custom_xml_to_dict(xml_string):
    """Convert complex XML to dict using ElementTree."""
    
    def parse_element(element):
        """Recursively parse an XML element to dict."""
        result = {}
        
        # Add attributes
        if element.attrib:
            for attr_name, attr_value in element.attrib.items():
                result[f"@{attr_name}"] = attr_value
        
        # Process children
        children = list(element)
        if children:
            # Group children by tag name
            child_dict = {}
            for child in children:
                child_data = parse_element(child)
                tag = child.tag
                
                # Handle namespace by stripping it
                if '}' in tag:
                    tag = tag.split('}')[-1]
                
                if tag in child_dict:
                    # Convert to list if multiple children with same tag
                    if not isinstance(child_dict[tag], list):
                        child_dict[tag] = [child_dict[tag]]
                    child_dict[tag].append(child_data)
                else:
                    child_dict[tag] = child_data
            
            # Merge with result
            for key, value in child_dict.items():
                result[key] = value
        
        # Add text content
        if element.text and element.text.strip():
            text = element.text.strip()
            # If there are children, text goes to '#text'
            if children or element.attrib:
                result['#text'] = text
            else:
                # No children or attributes, just return the text
                return text
        
        return result if result else None
    
    try:
        # Parse XML with ElementTree (more forgiving than xmltodict)
        root = ET.fromstring(xml_string)
        
        # Get root tag name (strip namespace)
        root_tag = root.tag
        if '}' in root_tag:
            root_tag = root_tag.split('}')[-1]
        
        # Parse root element
        result = {root_tag: parse_element(root)}
        
        # Clean up empty values
        def clean_empty(obj):
            if isinstance(obj, dict):
                return {k: clean_empty(v) for k, v in obj.items() if v is not None and v != {} and v != []}
            elif isinstance(obj, list):
                return [clean_empty(item) for item in obj if item is not None and item != {} and item != []]
            return obj
        
        return clean_empty(result)
        
    except ET.ParseError as e:
        raise Exception(f"XML parsing error: {str(e)}")


# ---------- Conversion functions ----------
def yaml_to_dict(s):
    return yaml.safe_load(s)


def dict_to_yaml(d, indent=2):
    return yaml.dump(d, default_flow_style=False, indent=indent, allow_unicode=True)


def json_to_dict(s):
    return json.loads(s)


def dict_to_json(d, indent=2):
    return json.dumps(d, indent=indent, ensure_ascii=False, cls=CustomJSONEncoder)


def xml_to_dict(s):
    """Convert XML to dict using custom parser (handles complex structures)."""
    try:
        # First try with custom parser (handles nested structures better)
        result = custom_xml_to_dict(s)
        if result and isinstance(result, dict) and len(result) == 1:
            return list(result.values())[0]
        return result
    except Exception as e1:
        # Fallback to xmltodict if custom parser fails
        try:
            result = xmltodict.parse(s, force_cdata=True, dict_constructor=dict)
            if isinstance(result, dict) and len(result) == 1:
                return list(result.values())[0]
            return result
        except Exception as e2:
            raise Exception(f"XML parsing failed. Custom parser error: {str(e1)}\nxmltodict error: {str(e2)}")


def dict_to_xml(data, root_tag="root"):
    """Convert Python dict to XML."""
    def add_ids(obj, path=""):
        if isinstance(obj, list):
            for idx, item in enumerate(obj, start=1):
                if isinstance(item, dict):
                    if "@id" not in item:
                        item["@id"] = str(idx)
                else:
                    obj[idx-1] = {"@id": str(idx), "#text": str(item)}
            for item in obj:
                add_ids(item, path)
        elif isinstance(obj, dict):
            for k, v in list(obj.items()):
                if not k.startswith('@'):
                    add_ids(v, path + "/" + k)
        return obj
    
    if data is None:
        return f"<{root_tag}/>"
    
    if not isinstance(data, dict):
        data = {root_tag: data}
    else:
        data = {root_tag: copy.deepcopy(data)}
    
    # Clean up None values
    def clean_none(obj):
        if isinstance(obj, dict):
            return {k: clean_none(v) for k, v in obj.items() if v is not None}
        elif isinstance(obj, list):
            return [clean_none(item) for item in obj if item is not None]
        return obj
    
    data = clean_none(data)
    processed = copy.deepcopy(data)
    add_ids(processed)
    
    try:
        result = xmltodict.unparse(processed, pretty=True, short_empty_elements=True)
        if not result.startswith('<?xml'):
            result = '<?xml version="1.0" encoding="UTF-8"?>\n' + result
        return result
    except Exception as e:
        # If xmltodict fails, try a simpler approach
        try:
            from dicttoxml import dicttoxml
            xml_bytes = dicttoxml.dicttoxml(data, custom_root=root_tag, attr_type=False)
            result = xml_bytes.decode('utf-8')
            try:
                dom = minidom.parseString(result)
                result = dom.toprettyxml(indent="  ")
                result = '\n'.join([line for line in result.split('\n') if line.strip()])
            except:
                pass
            return result
        except ImportError:
            return f"<error>Failed to convert to XML: {str(e)}</error>"


# ---------- Main Window ----------
class MegaConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JyxOps - YAML | JSON | XML Converter")
        
        # Set window icon (if exists)
        icon_path = resource_path("resources/logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setGeometry(100, 100, 1500, 800)

        self.settings = SettingsManager()
        self.last_export_dir = self.settings.get_last_export_dir()

        # Load per-editor font sizes
        self.yaml_font_size = self.settings.get_font_size("yaml")
        self.json_font_size = self.settings.get_font_size("json")
        self.xml_font_size = self.settings.get_font_size("xml")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Drop area
        drop_group = QGroupBox("Drag & Drop a YAML, JSON, or XML file")
        drop_layout = QVBoxLayout(drop_group)
        self.drop_label = QLabel("📂 Drag file here\nor use toolbar to open")
        self.drop_label.setObjectName("drop_label")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setAcceptDrops(True)
        self.drop_label.dragEnterEvent = self.dragEnterEvent
        self.drop_label.dropEvent = self.dropEvent
        drop_layout.addWidget(self.drop_label)
        main_layout.addWidget(drop_group)

        # Triple splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.yaml_edit = self._create_editor("YAML", self.yaml_font_size)
        splitter.addWidget(self.yaml_edit[0])
        self.json_edit = self._create_editor("JSON", self.json_font_size)
        splitter.addWidget(self.json_edit[0])
        self.xml_edit = self._create_editor("XML", self.xml_font_size)
        splitter.addWidget(self.xml_edit[0])

        main_layout.addWidget(splitter, stretch=1)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        open_action = QAction("📂 Open", self)
        open_action.triggered.connect(self.load_file_dialog)
        toolbar.addAction(open_action)

        export_yaml = QAction("💾 Export YAML", self)
        export_yaml.triggered.connect(lambda: self.export_current("yaml"))
        toolbar.addAction(export_yaml)
        export_json = QAction("💾 Export JSON", self)
        export_json.triggered.connect(lambda: self.export_current("json"))
        toolbar.addAction(export_json)
        export_xml = QAction("💾 Export XML", self)
        export_xml.triggered.connect(lambda: self.export_current("xml"))
        toolbar.addAction(export_xml)
        export_all = QAction("💾📁 Export All", self)
        export_all.triggered.connect(self.export_all)
        toolbar.addAction(export_all)

        toolbar.addSeparator()
        pretty_action = QAction("✨ Pretty Print", self)
        pretty_action.triggered.connect(self.pretty_print_current)
        pretty_action.setShortcut(QKeySequence("Ctrl+Shift+F"))
        toolbar.addAction(pretty_action)

        batch_action = QAction("📁 Batch Convert", self)
        batch_action.triggered.connect(self.open_batch_converter)
        batch_action.setShortcut(QKeySequence("Ctrl+B"))
        toolbar.addAction(batch_action)

        learn_action = QAction("📚 Learning Center", self)
        learn_action.triggered.connect(self.open_learning_center)
        learn_action.setShortcut(QKeySequence("Ctrl+L"))
        toolbar.addAction(learn_action)

        help_action = QAction("❓ Shortcuts", self)
        help_action.triggered.connect(self.show_shortcuts)
        help_action.setShortcut(QKeySequence("Ctrl+?"))
        toolbar.addAction(help_action)

        toolbar.addSeparator()
        self.undo_action = QAction("↩ Undo", self)
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        toolbar.addAction(self.undo_action)
        self.redo_action = QAction("↪ Redo", self)
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setShortcuts([QKeySequence.StandardKey.Redo, QKeySequence("Ctrl+Y")])
        toolbar.addAction(self.redo_action)

        toolbar.addSeparator()
        find_action = QAction("🔍 Find", self)
        find_action.triggered.connect(self.show_find)
        find_action.setShortcut(QKeySequence.StandardKey.Find)
        toolbar.addAction(find_action)
        replace_action = QAction("🔄 Replace", self)
        replace_action.triggered.connect(self.show_replace)
        replace_action.setShortcut(QKeySequence.StandardKey.Replace)
        toolbar.addAction(replace_action)

        toolbar.addSeparator()
        clear_action = QAction("🗑 Clear All", self)
        clear_action.triggered.connect(self.clear_all)
        toolbar.addAction(clear_action)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        self.format_selector = QComboBox()
        self.format_selector.addItems(["YAML", "JSON", "XML"])
        self.format_selector.setCurrentText(self.settings.get_default_format().upper())
        self.format_selector.currentTextChanged.connect(self.on_default_format_changed)
        self.status_bar.addPermanentWidget(QLabel("  Default format:"))
        self.status_bar.addPermanentWidget(self.format_selector)

        # Internal state
        self._updating = False
        self._conversion_pending = False
        self._source = None
        self.current_data = None
        self.find_dialog = None

        # Syntax highlighting
        self.yaml_highlighter = YamlJsonHighlighter(self.yaml_edit[1].document())
        self.json_highlighter = YamlJsonHighlighter(self.json_edit[1].document())
        self.xml_highlighter = YamlJsonHighlighter(self.xml_edit[1].document())

        self.setStyleSheet(DARK_THEME)

        splitter_sizes = self.settings.get_splitter_sizes()
        if splitter_sizes:
            splitter.setSizes([int(s) for s in splitter_sizes])

    def _create_editor(self, title, font_size):
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        editor = IndentedTextEdit()
        editor.setPlaceholderText(f"{title} code...")
        editor.textChanged.connect(lambda: self.on_editor_changed(title.lower()))
        editor.set_font_size(font_size)
        layout.addWidget(editor)
        copy_btn = QPushButton(f"📋 Copy {title}")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(editor))
        layout.addWidget(copy_btn)
        return group, editor

    def open_learning_center(self):
        """Open the Learning Center dialog."""
        dialog = LearningCenterDialog(self)
        dialog.show()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            self.load_file(Path(urls[0].toLocalFile()))

    def load_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Data File", self.settings.get("last_open_dir", ""),
            "Data Files (*.yaml *.yml *.json *.xml)"
        )
        if file_path:
            self.settings.set("last_open_dir", str(Path(file_path).parent))
            self.load_file(Path(file_path))

    def load_file(self, path: Path):
        try:
            content = path.read_text(encoding="utf-8")
            suffix = path.suffix.lower()
            
            if suffix in (".yaml", ".yml"):
                data = yaml_to_dict(content)
            elif suffix == ".json":
                data = json_to_dict(content)
            elif suffix == ".xml":
                data = xml_to_dict(content)
                if isinstance(data, dict) and len(data) == 1:
                    data = list(data.values())[0]
            else:
                QMessageBox.warning(self, "Unsupported", f"Cannot handle {suffix} files.")
                return
            
            self._set_all_texts(data)
            self.current_data = data

            self.yaml_edit[1].set_font_size(self.yaml_edit[1].font_size)
            self.json_edit[1].set_font_size(self.json_edit[1].font_size)
            self.xml_edit[1].set_font_size(self.xml_edit[1].font_size)

            self.status_bar.showMessage(f"Loaded {path.name}", 3000)
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Load Error", f"Failed to load file:\n{str(e)}")

    def on_editor_changed(self, source):
        if self._updating:
            return
        self._source = source
        if not self._conversion_pending:
            self._conversion_pending = True
            QTimer.singleShot(50, self._perform_conversion)

    def _perform_conversion(self):
        self._conversion_pending = False
        source = self._source
        if self._updating:
            return
        editor = getattr(self, f"{source}_edit")[1]
        txt = editor.toPlainText().strip()
        if not txt:
            self._clear_all_editors()
            return
        try:
            if source == "yaml":
                data = yaml_to_dict(txt)
            elif source == "json":
                data = json_to_dict(txt)
            else:
                data = xml_to_dict(txt)
                if isinstance(data, dict) and len(data) == 1:
                    data = list(data.values())[0]
            self._update_others(source, data)
            editor.setStyleSheet("")
        except Exception as e:
            editor.setStyleSheet("border: 1px solid red;")
            self.status_bar.showMessage(f"{source.upper()} error: {str(e)}", 4000)

    def _update_others(self, source, data):
        self.current_data = data
        self._updating = True
        try:
            if source != "yaml":
                self.yaml_edit[1].setPlainText(dict_to_yaml(data))
            if source != "json":
                self.json_edit[1].setPlainText(dict_to_json(data))
            if source != "xml":
                self.xml_edit[1].setPlainText(dict_to_xml(data))
        finally:
            self._updating = False
        self.status_bar.showMessage(f"{source.upper()} → others updated", 1000)

    def _set_all_texts(self, data):
        self._updating = True
        try:
            self.yaml_edit[1].setPlainText(dict_to_yaml(data))
            self.json_edit[1].setPlainText(dict_to_json(data))
            self.xml_edit[1].setPlainText(dict_to_xml(data))
        finally:
            self._updating = False

    def _clear_all_editors(self):
        self._updating = True
        try:
            self.yaml_edit[1].clear()
            self.json_edit[1].clear()
            self.xml_edit[1].clear()
        finally:
            self._updating = False
        self.current_data = None
        self.status_bar.showMessage("Cleared", 2000)

    def copy_to_clipboard(self, editor):
        text = editor.toPlainText()
        if text:
            QGuiApplication.clipboard().setText(text)
            self.status_bar.showMessage("Copied to clipboard", 2000)
        else:
            self.status_bar.showMessage("Nothing to copy", 1000)

    def pretty_print_current(self):
        focus = self.focusWidget()
        if not isinstance(focus, IndentedTextEdit):
            self.status_bar.showMessage("Click inside an editor first", 2000)
            return
        text = focus.toPlainText().strip()
        if not text:
            return
        if focus == self.yaml_edit[1]:
            try:
                data = yaml_to_dict(text)
                focus.setPlainText(dict_to_yaml(data))
                self.status_bar.showMessage("YAML pretty printed", 2000)
            except:
                self.status_bar.showMessage("Invalid YAML", 3000)
        elif focus == self.json_edit[1]:
            try:
                data = json_to_dict(text)
                focus.setPlainText(dict_to_json(data))
                self.status_bar.showMessage("JSON pretty printed", 2000)
            except:
                self.status_bar.showMessage("Invalid JSON", 3000)
        elif focus == self.xml_edit[1]:
            try:
                dom = minidom.parseString(text)
                pretty = dom.toprettyxml(indent="  ")
                pretty = '\n'.join([line for line in pretty.split('\n') if line.strip()])
                focus.setPlainText(pretty)
                self.status_bar.showMessage("XML pretty printed", 2000)
            except:
                self.status_bar.showMessage("Invalid XML", 3000)

    def show_find(self):
        focus = self.focusWidget()
        if isinstance(focus, IndentedTextEdit):
            if self.find_dialog:
                self.find_dialog.close()
            self.find_dialog = FindReplaceDialog(focus, self)
            self.find_dialog.show()
        else:
            self.status_bar.showMessage("Focus an editor first", 2000)

    def show_replace(self):
        self.show_find()

    def open_batch_converter(self):
        dialog = BatchConverterDialog(self)
        dialog.exec()

    def export_current(self, format_type: str):
        if self.current_data is None:
            QMessageBox.information(self, "No Data", "Nothing to export.")
            return
        if format_type == "yaml":
            content = dict_to_yaml(self.current_data)
            ext = ".yaml"
        elif format_type == "json":
            content = dict_to_json(self.current_data)
            ext = ".json"
        else:
            content = dict_to_xml(self.current_data)
            ext = ".xml"
        file_path, _ = QFileDialog.getSaveFileName(
            self, f"Export {format_type.upper()}", self.last_export_dir,
            f"{format_type.upper()} Files (*{ext})"
        )
        if file_path:
            Path(file_path).write_text(content, encoding="utf-8")
            self.last_export_dir = str(Path(file_path).parent)
            self.settings.set_last_export_dir(self.last_export_dir)
            self.status_bar.showMessage(f"Exported {Path(file_path).name}", 3000)

    def export_all(self):
        if self.current_data is None:
            QMessageBox.information(self, "No Data", "Nothing to export.")
            return
        reply = QMessageBox.question(self, "Export All",
                                     "Export as ZIP archive? (Yes = ZIP, No = folder)",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if reply == QMessageBox.StandardButton.Yes:
            zip_path, _ = QFileDialog.getSaveFileName(
                self, "Save ZIP Archive", self.last_export_dir,
                "ZIP Files (*.zip)"
            )
            if zip_path:
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_dir = Path(tmpdir)
                    (tmp_dir / "data.yaml").write_text(dict_to_yaml(self.current_data), encoding="utf-8")
                    (tmp_dir / "data.json").write_text(dict_to_json(self.current_data), encoding="utf-8")
                    (tmp_dir / "data.xml").write_text(dict_to_xml(self.current_data), encoding="utf-8")
                    with zipfile.ZipFile(zip_path, 'w') as zf:
                        for f in tmp_dir.iterdir():
                            zf.write(f, arcname=f.name)
                self.status_bar.showMessage(f"Exported to {Path(zip_path).name}", 3000)
        else:
            export_dir = Path(self.last_export_dir) / f"export_{timestamp}"
            export_dir.mkdir(exist_ok=True)
            (export_dir / "data.yaml").write_text(dict_to_yaml(self.current_data), encoding="utf-8")
            (export_dir / "data.json").write_text(dict_to_json(self.current_data), encoding="utf-8")
            (export_dir / "data.xml").write_text(dict_to_xml(self.current_data), encoding="utf-8")
            self.status_bar.showMessage(f"Exported to folder {export_dir}", 5000)

    def undo(self):
        focus = self.focusWidget()
        if isinstance(focus, IndentedTextEdit):
            focus.undo()
            self.status_bar.showMessage("Undo", 1000)
            self._trigger_conversion_from_focus(focus)

    def redo(self):
        focus = self.focusWidget()
        if isinstance(focus, IndentedTextEdit):
            focus.redo()
            self.status_bar.showMessage("Redo", 1000)
            self._trigger_conversion_from_focus(focus)

    def _trigger_conversion_from_focus(self, editor):
        if editor == self.yaml_edit[1]:
            self.on_editor_changed("yaml")
        elif editor == self.json_edit[1]:
            self.on_editor_changed("json")
        elif editor == self.xml_edit[1]:
            self.on_editor_changed("xml")

    def clear_all(self):
        self._clear_all_editors()

    def on_default_format_changed(self, fmt):
        self.settings.set_default_format(fmt.lower())

    def show_shortcuts(self):
        dialog = ShortcutDialog(self)
        dialog.exec()

    def closeEvent(self, event):
        self.settings.set_font_size("yaml", self.yaml_edit[1].font_size)
        self.settings.set_font_size("json", self.json_edit[1].font_size)
        self.settings.set_font_size("xml", self.xml_edit[1].font_size)
        splitter = self.findChild(QSplitter)
        if splitter:
            self.settings.set_splitter_sizes(splitter.sizes())
        event.accept()


# ---------- Main function ----------
def main():
    # Suppress Qt font warnings
    os.environ["QT_LOGGING_RULES"] = "qt.text.font.db=false"
    
    app = QApplication(sys.argv)
    
    # Set Windows taskbar icon (Windows only)
    if sys.platform == 'win32':
        import ctypes
        myappid = 'jyxops.converter.v2.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app.setStyle("Fusion")
    window = MegaConverter()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()