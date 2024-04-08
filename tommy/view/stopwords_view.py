from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QScrollArea, QWidget, QVBoxLayout,
                               QLineEdit, QHBoxLayout, QPushButton)

from tommy.controller.stopwords_controller import StopwordsController
from tommy.support.constant_variables import text_font, \
    hover_seco_col_blue, pressed_seco_col_blue, sec_col_purple
from tommy.view.observer.observer import Observer


class StopwordsView(QScrollArea, Observer):
    """The StopWordsDisplay area to view all stopwords."""

    def __init__(self, stopwords_controller: StopwordsController) -> None:
        """The initialization of the StopwordsDisplay."""
        super().__init__()

        # Set reference to the controller
        self._stopwords_controller = stopwords_controller
        stopwords_controller.add(self)

        # Initialize widget properties
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: white;")

        # Initialize container for all elements
        self.container = QWidget()

        # Initialize layout for container
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Initialize container for the input field and button
        self.input_container = QWidget()
        self.input_layout = QVBoxLayout(self.input_container)
        self.input_layout.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.input_container)

        # Initialize input field
        self.add_button = None
        self.input_field = None
        self.initialize_widgets()

        # Initialize scroll area and its layout
        self.scroll_area = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_area)
        self.scroll_layout.setAlignment(Qt.AlignCenter)

        # Initialize excluded words
        self.word_layout = QVBoxLayout()
        self.scroll_layout.addLayout(self.word_layout)
        # TODO: maybe this isn't good design,
        #  and it should happen from the controller
        self.show_excluded_words([])

        # Add scroll area to container
        self.container_layout.addWidget(self.scroll_area)

        # Set container as the focal point
        self.setWidget(self.container)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def initialize_widgets(self) -> None:
        """Initialize the widgets."""
        self.initialize_input_field()
        self.initialize_add_button()

    def initialize_input_field(self) -> None:
        """
        Initialize the input field.

        :return: None
        """
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Voer een woord in")
        self.input_field.setStyleSheet(f"border-radius: 5px;"
                                       f"font-size: 14px;"
                                       f"font-family: {text_font};"
                                       f"color: black;"
                                       f"border: 2px solid #00968F;"
                                       f"padding: 5px;"
                                       f"background-color: white;")
        self.input_layout.addWidget(self.input_field)

        # Add event for pressing enter
        self.input_field.returnPressed.connect(self.add_to_word_list)

    def initialize_add_button(self) -> None:
        """
        Initialize the add button.

        :return: None
        """
        self.add_button = QPushButton("Uitsluiten")
        self.add_button.setStyleSheet(f"background-color: #00968F;"
                                      f"color: white;"
                                      f"font-family: {text_font};"
                                      f"padding: 10px;"
                                      f"border: none;")

        self.add_button.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: #00968F;
                    color: white;
                    font-family: {text_font};
                    padding: 10px;
                    border: none;
                }}
                
                QPushButton:hover {{
                    background-color: {hover_seco_col_blue};
                }}
                
                QPushButton:pressed {{
                    background-color: {pressed_seco_col_blue};
                }}
            """)

        self.input_layout.addWidget(self.add_button)

        # Connect button click event to add_to_word_list method
        self.add_button.clicked.connect(self.add_to_word_list)

    def create_word_label(self, stopword: str) -> QLabel:
        """Create a label for every word"""
        stopword_label = QLabel(stopword, self)
        stopword_label.setStyleSheet(f"background-color: {sec_col_purple};"
                                     f"color: white;"
                                     f"font-family: {text_font};"
                                     f"font-size: 12px;"
                                     f"padding: 15px;")
        stopword_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stopword_label.setScaledContents(True)
        stopword_label.setWordWrap(True)
        stopword_label.setCursor(Qt.PointingHandCursor)

        # Connect click event to remove_word method
        stopword_label.mousePressEvent = lambda event: (
            self.remove_word(stopword))

        return stopword_label

    def show_excluded_words(self, word_list: list[str]) -> None:
        """
        Visualize words in the words list.

        :param word_list: The list of words needed to be shown
        :return: None
        """
        horizontal_layout = QHBoxLayout()

        for i, word in enumerate(word_list):
            # Make and format word
            word_label = self.create_word_label(word)
            horizontal_layout.addWidget(word_label)

            if (i + 1) % 2 == 0 or len(word) >= 8:
                self.word_layout.addLayout(horizontal_layout)
                horizontal_layout = QHBoxLayout()

        # Add remaining widgets if any
        if horizontal_layout.count() > 0:
            self.word_layout.addLayout(horizontal_layout)

    def add_to_word_list(self) -> None:
        """
        Add words to the list of excluded words and update the UI.

        :return: None
        """
        new_word = self.input_field.text()
        if new_word:
            self._stopwords_controller.add_stopword(new_word)
            self.input_field.clear()

    def remove_word(self, word) -> None:
        """
        Remove a word from the list of excluded words and update the UI.

        :param word: The word to be removed
        :return: None
        """
        self._stopwords_controller.remove_stopword(word)

    def update_word_vis(self, stopwords: list[str]) -> None:
        """
        Remove current words from excluded word UI and show new ones.

        :return: None
        """
        # Clear current view
        for i in reversed(range(self.word_layout.count())):
            layout_item = self.word_layout.itemAt(i)
            if layout_item is not None:
                while layout_item.count():
                    item = layout_item.takeAt(0)
                    current_item = item.widget()
                    if current_item:
                        current_item.setParent(None)

        # Display updated words in UI
        self.show_excluded_words(stopwords)

    def update_observer(self, publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        self.update_word_vis(list(publisher.stopwords_model.extra_words))


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
