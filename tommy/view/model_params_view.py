from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QScrollArea, QLineEdit,
                               QWidget, QPushButton)

from tommy.controller.controller import Controller
from tommy.support.constant_variables import (
    text_font, heading_font, seco_col_blue, hover_seco_col_blue,
    pressed_seco_col_blue, prim_col_red, hover_prim_col_red)
from tommy.controller.model_parameters_controller import (
    ModelParametersController)


class ModelParamsView(QScrollArea):
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
        self.topic_input = None
        self.topic_input_layout_valid = None
        self.topic_input_layout_invalid = None
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
        self.initialize_topic_amount_field()

    def initialize_topic_amount_field(self) -> None:
        """
        Initialize the topic amount field.
        :return: None
        """
        # Add label
        topic_label = QLabel("Aantal topics:")
        topic_label.setStyleSheet(f"font-size: 16px;"
                                  f"color: black;"
                                  f"font-family: {text_font}")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container_layout.addWidget(topic_label)

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
        self.topic_input = QLineEdit()
        # QIntValidator prevents user from typing
        # anything that isn't an integer
        self.topic_input.setValidator(QIntValidator(1, 999))
        self.topic_input.setPlaceholderText("Voer aantal topics in")
        self.topic_input.setText(
            str(self._model_parameters_controller.get_model_n_topics()))
        self.topic_input.setStyleSheet(self.topic_input_layout_valid)
        self.topic_input.setAlignment(Qt.AlignLeft)
        self.container_layout.addWidget(self.topic_input)
        self.topic_input.editingFinished.connect(
            self.topic_input_editing_finished_event)

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
        text = self.topic_input.text()
        input_valid = self.validate_input()
        if input_valid:
            return int(text)
        return 0

    def validate_input(self) -> bool:
        """
        Check whether each topic modelling parameter is a valid string and
        notify the user if it isn't. It is called during an EditingFinished
        event of the input field and when the apply button is pressed.
        :return: Whether the parameters are valid
        """
        topic_input_text = self.topic_input.text()
        valid_input = True
        try:
            num_topics = int(topic_input_text)
            if num_topics < 1 or num_topics > 999:
                valid_input = False
        except ValueError:
            valid_input = False

        if valid_input:
            self.topic_input.setStyleSheet(self.topic_input_layout_valid)
            self.topic_input.setPlaceholderText("")
        else:
            self.topic_input.setStyleSheet(self.topic_input_layout_invalid)
            self.topic_input.setText("")
            self.topic_input.setPlaceholderText(
                "Moet tussen 1 en 999 liggen")
        return valid_input

    def topic_input_editing_finished_event(self) -> None:
        """
        The event when the topic input field is pressed. Updates topic
        amount in model_parameters_controller
        :return: None
        """
        self._model_parameters_controller.set_model_n_topics(
            self.fetch_topic_num())

    def apply_button_clicked_event(self) -> None:
        """
        The event when the apply button is clicked.
        :return: None
        """
        if self.validate_input():
            self._controller.on_run_topic_modelling()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""