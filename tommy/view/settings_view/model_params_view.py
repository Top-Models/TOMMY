from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QScrollArea, QWidget,
                               QPushButton)

from tommy.controller.controller import Controller
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.controller.publisher.publisher import Publisher
from tommy.support.constant_variables import (
    text_font, heading_font, seco_col_blue, hover_seco_col_blue,
    pressed_seco_col_blue, prim_col_red, hover_prim_col_red, disabled_gray)
from tommy.support.model_type import ModelType
from tommy.view.observer.observer import Observer
from tommy.view.settings_view.abstract_settings.lda_settings import LdaSettings


class ModelParamsView(QScrollArea, Observer):
    """The ModelParamsDisplay that displays the model settings"""

    def __init__(self, model_parameters_controller: ModelParametersController,
                 controller: Controller,
                 ) -> None:
        """The initialization ot the ModelParamDisplay."""
        super().__init__()

        self.setObjectName("model_params_display")
        self.setContentsMargins(0, 0, 0, 0)

        # Set reference to the model parameters controller
        self._model_parameters_controller = model_parameters_controller
        self._controller = controller

        # Initialize widget properties
        self.setFixedWidth(250)

        # Apply stylesheet to model_params_display object
        self.setStyleSheet(
            """
            QWidget#model_params_display {
                border-bottom: 3px solid lightgrey;
            }
            
            QWidget#model_params_display QWidget {
                background-color: rgba(230, 230, 230, 230);
            }
            """
        )

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
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)

        # Initialize title label
        self.title_label = None
        self.initialize_title_label()

        # Initialize scroll area and its layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_widget)

        # Initialize topic widgets
        self.apply_button = None

        # Initialize button layout
        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.scroll_area)

        # Add settings to the model parameters controller
        self._model_parameters_controller.add_settings_view(
            ModelType.LDA,
            LdaSettings(self._model_parameters_controller,
                        self.scroll_layout))

        # Initialize parameter widgets
        self.initialize_parameter_widgets()

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

    # TODO: Make this method more dynamic
    def initialize_parameter_widgets(self) -> None:
        """
        Initialize the parameter widgets.
        """
        # TODO: Add headers to the different sections
        current_view = (self._model_parameters_controller.
                        get_current_settings_view())
        current_view.initialize_parameter_widgets()
        self.initialize_apply_button()

    def clear_layouts_from_scroll_layout(self) -> None:
        """
        Clear the layouts from the scroll layout.
        :return: None
        """
        for i in reversed(range(self.scroll_layout.count())):
            layout = self.scroll_layout.itemAt(i)

            # Skip button layout
            if layout is self.button_layout:
                continue

            if layout is not None:
                for j in reversed(range(layout.count())):
                    widget = layout.itemAt(j).widget()
                    if widget is not None:
                        widget.deleteLater()
                layout.deleteLater()

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
        self.apply_button.clicked.connect(self.apply_button_clicked_event)
        self.scroll_layout.addLayout(self.button_layout, stretch=1)

    def apply_button_clicked_event(self) -> None:
        """
        The event when the apply button is clicked.
        :return: None
        """
        current_view = (self._model_parameters_controller.
                        get_current_settings_view())
        if current_view.all_fields_valid():
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
