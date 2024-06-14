import sys

from PySide6.QtGui import QIntValidator, Qt
from PySide6.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, \
    QWidget, QSizePolicy, QPushButton

from tommy.controller.config_controller import ConfigController
from tommy.controller.language_controller import LanguageController
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.support.constant_variables import (
    text_font, seco_col_blue, disabled_gray, heading_font, hover_seco_col_blue,
    pressed_seco_col_blue)
from tommy.support.model_type import ModelType
from tommy.support.parameter_limits import num_topics_min_value, \
    num_topics_max_value, amount_of_words_min_value, amount_of_words_max_value
from tommy.support.supported_languages import SupportedLanguage
from tommy.view.settings_view.abstract_settings.better_combo_box import \
    BetterComboBox
from tommy.view.config_view import ConfigView


class AbstractSettings:
    """
    Abstract class for settings view
    """
    _model_parameters_controller: ModelParametersController
    _config_controller: ConfigController
    _scroll_layout: QVBoxLayout

    def __init__(self,
                 model_parameters_controller: ModelParametersController,
                 config_controller: ConfigController,
                 language_controller: LanguageController):
        """
        Constructor for abstract settings

        :param model_parameters_controller: ModelParametersController
        """
        # Initialize controllers
        self._model_parameters_controller = model_parameters_controller
        self._config_controller = config_controller
        self._language_controller = language_controller

        # Initialize stylesheet
        self.enabled_input_stylesheet = (f"background-color: white;"
                                         f"border-radius: 5px;"
                                         f"font-size: 14px;"
                                         f"font-family: {text_font};"
                                         f"color: black;"
                                         f"border: 2px solid {seco_col_blue};"
                                         f"padding: 5px;")
        self.disabled_input_stylesheet = (f"background-color: {disabled_gray};"
                                          f"border-radius: 5px;"
                                          f"font-size: 14px;"
                                          f"font-family: {text_font};"
                                          f"color: black;"
                                          f"border: 2px solid {seco_col_blue};"
                                          f"padding: 5px;")

        # Initialize buttons
        self.config_management_label = None
        self._config_management_button = None

        # Initialize input fields
        self._algorithm_field = BetterComboBox()
        self._language_field = BetterComboBox()
        self._topic_amount_field = QLineEdit()
        self._amount_of_words_field = QLineEdit()

        # Initialize layout
        self.topic_input_layout_invalid = None
        self.topic_input_layout_valid = None

    def initialize_parameter_widgets(self, scroll_layout: QVBoxLayout) -> None:
        """
        Initialize the parameter widgets
        This method should be overridden by the child class
        to add the model specific widgets to the view

        :return: None
        """
        self._scroll_layout = scroll_layout

        # Config
        self.initialize_config_management()
        self.add_margin(10)

        # Visualizations
        self.add_header_label("Visualisatie", 17)
        self.initialize_amount_of_words_field()
        self.add_margin(10)

        # General
        self.add_header_label("Algemeen", 17)
        self.initialize_algorithm_field()
        self.initialize_topic_amount_field()
        self.initialize_language_field()
        self.add_margin(10)

    def all_fields_valid(self) -> bool:
        """
        Validate all fields

        :return: bool
        """
        return self.validate_topic_amount_field() and (
            self.validate_amount_of_words_field())

    def add_header_label(self, header_text: str, size: int) -> None:
        """
        Add a header label to the settings view

        :param header_text: str
        :param size: int
        :return: None
        """
        header_label = QLabel(header_text)
        header_label.setStyleSheet(f"font-weight: bold;"
                                   f"font-size: {size}px;"
                                   f"font-family: {heading_font};"
                                   f"color: black;"
                                   f"font-family: {text_font};")
        self._scroll_layout.addWidget(header_label)

    def add_margin(self, height: int) -> None:
        """
        Add a margin to the settings view

        :param height: int
        :return: None
        """
        margin_label = QLabel("")
        margin_label.setFixedHeight(height)
        self._scroll_layout.addWidget(margin_label)

    def initialize_config_management(self) -> None:
        """
        Initialize the config management button

        :return: None
        """
        config_management_layout = QHBoxLayout()

        # Add container widget
        config_management_container = QWidget()
        config_management_container.setObjectName(
            "config_management_container")
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        config_management_container.setLayout(container_layout)
        config_management_container.setStyleSheet(f"""
            QWidget#config_management_container {{
                background-color: white;
                border: 2px solid {seco_col_blue};
                border-radius: 5px;
            }}
        """)

        # Add label to container
        self.config_management_label = QLabel(
            self._config_controller.get_selected_configuration()
        )
        self.config_management_label.setStyleSheet(
            f"font-size: 14px;"
            f"color: black;"
            f"font-family: {text_font};"
            f"border-top: 2px solid {seco_col_blue};"
            f"border-bottom: 2px solid {seco_col_blue};"
            f"background-color: white;"
            f"margin-left: 10px;"
        )
        self.config_management_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        container_layout.addWidget(self.config_management_label)

        # Add a horizontal spacer to push the button to the right
        spacer = QWidget()
        spacer.setStyleSheet("background-color: white;"
                             f"border-top: 2px solid {seco_col_blue};"
                             f"border-bottom: 2px solid {seco_col_blue};")
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        container_layout.addWidget(spacer)

        # Add button to container
        self._config_management_button = QPushButton("⛭")
        self._config_management_button.setStyleSheet(f"""
            QPushButton {{
                font-size: 20px;
                font-family: {text_font};
                border-radius: 5px;
                color: white;
                border: none;
                padding: 5px 10px 5px 10px;
                background-color: {seco_col_blue};
            }}
            
            QPushButton:hover {{
                background-color: {hover_seco_col_blue};
            }}
            
            QPushButton:pressed {{
                background-color: {pressed_seco_col_blue};
            }}
        """)
        self._config_management_button.clicked.connect(
            self.open_config_management_widget
        )
        container_layout.addWidget(self._config_management_button)

        # Add config management layout to container layout
        config_management_layout.addWidget(config_management_container)
        self._scroll_layout.addLayout(config_management_layout)

    def open_config_management_widget(self):
        """Method to open the configuration management widget"""
        config_management_widget = ConfigView(
            self._config_controller, self._model_parameters_controller)
        config_management_widget.exec()

    def initialize_topic_amount_field(self) -> None:
        """
        Initialize the topic amount field

        :return: None
        """
        topic_amount_layout = QHBoxLayout()

        # Add label
        topic_label = QLabel("#Topics:")
        topic_label.setStyleSheet(f"font-size: 16px;"
                                  f"color: black;"
                                  f"font-family: {text_font};")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                 Qt.AlignmentFlag.AlignVCenter)
        topic_amount_layout.addWidget(topic_label)

        # Define layout for whether topic input is valid or invalid
        self.topic_input_layout_valid = (f"border-radius: 5px;"
                                         f"font-size: 14px;"
                                         f"font-family: {text_font};"
                                         f"color: black;"
                                         f"border: 2px solid {seco_col_blue};"
                                         f"padding: 5px;"
                                         f"background-color: white;")
        self.topic_input_layout_invalid = (f"border-radius: 5px;"
                                           f"font-size: 14px;"
                                           f"font-family: {text_font};"
                                           f"color: black;"
                                           f"border: 2px solid red;"
                                           f"padding: 5px;"
                                           f"background-color: white;")

        # Add input field
        self._topic_amount_field = QLineEdit()
        self._topic_amount_field.setFixedWidth(100)
        self._topic_amount_field.setStyleSheet(self.topic_input_layout_valid)
        # QIntValidator prevents user from typing
        # anything that isn't an integer
        self._topic_amount_field.setValidator(QIntValidator(
            num_topics_min_value, num_topics_max_value))
        self._topic_amount_field.setPlaceholderText("Voer aantal topics in")
        self._topic_amount_field.setStyleSheet(self.topic_input_layout_valid)
        self._topic_amount_field.setAlignment(Qt.AlignmentFlag.AlignLeft)
        topic_amount_layout.addWidget(self._topic_amount_field)
        self._topic_amount_field.editingFinished.connect(
            self.topic_amount_field_editing_finished_event)

        # Add topic amount layout to container layout
        self._scroll_layout.addLayout(topic_amount_layout)

    def topic_amount_field_editing_finished_event(self) -> None:
        """
        Event handler for when the topic amount field is edited

        :return: None
        """
        self._model_parameters_controller.set_model_n_topics(
            self.get_topic_amount())

    def validate_topic_amount_field(self) -> bool:
        """
        Validate the topic amount field

        :return: bool
        """
        topic_input_text = self._topic_amount_field.text()
        valid_input = True
        try:
            num_topics = int(topic_input_text)
            if (num_topics < num_topics_min_value or num_topics >
                    num_topics_max_value):
                valid_input = False
        except ValueError:
            valid_input = False

        if valid_input:
            self._topic_amount_field.setStyleSheet(
                self.topic_input_layout_valid)
            self._topic_amount_field.setPlaceholderText("")
        else:
            self._topic_amount_field.setStyleSheet(
                self.topic_input_layout_invalid)
            self._topic_amount_field.setText("")
            self._topic_amount_field.setPlaceholderText(
                f"{num_topics_min_value} - {num_topics_max_value}")
        return valid_input

    def get_topic_amount(self) -> int:
        """
        Get the topic amount

        :return: int
        """
        text = self._topic_amount_field.text()
        input_valid = self.validate_topic_amount_field()
        if input_valid:
            return int(text)
        return 0

    def initialize_amount_of_words_field(self) -> None:
        """
        Initialize the amount of words field

        :return: None
        """
        topic_words_layout = QHBoxLayout()

        # Add label
        topic_words_label = QLabel("#Topicwoorden:")
        topic_words_label.setStyleSheet(f"font-size: 16px;"
                                        f"color: black;"
                                        f"font-family: {text_font};")
        topic_words_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                       Qt.AlignmentFlag.AlignVCenter)
        topic_words_layout.addWidget(topic_words_label)

        # Add input field
        self._amount_of_words_field = QLineEdit()
        self._amount_of_words_field.setFixedWidth(100)
        self._amount_of_words_field.setPlaceholderText("Voer aantal "
                                                       "woorden in")
        self._amount_of_words_field.setStyleSheet(
            self.enabled_input_stylesheet)
        self._amount_of_words_field.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._amount_of_words_field.setValidator(QIntValidator(
            amount_of_words_min_value, amount_of_words_max_value))
        self._amount_of_words_field.editingFinished.connect(
            self.amount_of_words_field_editing_finished_event)
        topic_words_layout.addWidget(self._amount_of_words_field)

        # Add topic words layout to container layout
        self._scroll_layout.addLayout(topic_words_layout)

    def amount_of_words_field_editing_finished_event(self) -> None:
        """
        Event handler for when the amount of words field is edited

        :return: None
        """
        self._model_parameters_controller.set_model_word_amount(
            int(self._amount_of_words_field.text()))

    def validate_amount_of_words_field(self) -> bool:
        """
        Validate the amount of words field

        :return: bool
        """
        topic_words_input_text = self._amount_of_words_field.text()
        valid_input = True
        try:
            num_words = int(topic_words_input_text)
            if (num_words < amount_of_words_min_value or num_words >
                    amount_of_words_max_value):
                valid_input = False
        except ValueError:
            valid_input = False

        if valid_input:
            self._amount_of_words_field.setStyleSheet(
                self.enabled_input_stylesheet)
            self._amount_of_words_field.setPlaceholderText("")
        else:
            self._amount_of_words_field.setStyleSheet(
                self.topic_input_layout_invalid)
            self._amount_of_words_field.setText("")
            self._amount_of_words_field.setPlaceholderText(
                f"{amount_of_words_min_value} - {amount_of_words_max_value}")
        return valid_input

    def get_amount_of_words(self) -> int:
        """
        Get the amount of words

        :return: int
        """
        text = self._amount_of_words_field.text()
        input_valid = self.validate_amount_of_words_field()
        if input_valid:
            return int(text)
        return 0

    def set_text_on_config_change(self):
        self.set_field_values_from_backend()

    def initialize_algorithm_field(self) -> None:
        """
        Initialize the algorithm field

        :return: str
        """
        algorithm_layout = QHBoxLayout()

        # Add label
        algorithm_label = QLabel("Algoritme:")
        algorithm_label.setStyleSheet(f"font-size: 16px;"
                                      f"color: black;"
                                      f"font-family: {text_font};")
        algorithm_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                     Qt.AlignmentFlag.AlignVCenter)
        algorithm_layout.addWidget(algorithm_label)

        # Add input field
        self._algorithm_field = BetterComboBox()
        self._algorithm_field.setFixedWidth(100)
        self._algorithm_field.addItem("LDA")
        self._algorithm_field.addItem("NMF")

        # BERTopic has issues with PyInstaller
        # For this reason, BERTopic is only available when running via Python
        # Like this, the field becomes unavailable when running via PyInstaller
        if not getattr(sys, 'frozen', False):
            self._algorithm_field.addItem("BERTopic")

        # Try to disconnect the algorithm_field_changed_event method, otherwise
        # endless recursion
        try:
            self._algorithm_field.currentIndexChanged.disconnect(
                self.algorithm_field_changed_event)
        # Upon first initialization this is not necessary and will result in
        # an error
        except RuntimeError:
            pass

        current_model = self._model_parameters_controller.get_model_type().name
        self._algorithm_field.setCurrentText(current_model)
        self._algorithm_field.setStyleSheet(self.enabled_input_stylesheet)
        algorithm_layout.addWidget(self._algorithm_field)

        # Reconnect the algorithm_field_changed_event method
        self._algorithm_field.currentIndexChanged.connect(
            self.algorithm_field_changed_event)

        # Add algorithm layout to container layout
        self._scroll_layout.addLayout(algorithm_layout)

    def algorithm_field_changed_event(self) -> None:
        """
        Event handler for when the algorithm field is changed

        :return: None
        """
        selected_model_type = self._algorithm_field.currentText()
        model_type_enum = ModelType[selected_model_type]
        self._model_parameters_controller.set_model_type(
            model_type_enum)

    def initialize_language_field(self) -> None:
        """
        Initialize the language field

        :return: None
        """
        language_layout = QHBoxLayout()

        # Add label
        self._language_field = BetterComboBox()
        language_label = QLabel("Taal corpus:")
        language_label.setStyleSheet(f"font-size: 16px;"
                                     f"color: black;"
                                     f"font-family: {text_font};")
        language_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                    Qt.AlignmentFlag.AlignVCenter)
        language_layout.addWidget(language_label)

        # Add input field
        self._language_field.setFixedWidth(100)
        self._language_field.addItem("Nederlands")
        self._language_field.addItem("Engels")

        # Try to disconnect the algorithm_field_changed_event method, otherwise
        # endless recursion
        try:
            self._language_field.currentIndexChanged.disconnect(
                self.language_field_changed_event)
        # Upon first initialization this is not necessary and will result in
        # an error
        except RuntimeError:
            pass

        self._language_field.setStyleSheet(self.enabled_input_stylesheet)
        language_layout.addWidget(self._language_field)

        # Reconnect the algorithm_field_changed_event method
        self._language_field.currentIndexChanged.connect(
            self.language_field_changed_event)

        # Add algorithm layout to container layout
        self._scroll_layout.addLayout(language_layout)

    def language_field_changed_event(self) -> None:
        """
        Event handler for when the algorithm field is changed

        :return: None
        """
        selected_model_type = self._language_field.currentText()
        self._language_controller.set_language(
            SupportedLanguage.from_string(selected_model_type))

    def set_field_values_from_backend(self):
        """
        Get the parameter values from the backend and put them in the
        text boxes in the frontend. The dropdown for the model type has already
        been set in initialize_algorithm_field. If it was set here,
        it would trigger the algorithm_changed event and cause an infinite
        recursion.
        :return: None
        """
        self._topic_amount_field.setText(
            str(self._model_parameters_controller.get_model_n_topics()))
        self._amount_of_words_field.setText(
            str(self._model_parameters_controller.get_model_word_amount()))
        current_language = self._language_controller.get_language()
        self._language_field.set_current_text_without_signal(
            SupportedLanguage.to_string(current_language))


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
