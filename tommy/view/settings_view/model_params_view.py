from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QScrollArea, QWidget,
                               QPushButton, QApplication, QHBoxLayout)

from tommy.controller.config_controller import ConfigController
from tommy.controller.controller import Controller
from tommy.controller.language_controller import LanguageController
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.controller.topic_modelling_controller import \
    TopicModellingController
from tommy.controller.topic_modelling_runners.abstract_topic_runner import \
    TopicRunner
from tommy.model.model_parameters_model import ModelParametersModel
from tommy.support.constant_variables import (
    text_font, heading_font, seco_col_blue, hover_seco_col_blue,
    pressed_seco_col_blue, prim_col_red, hover_prim_col_red, disabled_gray,
    extra_light_gray, scrollbar_style)
from tommy.support.model_type import ModelType
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings
from tommy.view.settings_view.abstract_settings.bert_settings import (
    BertSettings)
from tommy.view.settings_view.abstract_settings.lda_settings import LdaSettings
from tommy.view.settings_view.abstract_settings.nmf_settings import NmfSettings


class ModelParamsView(QScrollArea):
    """The ModelParamsDisplay that displays the model settings"""

    def __init__(self, model_parameters_controller: ModelParametersController,
                 language_controller: LanguageController,
                 config_controller: ConfigController,
                 topic_modelling_controller: TopicModellingController) -> None:
        """The initialization of the ModelParamDisplay."""
        super().__init__()
        self.setObjectName("model_params_display")
        self.setContentsMargins(0, 0, 0, 0)

        # Set reference to the model parameters controller
        self._model_parameters_controller = model_parameters_controller
        self._model_parameters_controller.algorithm_changed_event.subscribe(
            lambda _: self.model_type_changed_event())
        self._topic_modelling_controller = topic_modelling_controller
        self._topic_modelling_controller.model_trained_event.subscribe(
            lambda _: self._reset_apply_button_on_model_trained())
        self._config_controller = config_controller

        # Subscribe to the event when the config changes
        self._model_parameters_controller.params_model_changed_event.subscribe(
            self._update_ui_on_model_params_switch)
        language_controller.language_model_changed_event.subscribe(
            self._update_ui_on_language_model_switch)

        # Initialize model settings
        self.algorithm_specific_settings_views: dict[
            ModelType, AbstractSettings] = {
            ModelType.LDA: LdaSettings(self._model_parameters_controller,
                                       self._config_controller,
                                       language_controller),
            ModelType.BERTopic: BertSettings(self._model_parameters_controller,
                                             self._config_controller,
                                             language_controller),
            ModelType.NMF: NmfSettings(self._model_parameters_controller,
                                       self._config_controller,
                                       language_controller)
        }

        # Initialize widget properties
        self.setFixedWidth(250)
        self.setMinimumHeight(350)

        # Apply stylesheet to model_params_display object
        self.setStyleSheet(f"""
            QWidget#model_params_display {{
                border-bottom: 3px solid lightgray;
            }}

            QWidget#model_params_display QWidget {{
                background-color: rgba(230, 230, 230, 230);
            }}
            """)

        self.enabled_input_stylesheet = (f"background-color: white;"
                                         f"font-size: 14px;"
                                         f"font-family: {text_font};"
                                         f"color: black;"
                                         f"border: 2px solid {seco_col_blue};"
                                         f"padding: 5px;")
        self.disabled_input_stylesheet = (f"background-color: {disabled_gray};"
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

        # Style the scroll area
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: 0px;
                border-bottom: 3px solid lightgray;
            }}
            """ + scrollbar_style)

        # Initialize button widgets
        self.apply_button = None

        # Initialize button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignRight)
        self.button_layout.setSpacing(10)

        # Add widgets to the layout
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
        current_view = self.get_current_settings_view()
        current_view.initialize_parameter_widgets(self.scroll_layout)
        current_view.set_field_values_from_backend()
        self.initialize_apply_button()

    def clear_layouts_from_scroll_layout(self) -> None:
        """
        Clear the layouts from the scroll layout.

        :return: None
        """
        layout = self.scroll_layout

        # While layout is not empty
        while layout.count():
            child = layout.takeAt(0)

            # If there is a widget
            if child.widget() is not None:
                # Delete the widget
                child.widget().deleteLater()

            # If there is a layout
            elif child.layout() is not None:
                # Delete all widgets in the layout
                while child.layout().count():
                    sub_child = child.layout().takeAt(0)
                    if sub_child.widget() is not None:
                        sub_child.widget().deleteLater()

    def clear_layouts_from_button_layout(self) -> None:
        """
        Clear the layouts from the button layout.

        :return: None
        """
        layout = self.button_layout

        # While layout is not empty
        while layout.count():
            child = layout.takeAt(0)

            # If there is a widget
            if child.widget() is not None:
                # Delete the widget
                child.widget().deleteLater()

            # If there is a layout
            elif child.layout() is not None:
                # Delete all widgets in the layout
                while child.layout().count():
                    sub_child = child.layout().takeAt(0)
                    if sub_child.widget() is not None:
                        sub_child.widget().deleteLater()

    def initialize_apply_button(self) -> None:
        """
        Initialize the apply button.

        :return: None
        """
        self.clear_layouts_from_button_layout()
        self.apply_button = QPushButton("TOEPASSEN")
        self.apply_button.setFixedHeight(40)
        self.apply_button.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: {seco_col_blue};
                    color: white;
                    font-family: {heading_font};
                    font-size: 12px;
                    font-weight: bold;
                }}

                QPushButton:hover {{
                    background-color: {hover_seco_col_blue};
                }}

                QPushButton:pressed {{
                    background-color: {pressed_seco_col_blue};
                }}
            """)
        self.apply_button.clicked.connect(self.apply_button_clicked_event)
        self.button_layout.addWidget(self.apply_button, stretch=1)
        self.layout.addLayout(self.button_layout)

    def get_current_settings_view(self) -> AbstractSettings:
        """
        Get the current settings view.

        :return: AbstractSettings
        """
        current_model_type = self._model_parameters_controller.get_model_type()
        return self.algorithm_specific_settings_views[current_model_type]

    def apply_button_clicked_event(self) -> None:
        """
        The event when the apply button is clicked.

        :return: None
        """
        current_model_type = self._model_parameters_controller.get_model_type()
        current_view = self.algorithm_specific_settings_views[
            current_model_type]
        # Disable the apply button and change its text to "Laden..."
        self.apply_button.setEnabled(False)
        self.apply_button.setText("LADEN...")
        self.apply_button.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: #808080;
                    color: white;
                    font-family: {heading_font};
                    font-size: 12px;
                    font-weight: bold;
                }}

                QPushButton:hover {{
                    background-color: {hover_seco_col_blue};
                }}

                QPushButton:pressed {{
                    background-color: {pressed_seco_col_blue};
                }}
            """)

        # Apply the settings
        if current_view.all_fields_valid():
            self.disable_input_fields_on_model_training()
            self._topic_modelling_controller.train_model()

    def disable_input_fields_on_model_training(self) -> None:
        """
        Disable the input fields when the model is training.

        :return: None
        """
        current_view = self.get_current_settings_view()
        current_view.disable_input_fields_on_model_training()

    def _reset_apply_button_on_model_trained(self) -> None:
        """
        Re-enable the apply button and restore its text when training is
        complete.
        :return: None
        """
        current_view = self.get_current_settings_view()
        current_view.enable_input_fields_on_model_trained()

        # Change the apply button back to its original state
        self.apply_button.setEnabled(True)
        self.apply_button.setText("TOEPASSEN")
        self.apply_button.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: {seco_col_blue};
                    color: white;
                    font-family: {heading_font};
                    font-size: 12px;
                    font-weight: bold;
                }}

                QPushButton:hover {{
                    background-color: {hover_seco_col_blue};
                }}

                QPushButton:pressed {{
                    background-color: {pressed_seco_col_blue};
                }}
            """)

    def model_type_changed_event(self) -> None:
        """
        The event when the model type is changed.

        :return: None
        """
        self.clear_layouts_from_scroll_layout()
        self.initialize_parameter_widgets()

    def _update_ui_on_model_params_switch(self, data: None) -> None:
        self.model_type_changed_event()

    def _update_ui_on_language_model_switch(self, data: None) -> None:
        settings_view = self.get_current_settings_view()
        settings_view.set_field_values_from_backend()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
