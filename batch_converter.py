# batch_converter.py
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QFileDialog, QProgressBar, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from pathlib import Path
from converters import yaml_to_dict, dict_to_yaml, json_to_dict, dict_to_json, xml_to_dict, dict_to_xml

class ConverterThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, input_format, output_format):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.input_format = input_format
        self.output_format = output_format

    def run(self):
        try:
            input_ext = f".{self.input_format}"
            output_ext = f".{self.output_format}"
            files = list(Path(self.input_dir).glob(f"*{input_ext}"))
            total = len(files)
            for idx, in_path in enumerate(files):
                try:
                    content = in_path.read_text(encoding="utf-8")
                    if self.input_format == "yaml":
                        data = yaml_to_dict(content)
                    elif self.input_format == "json":
                        data = json_to_dict(content)
                    else:
                        data = xml_to_dict(content)
                        if isinstance(data, dict) and len(data) == 1:
                            data = list(data.values())[0]
                    if self.output_format == "yaml":
                        out_text = dict_to_yaml(data)
                    elif self.output_format == "json":
                        out_text = dict_to_json(data)
                    else:
                        out_text = dict_to_xml(data)   # uses improved function with IDs
                    out_path = Path(self.output_dir) / (in_path.stem + output_ext)
                    out_path.write_text(out_text, encoding="utf-8")
                except Exception as e:
                    self.error.emit(f"Failed {in_path.name}: {str(e)}")
                self.progress.emit(idx+1, in_path.name)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class BatchConverterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Convert Folder")
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)

        # Input folder
        in_layout = QHBoxLayout()
        in_layout.addWidget(QLabel("Input Folder:"))
        self.in_edit = QLineEdit()
        in_layout.addWidget(self.in_edit)
        in_btn = QPushButton("Browse")
        in_btn.clicked.connect(self.browse_input)
        in_layout.addWidget(in_btn)
        layout.addLayout(in_layout)

        # Output folder
        out_layout = QHBoxLayout()
        out_layout.addWidget(QLabel("Output Folder:"))
        self.out_edit = QLineEdit()
        out_layout.addWidget(self.out_edit)
        out_btn = QPushButton("Browse")
        out_btn.clicked.connect(self.browse_output)
        out_layout.addWidget(out_btn)
        layout.addLayout(out_layout)

        # Formats
        fmt_layout = QHBoxLayout()
        fmt_layout.addWidget(QLabel("From:"))
        self.in_fmt = QComboBox()
        self.in_fmt.addItems(["yaml", "json", "xml"])
        fmt_layout.addWidget(self.in_fmt)
        fmt_layout.addWidget(QLabel("To:"))
        self.out_fmt = QComboBox()
        self.out_fmt.addItems(["yaml", "json", "xml"])
        fmt_layout.addWidget(self.out_fmt)
        layout.addLayout(fmt_layout)

        # Progress
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        # Buttons
        btn_layout = QHBoxLayout()
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.start_conversion)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.convert_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.thread = None

    def browse_input(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if dir_path:
            self.in_edit.setText(dir_path)

    def browse_output(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if dir_path:
            self.out_edit.setText(dir_path)

    def start_conversion(self):
        if not self.in_edit.text() or not self.out_edit.text():
            self.log.append("Please select input and output folders.")
            return
        self.convert_btn.setEnabled(False)
        self.thread = ConverterThread(
            self.in_edit.text(), self.out_edit.text(),
            self.in_fmt.currentText(), self.out_fmt.currentText()
        )
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.conversion_finished)
        self.thread.error.connect(self.log.append)
        self.thread.start()

    def update_progress(self, current, filename):
        self.progress_bar.setValue(int(current / self.progress_bar.maximum() * 100))
        self.log.append(f"Converted {filename}")

    def conversion_finished(self):
        self.log.append("✅ Conversion complete.")
        self.convert_btn.setEnabled(True)
        self.progress_bar.reset()