from PyQt6.QtCore import QSettings

# In __init__, after setting up UI
self.settings = QSettings("MegaConverter", "Settings")
self.load_theme_preference()