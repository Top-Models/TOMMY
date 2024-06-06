from PySide6.QtCore import Qt, Signal, QEvent, QRect, QPoint, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, \
    QLayout, QLayoutItem, QWidgetItem

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
        self.setMinimumHeight(430)
        self.setMinimumWidth(250)
        self.setContentsMargins(5, 5, 5, 5)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
        self.layout = FlowLayout(self.scroll_area)
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
        self._graph_controller.refresh_name_event.subscribe(
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

    def _on_topic_name_changed(self, index: int, new_name: str) -> None:
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


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=5, spacing=5):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(15, margin, margin, margin)

        self.setSpacing(spacing)
        self.itemList = []

    def addItem(self, item) -> None:
        """
        Add an item to the layout

        :param item: The item to add
        :return: None
        """
        self.itemList.append(item)

    def count(self) -> int:
        """
        Get the number of items in the layout

        :return: The number of items in the layout
        """
        return len(self.itemList)

    def itemAt(self, index) -> QWidgetItem:
        """
        Get the item at the given index

        :param index: The index of the item
        :return: The item at the given index
        """
        if 0 <= index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index) -> QWidgetItem:
        """
        Remove the item at the given index

        :param index: The index of the item to remove
        :return: The item that was removed
        """
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self) -> Qt.Orientations:
        """
        Get the expanding directions of the layout

        :return: The expanding directions of the layout
        """
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self) -> bool:
        """
        Check if the layout has a height for width

        :return: True if the layout has a height for width, False otherwise
        """
        return True

    def heightForWidth(self, width) -> int:
        """
        Get the height for the given width

        :param width: The width to get the height for
        :return: The height for the given width
        """
        return self.do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect) -> None:
        """
        Set the geometry of the layout

        :param rect: The rectangle to set the geometry to
        :return: None
        """
        super().setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self) -> QSize:
        """
        Get the size hint of the layout

        :return: The size hint of the layout
        """
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        """
        Get the minimum size of the layout

        :return: The minimum size of the layout
        """
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin = self.contentsMargins().left()
        size += QSize(2 * margin, 2 * margin)
        return size

    def do_layout(self, rect, testOnly) -> int:
        """
        Perform the layout

        :param rect: The rectangle to perform the layout in
        :param testOnly: True if the layout should only be tested, False
        :return: The height of the layout
        """
        x = rect.x() + self.contentsMargins().left()
        y = rect.y() + self.contentsMargins().top()
        line_height = 0
        space_y = self.spacing()

        # Calculate items per line
        items_per_line = []
        current_line = []
        line_width = 0

        for item in self.itemList:
            wid = item.widget()
            style = wid.style()
            space_x = self.spacing() + style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            space_y = self.spacing() + style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

            next_x = x + wid.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                items_per_line.append((current_line, line_width))
                current_line = []
                x = rect.x() + self.contentsMargins().left()
                y = y + line_height + space_y
                next_x = x + wid.sizeHint().width() + space_x
                line_height = 0
                line_width = 0

            current_line.append(item)
            x = next_x
            line_height = max(line_height, wid.sizeHint().height())
            line_width += wid.sizeHint().width() + space_x

        items_per_line.append((current_line, line_width))

        # Reset x and y for actual layout
        x = rect.x() + self.contentsMargins().left()
        y = rect.y() + self.contentsMargins().top()
        line_height = 0

        # Perform actual layout
        for line, line_width in items_per_line:
            extra_space = rect.width() - line_width + self.spacing()
            extra_space_per_item = extra_space // len(line) if len(
                line) > 0 else 0

            for item in line:
                wid = item.widget()
                style = wid.style()
                space_x = self.spacing() + style.layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton,
                    Qt.Horizontal)
                space_y = self.spacing() + style.layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton,
                    Qt.Vertical)

                item_width = wid.sizeHint().width() + extra_space_per_item
                if not testOnly:
                    item.setGeometry(QRect(QPoint(x, y),
                                           QSize(item_width,
                                                 wid.sizeHint().height())))

                x += item_width + space_x
                line_height = max(line_height, wid.sizeHint().height())

            x = rect.x() + self.contentsMargins().left()
            y += line_height + space_y
            line_height = 0

        return y + line_height - rect.y()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
