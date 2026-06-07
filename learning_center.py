# learning_center.py - Beautiful version with syntax highlighting
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QTextBrowser, QPushButton, QLabel, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def load_and_convert_md(filename):
    """Load markdown file and convert to HTML with syntax highlighting."""
    try:
        # Try multiple possible paths
        possible_paths = [
            Path("LearnHub") / filename,
            Path(__file__).parent / "LearnHub" / filename,
            Path.cwd() / "LearnHub" / filename,
        ]
        
        md_content = None
        for md_path in possible_paths:
            if md_path.exists():
                md_content = md_path.read_text(encoding="utf-8")
                break
        
        if md_content is None:
            return f"""
            <div style="padding: 40px; text-align: center;">
                <h1 style="color: #ff5555;">⚠️ File Not Found</h1>
                <p>Could not find <code>LearnHub/{filename}</code></p>
                <p>Expected path: {possible_paths[0]}</p>
            </div>
            """
        
        # Convert markdown to HTML with code highlighting
        html = markdown.markdown(
            md_content,
            extensions=['extra', 'codehilite', 'tables', 'fenced_code']
        )
        
        # Get pygments CSS
        formatter = HtmlFormatter(style='monokai')
        pygments_css = formatter.get_style_defs('.codehilite')
        
        # Complete HTML with beautiful styling
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                }}
                
                body {{
                    background-color: #0a0e1a;
                    color: #e4e4e7;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
                    font-size: 15px;
                    line-height: 1.6;
                    padding: 30px 40px;
                    margin: 0;
                }}
                
                /* Typography */
                h1 {{
                    color: #50fa7b;
                    font-size: 2.2em;
                    border-bottom: 3px solid #50fa7b;
                    padding-bottom: 12px;
                    margin-top: 0;
                    margin-bottom: 25px;
                    font-weight: 600;
                }}
                
                h2 {{
                    color: #8be9fd;
                    font-size: 1.6em;
                    margin-top: 35px;
                    margin-bottom: 15px;
                    padding-left: 10px;
                    border-left: 4px solid #8be9fd;
                    font-weight: 500;
                }}
                
                h3 {{
                    color: #ffb86c;
                    font-size: 1.3em;
                    margin-top: 25px;
                    margin-bottom: 12px;
                    font-weight: 500;
                }}
                
                /* Code blocks */
                .codehilite {{
                    background-color: #1a1f2e;
                    border-radius: 8px;
                    padding: 16px;
                    margin: 20px 0;
                    overflow-x: auto;
                    border: 1px solid #2d3a5e;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                }}
                
                .codehilite pre {{
                    margin: 0;
                    padding: 0;
                    background: transparent;
                }}
                
                .codehilite code {{
                    font-family: 'Fira Code', 'Courier New', 'Consolas', monospace;
                    font-size: 13px;
                    line-height: 1.5;
                }}
                
                /* Inline code */
                code {{
                    background-color: #1e2438;
                    color: #f1fa8c;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: 'Fira Code', 'Courier New', monospace;
                    font-size: 0.9em;
                }}
                
                /* Tables */
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background-color: #111520;
                    border-radius: 8px;
                    overflow: hidden;
                }}
                
                th {{
                    background-color: #1e2a3a;
                    color: #50fa7b;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                    border-bottom: 2px solid #50fa7b;
                }}
                
                td {{
                    padding: 10px 12px;
                    border-bottom: 1px solid #2d3a5e;
                }}
                
                tr:hover {{
                    background-color: #1a2035;
                }}
                
                /* Lists */
                ul, ol {{
                    margin: 15px 0;
                    padding-left: 30px;
                }}
                
                li {{
                    margin: 8px 0;
                }}
                
                /* Blockquotes */
                blockquote {{
                    border-left: 4px solid #ffb86c;
                    background-color: #1a1f2e;
                    padding: 12px 20px;
                    margin: 20px 0;
                    border-radius: 0 8px 8px 0;
                    font-style: italic;
                    color: #c4c4d4;
                }}
                
                /* Links */
                a {{
                    color: #8be9fd;
                    text-decoration: none;
                    border-bottom: 1px dotted #8be9fd;
                }}
                
                a:hover {{
                    color: #50fa7b;
                    border-bottom-color: #50fa7b;
                }}
                
                /* Horizontal rule */
                hr {{
                    border: none;
                    height: 1px;
                    background: linear-gradient(90deg, #50fa7b, transparent);
                    margin: 30px 0;
                }}
                
                /* Badges / Notes */
                .note {{
                    background: linear-gradient(135deg, #1e2a3a, #111520);
                    border-left: 4px solid #ffb86c;
                    padding: 15px 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                }}
                
                /* Scrollbar */
                ::-webkit-scrollbar {{
                    width: 10px;
                    height: 10px;
                }}
                
                ::-webkit-scrollbar-track {{
                    background: #1a1f2e;
                }}
                
                ::-webkit-scrollbar-thumb {{
                    background: #50fa7b;
                    border-radius: 5px;
                }}
                
                ::-webkit-scrollbar-thumb:hover {{
                    background: #8be9fd;
                }}
                
                /* Responsive */
                @media (max-width: 768px) {{
                    body {{
                        padding: 20px;
                        font-size: 14px;
                    }}
                    
                    h1 {{
                        font-size: 1.8em;
                    }}
                    
                    h2 {{
                        font-size: 1.4em;
                    }}
                }}
                
                {pygments_css}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        return styled_html
        
    except Exception as e:
        return f"""
        <div style="padding: 40px; text-align: center; color: #ff5555;">
            <h2>❌ Error Loading Tutorial</h2>
            <p>Failed to load {filename}: {str(e)}</p>
        </div>
        """


class LearningCenterDialog(QDialog):
    """Beautiful Learning Center window with syntax highlighting."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📚 JyxOps Learning Center - Master YAML, JSON & XML")
        self.setGeometry(150, 80, 1000, 750)
        self.setMinimumSize(800, 600)
        
        # Set window flags
        self.setWindowFlags(Qt.WindowType.Window)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #0a0e1a; border-bottom: 1px solid #2d3a5e;")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        title = QLabel("📖 JyxOps Learning Center")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #50fa7b;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Comprehensive tutorials for YAML, JSON, and XML with examples")
        subtitle.setStyleSheet("color: #8be9fd; font-size: 12px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_widget)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                background-color: #0a0e1a;
                border: none;
            }
            QTabBar::tab {
                background-color: #111520;
                color: #e4e4e7;
                padding: 10px 24px;
                margin-right: 2px;
                font-size: 13px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #50fa7b;
                color: #0a0e1a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #1e2a3a;
            }
        """)
        
        # Load tutorials
        self._add_tutorial_tab("YAML", "yaml.md", "🎯")
        self._add_tutorial_tab("JSON", "json.md", "💎")
        self._add_tutorial_tab("XML", "xml.md", "📄")
        
        layout.addWidget(self.tab_widget, stretch=1)
        
        # Bottom bar
        bottom_widget = QWidget()
        bottom_widget.setStyleSheet("background-color: #0a0e1a; border-top: 1px solid #2d3a5e;")
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(20, 10, 20, 10)
        
        # Status label
        self.status_label = QLabel("✨ Ready - Tutorials loaded")
        self.status_label.setStyleSheet("color: #8be9fd; font-size: 11px;")
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e2a3a;
                color: #e4e4e7;
                border: 1px solid #2d3a5e;
                border-radius: 5px;
                padding: 6px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2d3a5e;
                border-color: #50fa7b;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_tutorials)
        
        # Close button
        close_btn = QPushButton("✖ Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff7777;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(refresh_btn)
        bottom_layout.addWidget(close_btn)
        layout.addWidget(bottom_widget)
        
        # Set dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: #0a0e1a;
            }
        """)
    
    def _add_tutorial_tab(self, name, filename, emoji):
        """Add a tutorial tab with content."""
        tab = QTextBrowser()
        tab.setHtml(load_and_convert_md(filename))
        tab.setOpenExternalLinks(True)
        
        # Set text browser style
        tab.setStyleSheet("""
            QTextBrowser {
                background-color: #0a0e1a;
                border: none;
            }
        """)
        
        self.tab_widget.addTab(tab, f"{emoji} {name}")
    
    def refresh_tutorials(self):
        """Reload all tutorials from disk."""
        try:
            # Reload YAML
            self.tab_widget.widget(0).setHtml(load_and_convert_md("yaml.md"))
            # Reload JSON
            self.tab_widget.widget(1).setHtml(load_and_convert_md("json.md"))
            # Reload XML
            self.tab_widget.widget(2).setHtml(load_and_convert_md("xml.md"))
            
            self.status_label.setText("✅ Tutorials refreshed!")
            self.status_label.setStyleSheet("color: #50fa7b; font-size: 11px;")
            
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(3000, lambda: self.status_label.setText("✨ Ready - Tutorials loaded"))
            QTimer.singleShot(3000, lambda: self.status_label.setStyleSheet("color: #8be9fd; font-size: 11px;"))
            
        except Exception as e:
            self.status_label.setText(f"❌ Error refreshing: {str(e)}")
            self.status_label.setStyleSheet("color: #ff5555; font-size: 11px;")
    
    def keyPressEvent(self, event):
        """Handle ESC key to close."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)