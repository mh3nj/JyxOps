# settings_manager.py
import json
from PyQt6.QtCore import QSettings

class SettingsManager:
    def __init__(self):
        self.settings = QSettings("MegaConverter", "Settings")

    def get(self, key, default=None):
        return self.settings.value(key, default)

    def set(self, key, value):
        self.settings.setValue(key, value)

    def get_last_export_dir(self):
        return self.get("last_export_dir", "")

    def set_last_export_dir(self, path):
        self.set("last_export_dir", path)

    def get_font_size(self, editor_name="yaml"):
        sizes = self.get("font_sizes", {})
        if isinstance(sizes, str):
            import json
            try:
                sizes = json.loads(sizes)
            except:
                sizes = {}
        return sizes.get(editor_name, 10)

    def set_font_size(self, editor_name, size):
        sizes = self.get("font_sizes", {})
        if isinstance(sizes, str):
            import json
            try:
                sizes = json.loads(sizes)
            except:
                sizes = {}
        sizes[editor_name] = size
        self.set("font_sizes", sizes)

    def get_splitter_sizes(self):
        return self.get("splitter_sizes", [])

    def set_splitter_sizes(self, sizes):
        self.set("splitter_sizes", sizes)

    def get_default_format(self):
        return self.get("default_format", "yaml")

    def set_default_format(self, fmt):
        self.set("default_format", fmt)

    def get_file_watcher_enabled(self):
        return self.get("file_watcher_enabled", False) in [True, "true"]

    def set_file_watcher_enabled(self, enabled):
        self.set("file_watcher_enabled", "true" if enabled else "false")
