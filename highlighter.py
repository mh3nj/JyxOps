from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont

class YamlJsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []
        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        self.error_format.setUnderlineColor(QColor(255, 0, 0))

        # Keywords
        kw_fmt = QTextCharFormat()
        kw_fmt.setForeground(QColor("#ff79c6"))
        kw_fmt.setFontWeight(QFont.Weight.Bold)
        for pattern in [r"\btrue\b", r"\bfalse\b", r"\bnull\b"]:
            self.rules.append((QRegularExpression(pattern), kw_fmt))

        # Strings
        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor("#f1fa8c"))
        self.rules.append((QRegularExpression(r"\".*?\""), str_fmt))
        self.rules.append((QRegularExpression(r"\'.*?\'"), str_fmt))

        # Numbers
        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("#8be9fd"))
        self.rules.append((QRegularExpression(r"\b\d+(\.\d+)?\b"), num_fmt))

        # Keys
        key_fmt = QTextCharFormat()
        key_fmt.setForeground(QColor("#50fa7b"))
        self.rules.append((QRegularExpression(r"^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*:"), key_fmt))
        self.rules.append((QRegularExpression(r"\"[a-zA-Z_][a-zA-Z0-9_]*\"\s*:"), key_fmt))

        # XML tags
        tag_fmt = QTextCharFormat()
        tag_fmt.setForeground(QColor("#bd93f9"))
        self.rules.append((QRegularExpression(r"<[^>]+>"), tag_fmt))

        # XML attributes
        attr_fmt = QTextCharFormat()
        attr_fmt.setForeground(QColor("#8be9fd"))
        self.rules.append((QRegularExpression(r"\b[a-zA-Z_:][a-zA-Z0-9_:.-]*\s*="), attr_fmt))

        # Comments
        com_fmt = QTextCharFormat()
        com_fmt.setForeground(QColor("#6272a4"))
        com_fmt.setFontItalic(True)
        self.rules.append((QRegularExpression(r"#.*$"), com_fmt))
        self.rules.append((QRegularExpression(r"<!--.*?-->"), com_fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
        # Error underlining is handled by the editor's red border on syntax error, not here.

    def set_error(self, block, error_pos):
        # For simplicity, we just highlight the whole block (or we could highlight only the error)
        # We'll use red underline for the entire block when error occurs.
        # This is called from main window.
        pass