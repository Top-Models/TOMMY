
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea


class FetchedTopicsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setMinimumSize(195, 400)
        self.setStyleSheet("background-color: white;")

        # Initialize layout for scroll area
        self.scroll_area = QWidget()
        self.layout = QVBoxLayout(self.scroll_area)
        self.layout.setAlignment(Qt.AlignCenter)

        # Initialize topics
        self.first_topic = QLabel("First Topic")
        self.first_topic.setStyleSheet("background-color: #E40046;"
                                       "color: #FED800")
        self.first_topic.setFixedSize(200, 100)
        self.first_topic.setAlignment(Qt.AlignCenter)

        self.second_topic = QLabel("Second Topic")
        self.second_topic.setStyleSheet("background-color: #E40046;"
                                        "color: #FFA300")
        self.second_topic.setFixedSize(200, 100)
        self.second_topic.setAlignment(Qt.AlignCenter)

        self.third_topic = QLabel("Third Topic")
        self.third_topic.setStyleSheet("background-color: #E40046;"
                                       "color: #FED800")
        self.third_topic.setFixedSize(200, 100)
        self.third_topic.setAlignment(Qt.AlignCenter)

        self.fourth_topic = QLabel("Fourth Topic")
        self.fourth_topic.setStyleSheet("background-color: #E40046;"
                                        "color: #FFA300")
        self.fourth_topic.setFixedSize(200, 100)
        self.fourth_topic.setAlignment(Qt.AlignCenter)

        self.fifth_topic = QLabel("Fifth Topic")
        self.fifth_topic.setStyleSheet("background-color: #E40046;"
                                       "color: #FED800")
        self.fifth_topic.setFixedSize(200, 100)
        self.fifth_topic.setAlignment(Qt.AlignCenter)

        # Add topics to layout of scroll area
        self.layout.addWidget(self.first_topic)
        self.layout.addWidget(self.second_topic)
        self.layout.addWidget(self.third_topic)
        self.layout.addWidget(self.fourth_topic)
        self.layout.addWidget(self.fifth_topic)

        # Set scroll area as focal point
        self.setWidget(self.scroll_area)

        # Add Scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)











