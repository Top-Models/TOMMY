from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QScrollArea, QTabWidget,
                               QTextEdit)

from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.synonyms_controller import SynonymsController
from tommy.controller.topic_modelling_controller import \
    TopicModellingController
from tommy.support.constant_variables import (
    text_font, stopwords_tab_font, stopwords_text_edit_font, disabled_gray)


class PreprocessingView(QScrollArea):
    """
    The PreprocessingDisplay area to view all preprocessing-related
    input.
    """

    def __init__(self,
                 stopwords_controller: StopwordsController,
                 synonyms_controller: SynonymsController,
                 topic_modelling_controller: TopicModellingController) -> None:
        """The initialization of the StopwordsDisplay."""
        super().__init__()

        # Set reference to the controllers
        self._stopwords_controller = stopwords_controller
        self._topic_modelling_controller = topic_modelling_controller
        self._synonyms_controller = synonyms_controller

        # Subscribe to controller events
        stopwords_controller.stopwords_model_changed_event.subscribe(
            self._update_blacklist_textbox)
        synonyms_controller.synonyms_model_changed_event.subscribe(
            self._update_synonym_textbox)
        topic_modelling_controller.start_training_model_event.subscribe(
            lambda _: self.disable_text_edits_on_start_topic_modelling())
        topic_modelling_controller.model_trained_event.subscribe(
            lambda _: self.enable_text_edits_on_finish_topic_modelling())

        # Initialize widget properties
        self.setFixedWidth(250)
        self.setMinimumHeight(200)
        self.setMaximumHeight(300)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""        
                QTabWidget {{
                    color: black;
                    border: none;
                    background-color: white;
                }}

                QTabBar::tab {{ 
                    color: rgba(120, 120, 120, 1);
                    background-color: rgba(210, 210, 210, 1);
                    font-size: 15px;
                    font-family: {text_font};
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
                    border-radius: 10px;
                }}
                
                QScrollBar:vertical {{
                    border: none;
                    width: 10px;
                    background: #F0F0F0;
                    margin: 0px;
                }}
                
                QScrollBar::handle:vertical {{
                    background: #CCCCCC;
                    min-height: 20px;
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
        self.container.tabBar().setFont(stopwords_tab_font)

        # Initialize tabs
        self.tab_style_enabled = (f"""
            QTextEdit {{
                border-radius: 5px;
                font-size: 14px;
                font-family: {text_font};
                color: black;
                border: 2px solid #00968F;
                padding: 5px;
                background-color: white;
                margin: 5px;
            }}            
        """)
        self.tab_style_disabled = (f"""
            QTextEdit {{
                border-radius: 5px;
                font-size: 14px;
                font-family: {text_font};
                color: black;
                border: 2px solid #00968F;
                padding: 5px;
                background-color: {disabled_gray};
                margin: 5px;
            }}            
        """)

        self.blacklist_tab = QTextEdit()
        self.blacklist_tab.setFont(stopwords_text_edit_font)
        self.blacklist_tab.setLineWrapMode(QTextEdit.NoWrap)
        self.blacklist_tab.setPlaceholderText(
            "Plaats op elke regel een woord dat uitgesloten moet worden:"
            "\n\nwoord\nwoord\netc.")
        self.blacklist_tab.setStyleSheet(self.tab_style_enabled)

        self.synonym_tab = QTextEdit()
        self.synonym_tab.setFont(stopwords_text_edit_font)
        self.synonym_tab.setLineWrapMode(QTextEdit.NoWrap)
        self.synonym_tab.setPlaceholderText(
            "Plaats op elke regel een synoniem gevolgd door \"=\" en "
            "het woord dat dit synoniem vervangt:"
            "\n\nsynoniem = vervanging\nsynoniem = vervanging\netc.")
        self.synonym_tab.setStyleSheet(self.tab_style_enabled)

        # Set container as the focal point
        self.setWidget(self.container)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Set layouts for tabs
        self.container.addTab(self.blacklist_tab, "Blacklist")
        self.container.addTab(self.synonym_tab, "Synoniemen")

        # Connect text changed event to update methods
        self.blacklist_tab.textChanged.connect(self.update_blacklist)
        self.synonym_tab.textChanged.connect(self.update_synonyms)

        # Disable rich text
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
        Update the set of synonyms with the text from the Synonyms tab.

        :return: None
        """
        input_text = self.synonym_tab.toPlainText()
        lines = input_text.lower().split('\n')
        synonyms = {words[0]: words[1] for words
                    in map(lambda s: s.split(" = "), lines) if len(words) == 2}
        self._synonyms_controller.update_synonyms(synonyms)

    def _update_blacklist_textbox(self, words: list[str]) -> None:
        """Update the blacklist textbox with the given words."""
        text = "\n".join(words)
        self.blacklist_tab.setText(text)

    def _update_synonym_textbox(self, synonyms: dict[str, str]) -> None:
        """Update the synonym textbox with the given synonyms."""
        text = "\n".join([f"{key} = {value}" for key, value in synonyms.items()])
        self.synonym_tab.setText(text)

    def disable_text_edits_on_start_topic_modelling(self) -> None:
        """
        Disable the text edits when starting topic modelling.

        :return: None
        """
        self.blacklist_tab.setReadOnly(True)
        self.synonym_tab.setReadOnly(True)
        self.blacklist_tab.setStyleSheet(self.tab_style_disabled)
        self.synonym_tab.setStyleSheet(self.tab_style_disabled)

    def enable_text_edits_on_finish_topic_modelling(self) -> None:
        """
        Enable the text edits when stopping topic modelling.

        :return: None
        """
        self.blacklist_tab.setReadOnly(False)
        self.synonym_tab.setReadOnly(False)
        self.blacklist_tab.setStyleSheet(self.tab_style_enabled)
        self.synonym_tab.setStyleSheet(self.tab_style_enabled)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
