
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea


class FetchedTopicsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setMinimumSize(195, 400)
        self.setStyleSheet("background-color: white;")

        # Initialize layout and scroll area
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # Initialize Topics
        self.first_topic = QWidget()
        self.first_topic.setStyleSheet("background-color: black;")
        self.first_topic.setFixedSize(200, 100)

        self.second_topic = QLabel()
        self.second_topic.setStyleSheet("background-color: pink;")
        self.second_topic.setFixedSize(200, 100)

        self.third_topic = QLabel()
        self.third_topic.setStyleSheet("background-color: green;")
        self.third_topic.setFixedSize(200, 100)

        self.fourth_topic = QLabel()
        self.fourth_topic.setStyleSheet("background-color: red;")
        self.fourth_topic.setFixedSize(200, 100)

        self.fifth_topic = QLabel()
        self.fifth_topic.setStyleSheet("background-color: green;")
        self.fifth_topic.setFixedSize(200, 100)

        # Add widgets
        self.layout.addWidget(self.first_topic)
        self.layout.addWidget(self.second_topic)
        self.layout.addWidget(self.third_topic)
        self.layout.addWidget(self.fourth_topic)
        self.layout.addWidget(self.fifth_topic)

        self.setWidget(self.widget)

        # Add Scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)











