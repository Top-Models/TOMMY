from typing import Type

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QScrollArea, QLineEdit,
                               QWidget, QPushButton)

from interactive_topic_modeling.backend.observer.publisher import Publisher
from interactive_topic_modeling.support.constant_variables import (
    text_font, heading_font, seco_col_blue, hover_seco_col_blue,
    pressed_seco_col_blue)
from interactive_topic_modeling.view.observer.observer import Observer


class ModelParamsView(QScrollArea, Observer):
    """The ModelParamsDisplay that displays the model settings"""

    def __init__(self) -> None:
        """The initialization ot the ModelParamDisplay."""
        super().__init__()

        # Initialize widget properties
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

        # Add input field
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Voer aantal topics in")
        self.topic_input.setText("5")
        self.topic_input.setStyleSheet(f"border-radius: 5px;"
                                       f"font-size: 14px;"
                                       f"font-family: {text_font};"
                                       f"color: black;"
                                       f"border: 2px solid #00968F;"
                                       f"padding: 5px;"
                                       f"background-color: white;")
        self.topic_input.setAlignment(Qt.AlignLeft)
        self.container_layout.addWidget(self.topic_input)
        self.topic_input.returnPressed.connect(
            self.topic_input_return_pressed_event)

    def initialize_title_label(self) -> None:
        """
        Initialize the title label.
        :return: None
        """
        self.title_label = QLabel("Model parameters")
        self.title_label.setStyleSheet(f"font-size: 13px;"
                                       f"font-family: {heading_font};"
                                       f"font-weight: bold;"
                                       f"text-transform: uppercase;"
                                       f"background-color: {seco_col_blue};"
                                       f"color: white;"
                                       f"border-bottom: "
                                       f"3px solid {hover_seco_col_blue};")
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

    def fetch_topic_num(self) -> int:
        """
        Fetch the number of topics from the input field.
        :return: None
        """
        return int(self.topic_input.text())

    def topic_input_return_pressed_event(self) -> int:
        """
        The event when the topic input field is pressed.
        :return: The number of topics
        """
        return self.fetch_topic_num()

    def apply_button_clicked_event(self) -> NotImplementedError:
        """
        The event when the apply button is clicked.
        :return: None
        """
        return NotImplementedError()

    def update_observer(self, publisher: Publisher) -> None:
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
