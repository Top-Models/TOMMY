from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QScrollArea, QWidget,
                               QPushButton)

from tommy.controller.config_controller import ConfigController
from tommy.controller.controller import Controller
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.support.constant_variables import (
    text_font, heading_font, seco_col_blue, hover_seco_col_blue,
    pressed_seco_col_blue, prim_col_red, hover_prim_col_red, disabled_gray)
from tommy.support.model_type import ModelType
from tommy.view.config_view import ConfigView
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings
from tommy.view.settings_view.abstract_settings.lda_settings import LdaSettings


class ModelParamsView(QScrollArea):
    """The ModelParamsDisplay that displays the model settings"""

    def __init__(self, model_parameters_controller: ModelParametersController,
                 controller: Controller,
                 config_controller: ConfigController) -> None:
        """The initialization ot the ModelParamDisplay."""
        super().__init__()

        self.setObjectName("model_params_display")
        self.setContentsMargins(0, 0, 0, 0)

        # Set reference to the model parameters controller
        self._model_parameters_controller = model_parameters_controller
        self._controller = controller
        self._config_controller = config_controller

        # Subscribe to the event when the config changes
        self._model_parameters_controller.params_model_changed_event.subscribe(
            self._update_model_params)

        # Initialize model settings
        self.SETTINGS_VIEWS: dict[ModelType, AbstractSettings] = {
            ModelType.LDA: LdaSettings(self._model_parameters_controller)
        }

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

        # Initialize button widgets
        self.apply_button = None

        # TODO: Frontend people make this pretty
        self.config_management_button = None

        # Initialize button layout
        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.scroll_area)

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

    def initialize_parameter_widgets(self) -> None:
        """
        Initialize the parameter widgets.
        """
        self.initialize_config_button()
        current_view = self.get_current_settings_view()
        current_view.initialize_parameter_widgets(self.scroll_layout)
        self.initialize_apply_button()

    def clear_layouts_from_scroll_layout(self) -> None:
        """
        Clear the layouts from the scroll layout.

        :return: None
        """
        for i in reversed(range(self.scroll_layout.count())):
            layout = self.scroll_layout.itemAt(i)

            if layout is not None:
                for j in reversed(range(layout.count())):
                    widget = layout.itemAt(j).widget()
                    if widget is not None:
                        widget.deleteLater()
                layout.deleteLater()

    def open_config_management_widget(self):
        """Method to open the configuration management widget"""
        config_management_widget = ConfigView(
            self._config_controller, self._model_parameters_controller)
        config_management_widget.exec()

    def initialize_config_button(self) -> None:
        """
        Initialize the button that opens the config view
        TODO: Frontend people make this pretty
        :return:
        """
        self.config_management_button = QPushButton("Beheer Configuraties")
        self.config_management_button.setStyleSheet(
            f"""
                            QPushButton {{
                                background-color: {seco_col_blue};
                                color: white;
                                border-radius: 5px;
                                padding: 10px 20px;
                                font-size: 14px;
                                font-family: {text_font};
                            }}

                            QPushButton:hover {{
                                background-color: {hover_seco_col_blue};
                            }}

                            QPushButton:pressed {{
                                background-color: {pressed_seco_col_blue};
                            }}
                            """
        )
        self.config_management_button.clicked.connect(
            self.open_config_management_widget)
        self.button_layout.addWidget(self.config_management_button,
                                     alignment=Qt.AlignTop)

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

    def get_current_settings_view(self) -> AbstractSettings:
        """
        Get the current settings view.

        :return: AbstractSettings
        """
        current_model_type = self._model_parameters_controller.get_model_type()
        return self.SETTINGS_VIEWS[current_model_type]

    def apply_button_clicked_event(self) -> None:
        """
        The event when the apply button is clicked.

        :return: None
        """
        current_model_type = self._model_parameters_controller.get_model_type()
        current_view = self.SETTINGS_VIEWS[current_model_type]
        if current_view.all_fields_valid():
            self._controller.on_run_topic_modelling()

    def model_type_changed_event(self) -> None:
        """
        The event when the model type is changed.

        :return: None
        """
        self.clear_layouts_from_scroll_layout()
        self.initialize_parameter_widgets()

    def _update_model_params(self, data: tuple[int, ModelType]):
        # TODO: update the parameters in the text input fields
        num_topics, model_type = data
        # self.topic_input.setText(str(num_topics))


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
