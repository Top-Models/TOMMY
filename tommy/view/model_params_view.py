from typing import Type

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QScrollArea, QLineEdit,
                               QWidget, QPushButton, QHBoxLayout, QCheckBox)

from tommy.controller.controller import Controller
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.controller.publisher.publisher import Publisher
from tommy.support.constant_variables import (
    text_font, heading_font, seco_col_blue, hover_seco_col_blue,
    pressed_seco_col_blue, prim_col_red, hover_prim_col_red, disabled_gray)
from tommy.view.observer.observer import Observer


class ModelParamsView(QScrollArea, Observer):
    """The ModelParamsDisplay that displays the model settings"""

    def __init__(self, model_parameters_controller: ModelParametersController,
                 controller: Controller,
                 ) -> None:
        """The initialization ot the ModelParamDisplay."""
        super().__init__()

        # Set reference to the model parameters controller
        self._model_parameters_controller = model_parameters_controller
        self._controller = controller

        # Initialize widget properties
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: rgba(230, 230, 230, 230);"
                           "margin: 0px;"
                           "padding: 0px;"
                           "border-bottom: 3px solid lightgrey;")

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

        # Initialize layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Initialize container that will hold settings
        self.container = QWidget()
        self.container.setStyleSheet("border: none;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Initialize title label
        self.title_label = None
        self.initialize_title_label()

        # Initialize topic widgets
        self.topic_amount = None
        self.topic_words_amount_input = None
        self.topic_input_layout_valid = None
        self.topic_input_layout_invalid = None
        self.alpha_value_input = None
        self.beta_value_input = None
        self.auto_calculate_checkbox = None
        self.initialize_parameter_widgets()

        # Initialize button layout
        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignRight)
        self.container_layout.addLayout(self.button_layout, stretch=1)

        # Initialize apply button
        self.apply_button = None
        self.initialize_apply_button()

        # Add container to layout
        self.layout.addWidget(self.container)

    def initialize_parameter_widgets(self) -> None:
        """
        Initialize the parameter widgets.
        :return: None
        """
        # TODO: Add headers to the different sections

        # General settings
        self.initialize_topic_amount_field()
        self.initialize_amount_of_topic_words_field()

        # Hyperparameters LDA
        self.initialize_alpha_and_beta_fields()

    def initialize_topic_amount_field(self) -> None:
        """
        Initialize the topic amount field.
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
        self.topic_amount = QLineEdit()
        self.topic_amount.setFixedWidth(100)
        self.topic_amount.setStyleSheet(self.topic_input_layout_valid)
        # QIntValidator prevents user from typing
        # anything that isn't an integer
        self.topic_amount.setValidator(QIntValidator(1, 999))
        self.topic_amount.setPlaceholderText("Voer aantal topics in")
        self.topic_amount.setText(
            str(self._model_parameters_controller.get_model_n_topics()))
        self.topic_amount.setStyleSheet(self.topic_input_layout_valid)
        self.topic_amount.setAlignment(Qt.AlignLeft)
        topic_amount_layout.addWidget(self.topic_amount)
        self.topic_amount.editingFinished.connect(
            self.topic_k_input_editing_finished_event)

        # Add topic amount layout to container layout
        self.container_layout.addLayout(topic_amount_layout)

    def initialize_amount_of_topic_words_field(self) -> None:
        """
        Initialize the amount of topic words field.
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
        self.topic_words_amount_input = QLineEdit()
        self.topic_words_amount_input.setFixedWidth(100)
        self.topic_words_amount_input.setPlaceholderText("Voer aantal "
                                                         "woorden in")
        self.topic_words_amount_input.setText("10")
        self.topic_words_amount_input.setStyleSheet(
            self.enabled_input_stylesheet)
        self.topic_words_amount_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.topic_words_amount_input.setValidator(QIntValidator(1, 999))
        self.topic_words_amount_input.editingFinished.connect(
            self.topic_word_input_editing_finished_event)
        topic_words_layout.addWidget(self.topic_words_amount_input)

        # Add topic words layout to container layout
        self.container_layout.addLayout(topic_words_layout)

    # TODO: Apply input validation to alpha and beta fields
    def initialize_alpha_and_beta_fields(self) -> None:
        """
        Initialize the alpha and beta fields.
        :return: None
        """
        self.initialize_alpha_field()
        self.initialize_beta_field()
        self.initialize_auto_calculate_alpha_beta_checkbox()

    def initialize_alpha_field(self) -> None:
        """
        Initialize the alpha field.
        :return: None
        """
        alpha_layout = QHBoxLayout()

        # Add alpha label
        alpha_label = QLabel("Alpha:")
        alpha_label.setStyleSheet(f"font-size: 16px;"
                                  f"color: black;"
                                  f"font-family: {text_font};")
        alpha_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                 Qt.AlignmentFlag.AlignVCenter)
        alpha_layout.addWidget(alpha_label)

        # Add alpha input field
        self.alpha_value_input = QLineEdit()
        self.alpha_value_input.setReadOnly(True)
        self.alpha_value_input.setFixedWidth(100)
        self.alpha_value_input.setPlaceholderText("Voer alpha in")
        self.alpha_value_input.setText("1.0")
        self.alpha_value_input.setStyleSheet(self.disabled_input_stylesheet)
        self.alpha_value_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.alpha_value_input.editingFinished.connect(
            self.alpha_input_editing_finished_event)
        alpha_layout.addWidget(self.alpha_value_input)

        # Add alpha layout to container layout
        self.container_layout.addLayout(alpha_layout)

    def initialize_beta_field(self) -> None:
        """
        Initialize the beta field.
        :return: None
        """
        beta_layout = QHBoxLayout()

        # Add beta label
        beta_label = QLabel("Beta:")
        beta_label.setStyleSheet(f"font-size: 16px;"
                                 f"color: black;"
                                 f"font-family: {text_font};")
        beta_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                Qt.AlignmentFlag.AlignVCenter)
        beta_layout.addWidget(beta_label)

        # Add beta input field
        self.beta_value_input = QLineEdit()
        self.beta_value_input.setReadOnly(True)
        self.beta_value_input.setFixedWidth(100)
        self.beta_value_input.setPlaceholderText("Voer beta in")
        self.beta_value_input.setText("0.01")
        self.beta_value_input.setStyleSheet(self.disabled_input_stylesheet)
        self.beta_value_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.beta_value_input.editingFinished.connect(
            self.beta_input_editing_finished_event)
        beta_layout.addWidget(self.beta_value_input)

        # Add beta layout to container layout
        self.container_layout.addLayout(beta_layout)

    def initialize_auto_calculate_alpha_beta_checkbox(self) -> None:
        """
        Initialize the auto calculate alpha beta checkbox.
        :return: None
        """
        # Add auto calculate widgets
        auto_calculate_layout = QHBoxLayout()

        # Add auto calculate label
        auto_calculate_label = QLabel("Automatisch (aanbevolen):")
        auto_calculate_label.setStyleSheet(f"font-size: 16px;"
                                           f"color: black;"
                                           f"font-family: {text_font};")
        auto_calculate_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                          Qt.AlignmentFlag.AlignVCenter)
        auto_calculate_layout.addWidget(auto_calculate_label)

        # Add auto calculate checkbox
        self.auto_calculate_checkbox = QCheckBox()
        self.auto_calculate_checkbox.setFixedWidth(20)
        self.auto_calculate_checkbox.setFixedHeight(20)
        self.auto_calculate_checkbox.setStyleSheet(f"""
                    QCheckBox {{
                        font-family: {text_font};
                        color: black;
                        border: 2px solid {seco_col_blue};
                        padding: 5px;
                        background-color: white;
                        border-radius: 5px;
                        position: relative; 
                    }}

                    QCheckBox::indicator {{
                        /* Hide checkbox */
                        text-align: left;
                        width: 20;
                        height: 20;
                        border: none;
                        position: absolute;
                        left: -5px;
                    }}

                    QCheckBox::checked {{
                        background-color: {seco_col_blue};
                    }}
                """)
        self.auto_calculate_checkbox.setChecked(True)
        self.auto_calculate_checkbox.stateChanged.connect(
            self.toggle_auto_calculate_alpha_beta
        )
        auto_calculate_layout.addWidget(self.auto_calculate_checkbox)

        # Add auto calculate layout to container layout
        self.container_layout.addLayout(auto_calculate_layout)

    def toggle_auto_calculate_alpha_beta(self) -> None:
        """
        Change the alpha and beta fields to be editable or not.
        :return: None
        """
        auto_calculate = self.auto_calculate_checkbox.isChecked()
        if auto_calculate:
            self.alpha_value_input.setReadOnly(True)
            self.beta_value_input.setReadOnly(True)
        else:
            self.alpha_value_input.setReadOnly(False)
            self.beta_value_input.setReadOnly(False)

        self.change_style_of_alpha_beta_fields()
        self._model_parameters_controller.set_model_alpha_beta_custom_enabled(
            not auto_calculate)

    def change_style_of_alpha_beta_fields(self) -> None:
        """
        Change the style of the alpha and beta fields based on whether they
        are auto calculated or not.
        :return: None
        """
        auto_calculate = self.auto_calculate_checkbox.isChecked()
        if auto_calculate:
            self.alpha_value_input.setStyleSheet(
                self.disabled_input_stylesheet)
            self.beta_value_input.setStyleSheet(
                self.disabled_input_stylesheet)
        else:
            self.alpha_value_input.setStyleSheet(
                self.enabled_input_stylesheet)
            self.beta_value_input.setStyleSheet(
                self.enabled_input_stylesheet)

    def initialize_title_label(self) -> None:
        """
        Initialize the title label.
        :return: None
        """
        self.title_label = QLabel("Instellingen")
        self.title_label.setStyleSheet(f"font-size: 13px;"
                                       f"font-family: {heading_font};"
                                       f"font-weight: bold;"
                                       f"text-transform: uppercase;"
                                       f"background-color: {prim_col_red};"
                                       f"color: white;"
                                       f"border-bottom: "
                                       f"3px solid {hover_prim_col_red};")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                      Qt.AlignmentFlag.AlignTop)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_label.setFixedHeight(50)
        self.layout.addWidget(self.title_label)

    def initialize_apply_button(self) -> None:
        """
        Initialize the apply button.
        :return: None
        """
        self.apply_button = QPushButton("Toepassen")
        self.apply_button.setFixedWidth(100)
        self.apply_button.setFixedHeight(40)
        self.apply_button.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: {seco_col_blue};
                    color: white;
                }}

                QPushButton:hover {{
                    background-color: {hover_seco_col_blue};
                }}

                QPushButton:pressed {{
                    background-color: {pressed_seco_col_blue};
                }}
            """)
        self.button_layout.addWidget(self.apply_button,
                                     alignment=Qt.AlignBottom)
        self.apply_button.clicked.connect(
            self.apply_button_clicked_event)

    def fetch_topic_num(self) -> int:
        """
        Fetch the number of topics from the input field.
        :return: The number of topics from the input field, or 0 if the
        input is invalid
        """
        text = self.topic_amount.text()
        input_valid = self.validate_k_value_input()
        if input_valid:
            return int(text)
        return 0

    def validate_k_value_input(self) -> bool:
        """
        Check whether each topic modelling parameter is a valid string and
        notify the user if it isn't. It is called during an EditingFinished
        event of the input field and when the apply button is pressed.
        :return: Whether the parameters are valid
        """
        topic_input_text = self.topic_amount.text()
        valid_input = True
        try:
            num_topics = int(topic_input_text)
            if num_topics < 1 or num_topics > 999:
                valid_input = False
        except ValueError:
            valid_input = False

        if valid_input:
            self.topic_amount.setStyleSheet(self.topic_input_layout_valid)
            self.topic_amount.setPlaceholderText("")
        else:
            self.topic_amount.setStyleSheet(self.topic_input_layout_invalid)
            self.topic_amount.setText("")
            self.topic_amount.setPlaceholderText(
                "Moet tussen 1 en 999 liggen")
        return valid_input

    def validate_topic_words_input(self) -> bool:
        """
        Check whether the topic words input is a valid string and notify the
        user if it isn't. It is called during an EditingFinished event of the
        input field and when the apply button is pressed.
        :return: Whether the parameters are valid
        """
        topic_words_input_text = self.topic_words_amount_input.text()
        valid_input = True
        try:
            num_words = int(topic_words_input_text)
            if num_words < 1 or num_words > 999:
                valid_input = False
        except ValueError:
            valid_input = False

        if valid_input:
            self.topic_words_amount_input.setStyleSheet(
                self.enabled_input_stylesheet)
            self.topic_words_amount_input.setPlaceholderText("")
        else:
            self.topic_words_amount_input.setStyleSheet(
                self.disabled_input_stylesheet)
            self.topic_words_amount_input.setText("")
            self.topic_words_amount_input.setPlaceholderText(
                "Moet tussen 1 en 999 liggen")
        return valid_input

    def validate_alpha_beta_input(self) -> Type[NotImplementedError]:
        return NotImplementedError

    def topic_k_input_editing_finished_event(self) -> None:
        """
        The event when the topic input field is pressed. Updates topic
        amount in model_parameters_controller
        :return: None
        """
        self._model_parameters_controller.set_model_n_topics(
            self.fetch_topic_num())

    def topic_word_input_editing_finished_event(self) -> None:
        """
        The event when the topic word input field is pressed. Updates topic
        word amount in model_parameters_controller
        :return: None
        """
        self._model_parameters_controller.set_model_word_amount(
            int(self.topic_words_amount_input.text()))

    def alpha_input_editing_finished_event(self) -> None:
        """
        The event when the alpha input field is pressed. Updates alpha
        value in model_parameters_controller
        :return: None
        """
        self._model_parameters_controller.set_model_alpha(
            float(self.alpha_value_input.text()))

    def beta_input_editing_finished_event(self) -> None:
        """
        The event when the beta input field is pressed. Updates beta
        value in model_parameters_controller
        :return: None
        """
        self._model_parameters_controller.set_model_beta(
            float(self.beta_value_input.text()))

    def apply_button_clicked_event(self) -> None:
        """
        The event when the apply button is clicked.
        :return: None
        """
        if self.validate_k_value_input() and \
           self.validate_topic_words_input():
            self._controller.on_run_topic_modelling()

    def update_observer(self, publisher: Publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        # todo: look into whether this should still be an
        #   observer. We should probably observe changes to
        #   model parameters here.


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
