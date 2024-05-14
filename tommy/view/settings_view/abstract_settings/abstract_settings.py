from PySide6.QtGui import QIntValidator, Qt
from PySide6.QtWidgets import QLineEdit, QLabel, QHBoxLayout, \
    QVBoxLayout, QComboBox

from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.support.constant_variables import text_font, seco_col_blue, \
    disabled_gray, heading_font
from tommy.support.model_type import ModelType


class AbstractSettings:
    """
    Abstract class for settings view
    """
    _model_parameters_controller: ModelParametersController
    _scroll_layout: QVBoxLayout

    def __init__(self,
                 model_parameters_controller: ModelParametersController):
        """
        Constructor for abstract settings

        :param model_parameters_controller: ModelParametersController
        """
        # Initialize controllers
        self._model_parameters_controller = model_parameters_controller

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

        # Initialize input fields
        self._algorithm_field = QComboBox()
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
        self.add_header_label("Algemeen", 17)
        self.initialize_algorithm_field()
        self.initialize_topic_amount_field()
        self.initialize_amount_of_words_field()
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

    def initialize_topic_amount_field(self) -> None:
        """
        Initialize the topic amount field

        :return: None
        """
        topic_amount_layout = QHBoxLayout()

        # Add label
        topic_label = QLabel("Aantal topics:")
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
        self._topic_amount_field.setValidator(QIntValidator(1, 999))
        self._topic_amount_field.setPlaceholderText("Voer aantal topics in")
        self._topic_amount_field.setText(
            str(self._model_parameters_controller.get_model_n_topics()))
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
            if num_topics < 1 or num_topics > 999:
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
                "Moet tussen 1 en 999 liggen")
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
        topic_words_label = QLabel("Aantal woorden:")
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
        self._amount_of_words_field.setText("10")
        self._amount_of_words_field.setStyleSheet(
            self.enabled_input_stylesheet)
        self._amount_of_words_field.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._amount_of_words_field.setValidator(QIntValidator(1, 999))
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
            if num_words < 1 or num_words > 999:
                valid_input = False
        except ValueError:
            valid_input = False

        if valid_input:
            self._amount_of_words_field.setStyleSheet(
                self.enabled_input_stylesheet)
            self._amount_of_words_field.setPlaceholderText("")
        else:
            self._amount_of_words_field.setStyleSheet(
                self.disabled_input_stylesheet)
            self._amount_of_words_field.setText("")
            self._amount_of_words_field.setPlaceholderText(
                "Moet tussen 1 en 999 liggen")
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
        self._algorithm_field = QComboBox()
        self._algorithm_field.setFixedWidth(100)
        self._algorithm_field.addItem("LDA")
        self._algorithm_field.addItem("BERTopic")
        self._algorithm_field.addItem("NMF")

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




"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
