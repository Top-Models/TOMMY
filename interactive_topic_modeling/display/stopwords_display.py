from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea


class StopwordsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: white;")

        # Initialize layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Initialize widgets
        self.label = QLabel("Stopwords Display")
        self.label.setAlignment(Qt.AlignCenter)

        # Add widgets
        self.layout.addWidget(self.label, 0, 0)

