
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from interactive_topic_modeling.display.topic_display.topic_entity import TopicEntity


class FetchedTopicsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setMinimumSize(195, 400)
        self.setStyleSheet("background-color: white;")

        # Initialize topic container
        self.topic_container = []

        # Initialize layout for scroll area
        self.scroll_area = QWidget()
        self.layout = QVBoxLayout(self.scroll_area)
        self.layout.setAlignment(Qt.AlignCenter)

        # Initialize topics
        for i in range(10):
            self.topic_container.append(TopicEntity(f"Topic {i}", [f"Word {i}", f"Word {i+1}", f"Word {i+2}", f"Word {i+3}"]))
            self.layout.addWidget(self.topic_container[-1])

        # Set scroll area as focal point
        self.setWidget(self.scroll_area)

        # Add Scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def add_topic(self, topic_name: str, topic_words: list[str]) -> None:
        """
        Add a topic to the display
        :param topic_name: Name of the topic
        :param topic_words: Words associated with the topic
        :return: None
        """

        self.topic_container.append(TopicEntity(topic_name, topic_words))
        self.layout.addWidget(self.topic_container[-1])











