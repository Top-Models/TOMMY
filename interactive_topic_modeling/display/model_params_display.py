from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ModelParamsDisplay(QWidget):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: lightgrey;"
                           "margin: 0px;"
                           "padding: 0px;")

        # Initialize layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Initialize widgets
        self.label = QLabel("Model Parameters Display")
        self.label.setAlignment(Qt.AlignCenter)

        # Add widgets
        self.layout.addWidget(self.label)
