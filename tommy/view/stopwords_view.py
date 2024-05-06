from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QScrollArea, QTabWidget,
                               QTextEdit)

from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.synonims_controller import SynonymsController
from tommy.support.constant_variables import (
    text_font)


class StopwordsView(QScrollArea):
    """The StopWordsDisplay area to view all stopwords."""

    def __init__(self,
                 stopwords_controller: StopwordsController,
                 synonyms_controller: SynonymsController) -> None:
        """The initialization of the StopwordsDisplay."""
        super().__init__()

        # Set reference to the controllers
        self._stopwords_controller = stopwords_controller
        self._synonyms_controller = synonyms_controller

        # Initialize widget properties
        self.setFixedWidth(250)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""        
                QTabWidget {{
                    color: black;
                    border: none;
                }}

                QTabBar::tab {{ 
                    color: black;
                    background-color: rgba(230, 230, 230, 1);
                    font-size: 15px;
                    padding-left: 5px;
                    padding-right: 5px;
                    padding-top: 10px;
                    padding-bottom: 10px;
                    font-weight: bold;
                }}

                QTabBar::tab:selected {{
                    color: #000000;
                    background-color: white;
                }}

                QTabBar::tab:hover {{
                    background-color: white;
                }}

                QTabWidget::tab-bar {{
                    alignment: left;
                    width: 250px;
                }}

                QScrollArea {{
                    border: 0px solid #00968F;
                    border-radius: 10px;
                }}
                QScrollBar:vertical {{
                    border: none;
                    background: #F0F0F0;
                    width: 30px;
                    margin: 0px;
                }}
                QScrollBar::handle:vertical {{
                    background: #CCCCCC;
                    min-height: 20px;
                    border-radius: 10px;
                }}
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    height: 0px; 
                }}
                QScrollBar:horizontal {{
                    border: none;
                    background: #F0F0F0;
                    height: 30px;
                    margin: 0px;
                }}
                QScrollBar::handle:horizontal {{
                    background: #CCCCCC;
                    min-width: 20px;
                    border-radius: 10px;
                }}
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                    width: 0px; 
                }}
                   """)
        # Initialize container for all elements
        self.container = QTabWidget()

        # Initialize tabs
        tab_style = (f"border-radius: 5px;"
                     f"font-size: 14px;"
                     f"font-family: {text_font};"
                     f"color: black;"
                     f"border: 2px solid #00968F;"
                     f"padding: 5px;"
                     f"background-color: white;"
                     f"margin: 5px;")

        self.blacklist_tab = QTextEdit()
        self.blacklist_tab.setStyleSheet(tab_style)
        self.blacklist_tab.setLineWrapMode(QTextEdit.NoWrap)

        self.ngrams_tab = QTextEdit()
        self.ngrams_tab.setStyleSheet(tab_style)
        self.ngrams_tab.setLineWrapMode(QTextEdit.NoWrap)

        self.synonym_tab = QTextEdit()
        self.synonym_tab.setStyleSheet(tab_style)
        self.synonym_tab.setLineWrapMode(QTextEdit.NoWrap)

        # Set container as the focal point
        self.setWidget(self.container)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Set layouts for tabs
        self.container.addTab(self.blacklist_tab, "Blacklist")
        self.container.addTab(self.synonym_tab, "Synoniemen")
        self.container.addTab(self.ngrams_tab, "N-grams")

        # Connect text changed event to update methods
        self.blacklist_tab.textChanged.connect(self.update_blacklist)
        self.synonym_tab.textChanged.connect(self.update_synonyms)
        self.ngrams_tab.textChanged.connect(self.update_ngrams)

        # Disable rich text
        self.blacklist_tab.setAcceptRichText(False)
        self.synonym_tab.setAcceptRichText(False)
        self.ngrams_tab.setAcceptRichText(False)

    def update_blacklist(self) -> None:
        """
        Update the set of blacklisted words with the text from the Blacklist
        tab.

        :return: None
        """
        input_text = self.blacklist_tab.toPlainText()
        blacklist = set([word.lower() for word in input_text.split()])
        self._stopwords_controller.update_stopwords(blacklist)

    def update_synonyms(self) -> None:
        """
        Update the set of synonyms with the text from the Synonyms tab.

        :return: None
        """
        input_text = self.synonym_tab.toPlainText()
        synonyms_dict = {}

        # Split the input text into lines
        lines = input_text.split('\n')
        for line in lines:
            # Split each line into words
            words = line.split()
            if len(words) > 1:
                # First word is considered as the main word, rest are synonyms
                main_word = words[0].lower()
                synonyms = [word.lower() for word in words[1:]]
                synonyms_dict[main_word] = synonyms

        # Pass the synonyms mapping to the controller to update synonyms
        self._synonyms_controller.update_synonyms(synonyms_dict)

    def update_ngrams(self) -> None:
        """
        Update ngrams set with the text from the ngrams tab.
        should be updated to handle the right parsing.
        :return: None
        """
        input_text = self.ngrams_tab.toPlainText()
        # TODO: implement at a later point


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
