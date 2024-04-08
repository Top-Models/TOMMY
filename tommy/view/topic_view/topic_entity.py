from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFrame

from tommy.support.constant_variables import heading_font, \
    text_font, sec_col_purple, pressed_seco_col_purple, hover_seco_col_purple, \
    extra_light_gray, light_gray


class TopicEntity(QFrame):
    wordClicked = Signal(str)
    clicked = Signal(object)

    def __init__(self, topic_name: str, topic_words: list[str]):
        super().__init__()

        # Initialize layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {sec_col_purple}; "
                           f"color: white;")
        self.setFixedWidth(200)

        # Initialize title widget
        topic_label = QLabel(topic_name, self)
        topic_label.setStyleSheet(f"font-family: {heading_font}; "
                                  f"font-size: 15px; "
                                  f"font-weight: bold; "
                                  f"text-transform: uppercase;")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(topic_label)

        # Initialize word widgets
        self.word_layout = QVBoxLayout()
        main_layout.addLayout(self.word_layout)

        # List to store word labels
        self.word_labels = []

        # Adding words horizontally
        horizontal_layout = QHBoxLayout()
        self.add_words(horizontal_layout, topic_words)

        # Add remaining widgets if any
        if horizontal_layout.count() > 0:
            self.word_layout.addLayout(horizontal_layout)

        self.selected = False

    # TODO: Create separate WordEntity class
    # TODO: Make sure TopicEntities can be selected and deselected

    def add_words(self,
                  horizontal_layout: QHBoxLayout,
                  topic_words: list[str]) -> None:
        """
        Add words to the layout
        :param horizontal_layout: The layout to add the words
        :param topic_words: Topic words to add
        :return: None
        """
        for i, word in enumerate(topic_words):
            cleaned_word = word.replace('"', ' ')
            word_label = QLabel(cleaned_word, self)
            word_label.setStyleSheet(
                f"font-family: {text_font}; "
                f"font-size: 12px; "
                f"background-color: white; "
                f"padding: 10px; "
                f"color: black")
            word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            word_label.setCursor(Qt.CursorShape.PointingHandCursor)
            word_label.mousePressEvent = \
                lambda event, w=word_label: self.on_word_clicked(w.text())
            word_label.enterEvent = \
                lambda event, w=word_label: self.on_word_hover(w.text())
            horizontal_layout.addWidget(word_label)
            word_label.leaveEvent = \
                lambda event, w=word_label: self.on_word_leave()

            # Add word label to list
            self.word_labels.append(word_label)

            # Go to next row after 2 words or after long word
            if (i + 1) % 2 == 0 or len(word) >= 8:
                self.word_layout.addLayout(horizontal_layout)
                horizontal_layout = QHBoxLayout()

    def enterEvent(self, event):
        """
        Change the style of the label when the mouse enters.

        :param event: The mouse enter event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"background-color: {hover_seco_col_purple}; "
                               f"color: white;")

    def leaveEvent(self, event) -> None:
        """
        Change the style of the label when the mouse leaves.

        :param event: The mouse leave event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"background-color: {sec_col_purple}; "
                               f"color: white;")

    def mousePressEvent(self, event) -> None:
        """
        Change the style of the label when the mouse is pressed.

        :param event: The mouse press event
        :return: None
        """
        self.selected = True
        self.setStyleSheet(f"background-color: {pressed_seco_col_purple}; "
                           f"color: white;")
        self.clicked.emit(self)

    def deselect(self) -> None:
        """
        Deselect the label.

        :return: None
        """
        self.selected = False
        self.setStyleSheet(f"background-color: {sec_col_purple}; "
                           f"color: white;")

    def mouseReleaseEvent(self, event) -> None:
        """
        Change the style of the label when the mouse is released.
        :param event: The mouse release event
        :return: None
        """
        if self.selected:
            self.setStyleSheet(f"background-color: {pressed_seco_col_purple};")
            return

        self.setStyleSheet(f"background-color: {hover_seco_col_purple}; "
                           f"color: white;")

    def on_word_hover(self, word: str):
        """
        Change the style of the word when hovered

        :param word: The word to be hovered
        :return: None
        """
        for word_label in self.word_labels:
            if word_label.text() == word:
                word_label.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: {light_gray}; "
                    f"padding: 10px; "
                    f"color: black")

    def on_word_leave(self):
        """
        Change the style of the word when left

        :return: None
        """
        for word_label in self.word_labels:
            if word_label.selected:
                continue

            word_label.setStyleSheet(
                f"font-family: {text_font}; "
                f"font-size: 12px; "
                f"background-color: white; "
                f"padding: 10px; "
                f"color: black")

    def on_word_clicked(self, word: str):
        """
        Emit signal when word is clicked
        :param word: The word that was clicked
        :return: None
        """
        self.wordClicked.emit(word)

    def change_word_style(self,
                          word: str,
                          background_color: str,
                          text_color: str):
        """
        Change the style of a word
        :param word: The word to be changed
        :param background_color: The new background color
        :param text_color: The new text color
        :return: None
        """
        for word_label in self.word_labels:
            if word_label.text() == word:
                word_label.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: {background_color}; "
                    f"padding: 10px; "
                    f"color: {text_color}")
            else:
                word_label.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: white; "
                    f"padding: 10px; "
                    f"color: black")
