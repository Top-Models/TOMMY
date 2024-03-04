from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout
from nltk.corpus import stopwords
from interactive_topic_modeling.support.constant_variables import text_font

class StopwordsDisplay(QScrollArea):
    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: white;")

        # Initialize container for all elements
        self.container = QWidget()

        # Initialize layout for container
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Initialize container for the input field
        self.input_container = QWidget()
        self.input_layout = QVBoxLayout(self.input_container)
        self.input_layout.setAlignment(Qt.AlignCenter)

        # Initialize and add input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Woord uitsluiten:")
        self.input_field.setStyleSheet(f"border: 2px solid #E40046;"
                                       f"background-color: white;"
                                       f"font-family: {text_font};"
                                       f"margin-right: 10px;"
                                       f"color: black;")
        self.input_field.setFixedWidth(208)
        self.input_layout.addWidget(self.input_field)
        self.container_layout.addWidget(self.input_container)

        # Initialize scroll area and its layout
        self.scroll_area = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_area)
        self.scroll_layout.setAlignment(Qt.AlignCenter)

        # Import stopwords
        self.dutch_stopwords = set(stopwords.words("dutch"))

        # Initialize excluded words
        self.word_layout = QVBoxLayout()
        self.scroll_layout.addLayout(self.word_layout)
        self.show_excluded_words(self.dutch_stopwords)

        # Add scroll area to container
        self.container_layout.addWidget(self.scroll_area)

        # Set container as the focal point
        self.setWidget(self.container)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Input field workings
        self.input_field.returnPressed.connect(self.add_to_word_list)

    def show_excluded_words(self, word_list: list[str]):
        """
        Visualize words in the words list
        :param word_list: The list of words needed to be shown
        :return: None
        """

        def create_word_label(word):
            word_label = QLabel(word, self)
            word_label.setStyleSheet(f"background-color: #00968F;"
                                     f"color: white;"
                                     f"font-family: {text_font};"
                                     f"font-size: 12px;"
                                     f"padding: 15px;"
                                     )
            word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            word_label.setScaledContents(True)
            word_label.setWordWrap(True)
            word_label.setCursor(Qt.PointingHandCursor)
            word_label.mousePressEvent = lambda event: self.remove_word(word)
            return word_label

        horizontal_layout = QHBoxLayout()

        for i, word in enumerate(word_list):
            # Make and format word
            word_label = create_word_label(word)
            horizontal_layout.addWidget(word_label)

            if (i + 1) % 2 == 0 or len(word) >= 8:
                self.word_layout.addLayout(horizontal_layout)
                horizontal_layout = QHBoxLayout()

        # Add remaining widgets if any
        if horizontal_layout.count() > 0:
            self.word_layout.addLayout(horizontal_layout)

    def add_to_word_list(self):
        """
        Add words to the list of excluded words and update the UI
        :return: None
        """
        new_word = self.input_field.text()
        if new_word:
            self.dutch_stopwords.add(new_word)
            self.update_word_vis()
            self.input_field.clear()

    def remove_word(self, word):
        """
        Remove a word from the list of excluded words and update the UI
        :param word: The word to be removed
        :return: None
        """
        if word in self.dutch_stopwords:
            self.dutch_stopwords.remove(word)
            self.update_word_vis()

    def update_word_vis(self):
        """
        Remove current words from excluded word UI and show new ones
        :return: None
        """
        # Clear current display
        for i in reversed(range(self.word_layout.count())):
            layout_item = self.word_layout.itemAt(i)
            if layout_item is not None:
                while layout_item.count():
                    item = layout_item.takeAt(0)
                    current_item = item.widget()
                    if current_item:
                        current_item.setParent(None)

        # Display updated words in UI
        self.show_excluded_words(list(self.dutch_stopwords))


