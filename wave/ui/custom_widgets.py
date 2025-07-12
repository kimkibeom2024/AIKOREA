from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class HoverableImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)