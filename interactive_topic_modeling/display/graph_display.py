from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class GraphDisplay(QWidget):

    def __init__(self):
        super().__init__()

        # NOTE: initialized widget properties and added widgets for dev team testing purposes

        # Initialize widget properties
        self.setFixedSize(750, 562)
        self.setStyleSheet("background-color: lightgrey;")

        # Initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add widgets
        label = QLabel("Graph display")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

