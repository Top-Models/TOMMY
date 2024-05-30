from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QScrollArea, QTabWidget,
                               QTextEdit)

from tommy.controller.stopwords_controller import StopwordsController
from tommy.support.constant_variables import (
    text_font)


class StopwordsView(QScrollArea):
    """The StopWordsDisplay area to view all stopwords."""

    def __init__(self, stopwords_controller: StopwordsController) -> None:
        """The initialization of the StopwordsDisplay."""
        super().__init__()

        # Set reference to the controller
        self._stopwords_controller = stopwords_controller
        stopwords_controller.stopwords_model_changed_event.subscribe(
            self._update_blacklist_textbox)

        # Initialize widget properties
        self.setFixedWidth(250)
        self.setMinimumHeight(200)
        self.setMaximumHeight(300)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""        
                QTabWidget {{
                    color: black;
                    border: none;
                }}

                QTabBar::tab {{ 
                    color: rgba(120, 120, 120, 1);
                    background-color: rgba(210, 210, 210, 1);
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

        # self.stopwords_tab = QWidget()
        # self.stopwords_tab.setStyleSheet(tab_style)
        self.blacklist_tab = QTextEdit()
        self.blacklist_tab.setStyleSheet(tab_style)
        self.synonym_tab = QTextEdit()
        self.synonym_tab.setStyleSheet(tab_style)

        # Set container as the focal point
        self.setWidget(self.container)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Set layouts for tabs
        # self.container.addTab(self.stopwords_tab, "Stopwords")
        self.container.addTab(self.blacklist_tab, "Blacklist")
        self.container.addTab(self.synonym_tab, "Synoniemen")

        # Connect text changed event to update additional_stopwords
        # self.stopwords_tab.textChanged.connect(self.update_stopwords)
        self.blacklist_tab.textChanged.connect(self.update_blacklist)
        self.synonym_tab.textChanged.connect(self.update_synonyms)

        # Disable rich text
        # self.stopwords_tab.setAcceptRichText(False)
        self.blacklist_tab.setAcceptRichText(False)
        self.synonym_tab.setAcceptRichText(False)

    def update_blacklist(self) -> None:
        """
        Update the set of blacklisted words with the text from the Blacklist
        tab.

        :return: None
        """
        input_text = self.blacklist_tab.toPlainText()
        blacklist = input_text.split()
        self._stopwords_controller.update_stopwords(blacklist)

    def update_synonyms(self) -> None:
        """
        Updtate the set of synonyms with the text from the Synonyms tab.

        :return: None
        """
        input_text = self.synonym_tab.toPlainText()
        # TODO: implement at a later point

    def _update_blacklist_textbox(self, words: list[str]):
        text = "\n".join(words)
        self.blacklist_tab.setText(text)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
