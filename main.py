# main.py – final mega converter without file watcher or HTML copy
import sys
from pathlib import Path
from datetime import datetime
import json
import yaml
import xmltodict
from xml.dom import minidom
import zipfile
import tempfile
import copy

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QFileDialog, QMessageBox, QLabel, QPushButton, QSplitter,
    QToolBar, QStatusBar, QGroupBox, QComboBox
)
from PyQt6.QtCore import Qt, QSettings, QTimer, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QAction, QKeySequence, QGuiApplication

from indented_edit import IndentedTextEdit
from highlighter import YamlJsonHighlighter
from find_replace_dialog import FindReplaceDialog
from themes import DARK_THEME
from settings_manager import SettingsManager
from about_dialog import ShortcutDialog
from batch_converter import BatchConverterDialog

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# ---------- Conversion functions (improved dict_to_xml with IDs) ----------
def yaml_to_dict(s):
    return yaml.safe_load(s)

def dict_to_yaml(d, indent=2):
    return yaml.dump(d, default_flow_style=False, indent=indent, allow_unicode=True)

def json_to_dict(s):
    return json.loads(s)

def dict_to_json(d, indent=2):
    return json.dumps(d, indent=indent, ensure_ascii=False)

def xml_to_dict(s):
    return xmltodict.parse(s)

def dict_to_xml(data, root_tag="root"):
    """Convert Python dict to XML. Lists become repeated elements with id attributes."""
    def add_ids(obj, path=""):
        if isinstance(obj, list):
            for idx, item in enumerate(obj, start=1):
                if isinstance(item, dict):
                    item["@id"] = str(idx)
                else:
                    obj[idx-1] = {"@id": str(idx), "#text": item}
            for item in obj:
                add_ids(item, path)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                add_ids(v, path + "/" + k)
        return obj

    if not isinstance(data, dict):
        data = {root_tag: data}
    else:
        data = {root_tag: data}
    processed = copy.deepcopy(data)
    add_ids(processed)
    return xmltodict.unparse(processed, pretty=True)


# ---------- Main Window ----------
class MegaConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mega Converter – YAML | JSON | XML")
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
        splitter.addWidget(self.yaml_edit[0])  # groupbox
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
        editor.set_font_size(font_size)  # apply saved size
        layout.addWidget(editor)
        copy_btn = QPushButton(f"📋 Copy {title}")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(editor))
        layout.addWidget(copy_btn)
        return group, editor

    # ---------- Drag & Drop ----------
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

            # Reapply font sizes after loading (ensures zoom persists)
            self.yaml_edit[1].set_font_size(self.yaml_edit[1].font_size)
            self.json_edit[1].set_font_size(self.json_edit[1].font_size)
            self.xml_edit[1].set_font_size(self.xml_edit[1].font_size)

            self.status_bar.showMessage(f"Loaded {path.name}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load file:\n{str(e)}")

    # ---------- Live conversion (preserves undo) ----------
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

    # ---------- Copy to clipboard ----------
    def copy_to_clipboard(self, editor):
        text = editor.toPlainText()
        if text:
            QGuiApplication.clipboard().setText(text)
            self.status_bar.showMessage("Copied to clipboard", 2000)
        else:
            self.status_bar.showMessage("Nothing to copy", 1000)

    # ---------- Pretty Print ----------
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

    # ---------- Find / Replace ----------
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

    # ---------- Batch Conversion ----------
    def open_batch_converter(self):
        dialog = BatchConverterDialog(self)
        dialog.exec()

    # ---------- Export ----------
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

    # ---------- Undo/Redo ----------
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

    # ---------- Default format ----------
    def on_default_format_changed(self, fmt):
        self.settings.set_default_format(fmt.lower())

    # ---------- Help ----------
    def show_shortcuts(self):
        dialog = ShortcutDialog(self)
        dialog.exec()

    # ---------- Save settings on close ----------
    def closeEvent(self, event):
        self.settings.set_font_size("yaml", self.yaml_edit[1].font_size)
        self.settings.set_font_size("json", self.json_edit[1].font_size)
        self.settings.set_font_size("xml", self.xml_edit[1].font_size)
        splitter = self.findChild(QSplitter)
        if splitter:
            self.settings.set_splitter_sizes(splitter.sizes())
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MegaConverter()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
