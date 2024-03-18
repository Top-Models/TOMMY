from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from tommy.view.observer.observer import Observer
from tommy.view.topic_view.topic_entity import (
    TopicEntity)


class FetchedTopicsView(QScrollArea, Observer):
    """A widget for displaying the found topics."""
    def __init__(self) -> None:
        """Initialize the FetchedTopicDisplay widget."""
        super().__init__()

        # Initialize widget properties
        self.setObjectName("fetched_topics_display")
        self.setStyleSheet(
            """
            QWidget#scroll_area {
                background-color: rgba(230, 230, 230, 230);
                border-bottom: 3px solid lightgrey;
            }
            """
        )

        # { tab_name, [(topic_name, [words])] }
        self.topic_container = {}

        # Initialize layout for scroll area
        self.scroll_area = QWidget()
        self.scroll_area.setObjectName("scroll_area")
        self.layout = QVBoxLayout(self.scroll_area)
        self.layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # Set scroll area as focal point
        self.setWidget(self.scroll_area)

        # Add Scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Set default tab
        self.display_topics("lda_model")

    def add_topic(self, tab_name: str, topic_name: str,
                  topic_words: list[str]) -> None:
        """
        Add a new topic to the view.

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

        # Add topic to view
        topic_entity = TopicEntity(topic_name, topic_words)
        self.layout.addWidget(topic_entity)

    def display_topics(self, tab_name: str) -> None:
        """
        Display topics in the given tab

        :param tab_name: Name of the tab to view
        :return: None
        """
        # Clear current view
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        # Check if tab exists
        if tab_name not in self.topic_container:
            return

        # Add topics to view
        for topic_name, topic_words in self.topic_container[tab_name]:
            topic_entity = TopicEntity(topic_name, topic_words)
            self.layout.addWidget(topic_entity)

    def remove_tab_from_container(self, tab_name: str) -> None:
        """
        Remove tab from topic container.
        :param tab_name: Name of the tab to remove
        :return: None
        """
        self.topic_container.pop(tab_name)

    def clear_topics(self) -> None:
        """
        Clear the topics from the view.

        :return: None
        """
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
        self.topic_container = {}

    def update_observer(self, publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
