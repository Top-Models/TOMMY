from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QLineEdit, QWidget


class ModelParamsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: white;"
                           "margin: 0px;"
                           "padding: 0px;")

        # Initialize layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Initialize container that will hold settings
        self.container = QWidget()
        self.container.setStyleSheet("border: none;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Initialize widgets
        topic_label = QLabel("Number of topics:")
        topic_label.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(topic_label)

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("1")
        self.topic_input.setStyleSheet("border: 2px solid #E40046;")
        self.topic_input.setFixedWidth(208)
        self.topic_input.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.topic_input)

        # Add widgets
        self.layout.addWidget(self.container)
        self.setStyleSheet("border-bottom: 2px solid #E40046;")

