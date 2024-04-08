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

    def update_synonyms(self) -> None:
        """
        Update synoniems set with the text from the synoniems tab.
        should be updated to handle the right parsing.
        :return: None
        """
        text = self.synoniemen_tab.toPlainText()
        self.synoniemen = set(text.split())

    def update_ngrams(self) -> None:
        """
        Update ngrams set with the text from the ngrams tab.
        should be updated to handle the right parsing.
        :return: None
        """
        text = self.ngrams_tab.toPlainText()
        self.ngrams = set(text.split())


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
