from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from interactive_topic_modeling.display.topic_display.topic_entity import TopicEntity


class FetchedTopicsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: white;")

        # { tab_name, [(topic_name, [words])] }
        self.topic_container = {}

        # Initialize layout for scroll area
        self.scroll_area = QWidget()
        self.layout = QVBoxLayout(self.scroll_area)
        self.layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # NOTE: These topics are only for demonstration purposes
        self.add_topic("demo_second_tab", "Topic 3", ["word7", "word8", "word9"])
        self.add_topic("demo_second_tab", "Topic 4", ["word10", "word11", "word12"])

        # Set scroll area as focal point
        self.setWidget(self.scroll_area)

        # Add Scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Set default tab
        self.display_topics("init_model")

    def add_topic(self, tab_name: str, topic_name: str, topic_words: list[str]) -> None:
        """
        Add a new topic to the display
        :param tab_name: Name of the tab to add the topic to
        :param topic_name: Name of the topic
        :param topic_words: List of words in the topic
        :return: None
        """

        # Check if tab exists
        if tab_name not in self.topic_container:
            self.topic_container[tab_name] = []

        # Add topic to tab
        self.topic_container[tab_name].append((topic_name, topic_words))

        # Add topic to display
        topic_entity = TopicEntity(topic_name, topic_words)
        self.layout.addWidget(topic_entity)

    def display_topics(self, tab_name: str) -> None:
        """
        Display topics in the given tab
        :param tab_name: Name of the tab to display
        :return: None
        """

        # Clear current display
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        # Check if tab exists
        if tab_name not in self.topic_container:
            return

        # Add topics to display
        for topic_name, topic_words in self.topic_container[tab_name]:
            topic_entity = TopicEntity(topic_name, topic_words)
            self.layout.addWidget(topic_entity)

    def remove_tab_from_container(self, tab_name: str) -> None:
        """
        Remove tab from topic container
        :param tab_name: Name of the tab to remove
        :return: None
        """
        self.topic_container.pop(tab_name)
