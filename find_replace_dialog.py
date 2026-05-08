from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QTextCursor, QTextDocument   # <-- added QTextDocument

class FindReplaceDialog(QDialog):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Find / Replace")
        self.setModal(False)
        self.setFixedWidth(450)

        layout = QVBoxLayout(self)

        # Find
        hl = QHBoxLayout()
        hl.addWidget(QLabel("Find:"))
        self.find_edit = QLineEdit()
        self.find_edit.textChanged.connect(self.find_next)
        hl.addWidget(self.find_edit)
        layout.addLayout(hl)

        # Replace
        rl = QHBoxLayout()
        rl.addWidget(QLabel("Replace:"))
        self.replace_edit = QLineEdit()
        rl.addWidget(self.replace_edit)
        layout.addLayout(rl)

        # Options
        self.case_sensitive = QCheckBox("Case sensitive")
        self.whole_words = QCheckBox("Whole words")
        self.regex = QCheckBox("Regular expression")
        layout.addWidget(self.case_sensitive)
        layout.addWidget(self.whole_words)
        layout.addWidget(self.regex)

        # Buttons
        bl = QHBoxLayout()
        find_btn = QPushButton("Find Next")
        find_btn.clicked.connect(self.find_next)
        replace_btn = QPushButton("Replace")
        replace_btn.clicked.connect(self.replace)
        replace_all_btn = QPushButton("Replace All")
        replace_all_btn.clicked.connect(self.replace_all)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        bl.addWidget(find_btn)
        bl.addWidget(replace_btn)
        bl.addWidget(replace_all_btn)
        bl.addWidget(close_btn)
        layout.addLayout(bl)

        self.last_find = ""

    def _get_flags(self):
        flags = QTextDocument.FindFlag(0)
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if self.whole_words.isChecked():
            flags |= QTextDocument.FindFlag.FindWholeWords
        return flags

    def find_next(self):
        text = self.find_edit.text()
        if not text:
            return
        flags = self._get_flags()
        ok = self.editor.find(text, flags)
        if not ok:
            # wrap
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            self.editor.setTextCursor(cursor)
            ok = self.editor.find(text, flags)
        if ok:
            self.last_find = text
        else:
            self.parent().status_bar.showMessage("No match found", 2000)

    def replace(self):
        if not self.last_find:
            self.find_next()
            if not self.last_find:
                return
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_edit.text())
            self.find_next()

    def replace_all(self):
        text = self.find_edit.text()
        if not text:
            return
        flags = self._get_flags()
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.editor.setTextCursor(cursor)
        count = 0
        while self.editor.find(text, flags):
            cursor = self.editor.textCursor()
            cursor.insertText(self.replace_edit.text())
            count += 1
        self.parent().status_bar.showMessage(f"Replaced {count} occurrences", 3000)
