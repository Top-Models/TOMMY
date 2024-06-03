from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from tommy.controller.graph_controller import GraphController
from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.support.constant_variables import sec_col_orange, scrollbar_style
from tommy.datatypes.topics import TopicWithScores

from tommy.view.topic_view.topic_entity_component.topic_entity import (
    TopicEntity)


class FetchedTopicsView(QScrollArea):
    """A widget for displaying the found topics."""

    topicClicked = Signal(object)

    def __init__(self,
                 graph_controller: GraphController,
                 model_parameters_controller: ModelParametersController) \
            -> None:
        """Initialize the FetchedTopicDisplay widget."""
        super().__init__()

        # Initialize widget properties
        self.setMinimumHeight(400)
        self.setFixedWidth(250)
        self.setObjectName("fetched_topics_display")
        self.setStyleSheet(
            """
            QWidget#scroll_area {
                background-color: rgba(230, 230, 230, 230);
                border-bottom: 3px solid lightgrey;
            }
            """
            + scrollbar_style
        )

        # { tab_name, [(topic_name, [words])] }
        self.topic_container = {}
        self.selected_topic = None

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
        self._current_tab_name = "lda_model"

        # Set reference to the controller where topics will be fetched from
        # and subscribe to its topic publisher
        self._graph_controller = graph_controller
        self._graph_controller.topics_changed_event.subscribe(
            self._refresh_topics)

        # Set reference to the model parameters controller
        self._model_parameters_controller = model_parameters_controller

    def _add_topic(self,
                   tab_name: str,
                   topic_name: str,
                   topic_words: list[str],
                   index: int) -> None:
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
        topic_entity = TopicEntity(topic_name, topic_words, index)
        topic_entity.clicked.connect(self._on_topic_clicked)
        topic_entity.wordClicked.connect(self._on_word_clicked)
        topic_entity.nameChanged.connect(self._on_topic_name_changed)

    def _on_topic_name_changed(self, index: int,  new_name: str) -> None:
        """
        Event handler for when a topic name is changed
        :param new_name: The new name of the topic
        :return: None
        """
        if self._graph_controller.has_topic_runner:
            self._graph_controller.set_topic_name(index, new_name)
        self._refresh_topics(None)

    def _display_topics(self, tab_name: str) -> None:
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

        # Add topics to view
        for index, (topic_name, topic_words) in (
                enumerate(self.topic_container[tab_name])):
            topic_entity = TopicEntity(topic_name, topic_words, index)
            topic_entity.wordClicked.connect(self._on_word_clicked)
            topic_entity.clicked.connect(self._on_topic_clicked)
            topic_entity.nameChanged.connect(self._on_topic_name_changed)
            self.layout.addWidget(topic_entity)

    def remove_tab_from_container(self, tab_name: str) -> None:
        """
        Remove tab from topic container
        :param tab_name: Name of the tab to remove
        :return: None
        """
        self.topic_container.pop(tab_name)

    def _clear_topics(self) -> None:
        """
        Clear the topics from the display
        :return: None
        """
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
        self.topic_container = {}

    def _refresh_topics(self, data: None) -> None:
        """Retrieve the topics from the GraphController and update the view"""
        self._clear_topics()

        if not self._graph_controller.has_topic_runner:
            return

        for i in range(self._graph_controller.get_number_of_topics()):
            topic_name = self._graph_controller.get_topic_name(i)
            topic = self._graph_controller.get_topic_with_scores(
                i, self._model_parameters_controller.get_model_word_amount())
            topic_words = topic.top_words
            self._add_topic(self._current_tab_name, topic_name, topic_words, i)

        self._display_topics(self._current_tab_name)

    def _on_word_clicked(self, word: str):
        """
        Event handler for when a word is clicked

        :param word: The word that was clicked
        :return: None
        """
        for i in range(self.layout.count()):
            topic_entity = self.layout.itemAt(i).widget()
            if isinstance(topic_entity, TopicEntity):
                topic_entity.change_word_style(word,
                                               sec_col_orange,
                                               "black")

    def _on_topic_clicked(self, topic_entity: TopicEntity) -> None:
        """
        Event handler for when a topic is clicked

        :param topic_entity: The topic entity that was clicked
        :return: None
        """
        self.deselect_all_topics()

        # Deselect topic if it was already selected
        if self.selected_topic == topic_entity:
            self.selected_topic = None
            topic_entity.deselect()
        else:
            self.selected_topic = topic_entity
            topic_entity.select()
            topic_entity.select()
        self.topicClicked.emit(topic_entity)

        if self.selected_topic is not None:
            self._graph_controller.set_selected_topic(topic_entity.index)
            return

        self._graph_controller.set_selected_topic(None)

    def deselect_all_topics(self) -> None:
        """
        Deselect all topics
        :return: None
        """
        for i in range(self.layout.count()):
            topic_entity = self.layout.itemAt(i).widget()
            if isinstance(topic_entity, TopicEntity):
                topic_entity.deselect()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
