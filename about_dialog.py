# about_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton

class ShortcutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Shortcuts & Help")
        self.setFixedSize(500, 400)
        layout = QVBoxLayout(self)
        text = QTextBrowser()
        text.setHtml("""
        <h2>Mega Converter Shortcuts</h2>
        <table border='0' cellpadding='5'>
        <tr><td><b>Ctrl+O</b></td><td>Open file</td></tr>
        <tr><td><b>Ctrl+S</b></td><td>Export current format</td></tr>
        <tr><td><b>Ctrl+Shift+S</b></td><td>Export all formats (ZIP/folder)</td></tr>
        <tr><td><b>Ctrl+Z</b></td><td>Undo</td></tr>
        <tr><td><b>Ctrl+Y / Ctrl+Shift+Z</b></td><td>Redo</td></tr>
        <tr><td><b>Ctrl+F</b></td><td>Find</td></tr>
        <tr><td><b>Ctrl+H</b></td><td>Replace</td></tr>
        <tr><td><b>Ctrl+Mouse Wheel</b></td><td>Zoom in/out</td></tr>
        <tr><td><b>Shift+Mouse Wheel</b></td><td>Horizontal scroll</td></tr>
        <tr><td><b>Ctrl+Shift+F</b></td><td>Pretty print current panel</td></tr>
        <tr><td><b>Ctrl+Shift+W</b></td><td>Toggle file watcher</td></tr>
        <tr><td><b>Ctrl+B</b></td><td>Batch convert folder</td></tr>
        </table>
        <p>Drag & drop a file anywhere to load it.</p>
        """)
        layout.addWidget(text)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)