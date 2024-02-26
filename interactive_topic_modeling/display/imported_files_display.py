from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ImportedFilesDisplay(QWidget):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setMinimumSize(450, 200)
        self.setStyleSheet("background-color: lightgrey;")

        # Initialize layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add widgets
        self.label = QLabel("Files Display")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
