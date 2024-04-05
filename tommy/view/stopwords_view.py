from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QScrollArea, QWidget, QVBoxLayout,
                               QLineEdit, QHBoxLayout, QPushButton, QTabWidget,
                               QTextEdit)

from tommy.support.constant_variables import text_font, \
    hover_seco_col_blue, pressed_seco_col_blue, sec_col_purple, \
    hover_prim_col_red
from tommy.view.observer.observer import Observer


class StopwordsView(QScrollArea, Observer):
    """The StopWordsDisplay area to view all stopwords."""
    def __init__(self) -> None:
        """The initialization of the StopwordsDisplay."""
        super().__init__()

        # Initialize widget properties
        self.setFixedWidth(250)
        self.setStyleSheet(f"""        
                       QTabWidget {{
                           color: black;
                           border: none;
                       }}

                       QTabBar::tab {{ 
                           background-color: #FFFFFF; 
                           color: gray;
                           font-size: 15px;
                           padding-left: 10px;
                           padding-right: 10px;
                           padding-top: 15px;
                           padding-bottom: 15px;
                           font-weight: bold;
                       }}

                       QTabBar::tab:selected {{
                           border-bottom: 3px solid {hover_prim_col_red};
                           color: #000000;
                           background-color: rgba(240, 240, 240, 1);
                       }}

                       QTabBar::tab:hover {{
                           color: #000000;
                       }}

                       QTabWidget::tab-bar {{
                           alignment: left;
                       }}
                   """)
        # Initialize container for all elements
        self.container = QTabWidget()

        # Initialize tabs
        self.stopwords_tab = QWidget()
        self.ngrams_tab = QTextEdit()
        self.synoniemen_tab = QTextEdit()
        self.blacklist_tab = QTextEdit()

        # Set layouts for tabs
        self.container.addTab(self.blacklist_tab, "Blacklist")
        self.container.addTab(self.synoniemen_tab, "Synoniemen")
        self.container.addTab(self.ngrams_tab, "N-grams")
        self.container.addTab(self.stopwords_tab, "Stopwords")
        # Initialize the set of additional stopwords
        self.additional_stopwords = set()
        self.synoniemen = set()
        self.ngrams = set()

        # Set container as the focal point
        self.setWidget(self.container)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Connect text changed event to update additional_stopwords
        self.blacklist_tab.textChanged.connect(self.update_additional_stopwords)

    def update_additional_stopwords(self) -> None:
        """
        Update additional_stopwords set with the text from the Stopwords tab.

        :return: None
        """
        text = self.blacklist_tab.toPlainText()
        self.additional_stopwords = set(text.split())


    def add_to_word_list_stopwords(self) -> None:
        """
        Add words to the list of excluded words for stopwords tab and update the UI.

        :return: None
        """
        new_word = self.input_field_stopwords.text()
        if new_word:
            self.additional_stopwords.add(new_word)
            self.update_word_vis_stopwords()
            self.input_field_stopwords.clear()

    def update_word_vis_stopwords(self):
        """
        Remove current words from excluded word UI for stopwords tab and show new ones.

        :return: None
        """
        # Clear current view
        for i in reversed(range(self.stopwords_layout.count())):
            layout_item = self.stopwords_layout.itemAt(i)
            if layout_item is not None:
                while layout_item.count():
                    item = layout_item.takeAt(0)
                    current_item = item.widget()
                    if current_item:
                        current_item.setParent(None)

        # Display updated words in UI
        self.show_excluded_words(list(self.additional_stopwords), self.stopwords_layout)

    def show_excluded_words(self, word_list: list[str], layout) -> None:
        """
        Visualize words in the words list for a particular tab.

        :param word_list: The list of words needed to be shown
        :param layout: The layout to which words should be added
        :return: None
        """
        for word in word_list:
            # Make and format word
            word_label = self.create_word_label(word)
            layout.addWidget(word_label)

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

    def remove_word(self, word) -> None:
        """
        Remove a word from the list of excluded words and update the UI.

        :param word: The word to be removed
        :return: None
        """
        self.additional_stopwords.discard(word)
        self.update_word_vis_stopwords()

    def update_word_vis(self):
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
        self.show_excluded_words(list(self.additional_stopwords))

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
