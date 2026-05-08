# themes.py – only dark theme
DARK_THEME = """
    QMainWindow { background-color: #1e1e1e; }
    IndentedTextEdit, QTextEdit {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #555;
        font-family: "Courier New";
        font-size: 10pt;
        selection-background-color: #264f78;
    }
    QToolBar { background-color: #2d2d2d; border: none; }
    QToolButton {
        background-color: #3c3c3c;
        border: 1px solid #666;
        border-radius: 4px;
        padding: 4px 8px;
        color: #f0f0f0;
    }
    QToolButton:hover { background-color: #555; }
    QLabel#drop_label {
        background-color: #2d2d2d;
        border: 2px dashed #888;
        border-radius: 8px;
        color: #ccc;
        font-size: 14pt;
        padding: 20px;
    }
    QGroupBox { font-weight: bold; border: 1px solid #666; margin-top: 10px; color: #eee; }
    QStatusBar { background-color: #1e1e1e; color: #bbb; }
"""
