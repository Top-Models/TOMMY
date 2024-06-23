from PySide6.QtCore import QRegularExpression as QRegExp
from PySide6.QtCore import Qt
from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QCheckBox, \
    QVBoxLayout

from tommy.controller.language_controller import LanguageController
from tommy.support.constant_variables import (text_font, seco_col_blue,
                                              disabled_gray,
                                              settings_label_font)
from tommy.support.parameter_limits import alpha_min_value, beta_min_value
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings


class LdaSettings(AbstractSettings):
    """
    Class for LDA settings
    """

    allowed_expressions = QRegExp(r"^[0-9]+(\.[0-9]+)?$")

    def __init__(self,
                 model_parameters_controller,
                 config_controller,
                 language_controller: LanguageController):
        """
        Constructor for LDA settings

        :param model_parameters_controller: ModelParametersController
        """
        super().__init__(model_parameters_controller,
                         config_controller,
                         language_controller)

        model_parameters_controller.n_topics_changed_event.subscribe(
            self.on_n_topics_changed)
        self._alpha_value_input = QLineEdit()
        self._beta_value_input = QLineEdit()
        self._auto_calc_alpha_beta_checkbox = QCheckBox()
        self._enabled_checkbox_stylesheet = f"""
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
                        """
        self._disabled_checkbox_stylesheet = f"""
                            QCheckBox {{
                                font-family: {text_font};
                                color: black;
                                border: 2px solid {seco_col_blue};
                                padding: 5px;
                                background-color: {disabled_gray};
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
                                background-color: {disabled_gray};
                            }}
                        """

    def initialize_parameter_widgets(self,
                                     scroll_layout: QVBoxLayout) -> None:
        """
        Initialize the parameter widgets

        :return: None
        """
        super().initialize_parameter_widgets(scroll_layout)
        self.add_header_label("Hyperparameters", 17)
        self.initialize_alpha_field()
        self.initialize_beta_field()
        self.initialize_auto_calculate_alpha_beta_checkbox()
        self.add_margin(10)

    def all_fields_valid(self) -> bool:
        """
        Validate all fields

        :return: bool
        """
        return (super().all_fields_valid() and
                self.validate_alpha_field() and
                self.validate_beta_field())

    def initialize_alpha_field(self) -> None:
        """
        Initialize the alpha field

        :return: None
        """
        alpha_layout = QHBoxLayout()

        # Add alpha label
        alpha_label = QLabel("Alpha:")
        alpha_label.setFont(settings_label_font)
        alpha_label.setStyleSheet(f"font-size: 16px;"
                                  f"color: black;"
                                  f"font-family: {text_font};")
        alpha_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                 Qt.AlignmentFlag.AlignVCenter)
        alpha_layout.addWidget(alpha_label)

        # Add alpha input field
        self._alpha_value_input = QLineEdit()
        self._alpha_value_input.setFont(settings_label_font)
        self._alpha_value_input.setValidator(
            QRegExpValidator(self.allowed_expressions))
        self._alpha_value_input.setReadOnly(True)
        self._alpha_value_input.setFixedWidth(100)
        self._alpha_value_input.setPlaceholderText("Voer alpha in")
        alpha_beta_auto_string = self.get_alpha_beta_auto_string()
        self._alpha_value_input.setText(alpha_beta_auto_string)
        self._alpha_value_input.setStyleSheet(self.disabled_input_stylesheet)
        self._alpha_value_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._alpha_value_input.editingFinished.connect(
            self.alpha_input_editing_finished_event)
        alpha_layout.addWidget(self._alpha_value_input)

        # Add alpha layout to container layout
        self._scroll_layout.addLayout(alpha_layout)

    def alpha_input_editing_finished_event(self):
        """
        Event handler for when the alpha field is edited

        :return: None
        """
        alpha = self._alpha_value_input.text()
        self._model_parameters_controller.set_model_alpha(float(alpha))

    def validate_alpha_field(self) -> bool:
        """
        Validate the alpha field

        :return: bool
        """
        is_valid = True

        # Check if alpha is auto calculated
        if self._auto_calc_alpha_beta_checkbox.isChecked():
            self._alpha_value_input.setStyleSheet(
                self.disabled_input_stylesheet)
            return True

        # Check if alpha is a valid float
        try:
            alpha = float(self._alpha_value_input.text())
            if alpha <= alpha_min_value:
                is_valid = False
        except ValueError:
            is_valid = False

        if not is_valid:
            self._alpha_value_input.setStyleSheet(
                self.topic_input_layout_invalid)
            self._alpha_value_input.setText("")
            self._alpha_value_input.setPlaceholderText(
                f"Alpha > {alpha_min_value}")
            return False

        self._alpha_value_input.setStyleSheet(self.enabled_input_stylesheet)
        return True

    def initialize_beta_field(self):
        """
        Initialize the beta field.

        :return: None
        """
        beta_layout = QHBoxLayout()

        # Add beta label
        beta_label = QLabel("Beta:")
        beta_label.setFont(settings_label_font)
        beta_label.setStyleSheet(f"font-size: 16px;"
                                 f"color: black;"
                                 f"font-family: {text_font};")
        beta_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                Qt.AlignmentFlag.AlignVCenter)
        beta_layout.addWidget(beta_label)

        # Add beta input field
        self._beta_value_input = QLineEdit()
        self._beta_value_input.setValidator(
            QRegExpValidator(self.allowed_expressions))
        self._beta_value_input.setFont(settings_label_font)
        self._beta_value_input.setReadOnly(True)
        self._beta_value_input.setFixedWidth(100)
        self._beta_value_input.setPlaceholderText("Voer beta in")
        alpha_beta_auto_string = self.get_alpha_beta_auto_string()
        self._beta_value_input.setText(alpha_beta_auto_string)
        self._beta_value_input.setStyleSheet(self.disabled_input_stylesheet)
        self._beta_value_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._beta_value_input.editingFinished.connect(
            self.beta_input_editing_finished_event)
        beta_layout.addWidget(self._beta_value_input)

        # Add beta layout to container layout
        self._scroll_layout.addLayout(beta_layout)

    def beta_input_editing_finished_event(self):
        """
        Event handler for when the beta field is edited

        :return: None
        """
        self._model_parameters_controller.set_model_beta(
            float(self._beta_value_input.text()))

    def validate_beta_field(self) -> bool:
        """
        Validate the beta field

        :return: bool
        """
        is_valid = True

        # Check if beta is auto calculated
        if self._auto_calc_alpha_beta_checkbox.isChecked():
            self._beta_value_input.setStyleSheet(
                self.disabled_input_stylesheet)
            return True

        # Check if beta is a valid float
        try:
            beta = float(self._beta_value_input.text())
            if beta <= beta_min_value:
                is_valid = False
        except ValueError:
            is_valid = False

        if not is_valid:
            self._beta_value_input.setStyleSheet(
                self.topic_input_layout_invalid)
            self._beta_value_input.setText("")
            self._beta_value_input.setPlaceholderText(
                f"Beta > {beta_min_value}")
            return False

        self._beta_value_input.setStyleSheet(self.enabled_input_stylesheet)
        return True

    def initialize_auto_calculate_alpha_beta_checkbox(self) -> None:
        """
        Initialize the auto calculate alpha beta checkbox

        :return: None
        """
        # Add auto calculate widgets
        auto_calculate_layout = QHBoxLayout()

        # Add auto calculate label
        auto_calculate_label = QLabel("Standaard:")
        auto_calculate_label.setFont(settings_label_font)
        auto_calculate_label.setStyleSheet(f"font-size: 16px;"
                                           f"color: black;"
                                           f"font-family: {text_font};")
        auto_calculate_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                          Qt.AlignmentFlag.AlignVCenter)
        auto_calculate_layout.addWidget(auto_calculate_label)

        # Add auto calculate checkbox
        self._auto_calc_alpha_beta_checkbox = QCheckBox()
        self._auto_calc_alpha_beta_checkbox.setFont(settings_label_font)
        self._auto_calc_alpha_beta_checkbox.setFixedWidth(20)
        self._auto_calc_alpha_beta_checkbox.setFixedHeight(20)
        self._auto_calc_alpha_beta_checkbox.setStyleSheet(
            self._enabled_checkbox_stylesheet)
        self._auto_calc_alpha_beta_checkbox.setChecked(True)
        self._auto_calc_alpha_beta_checkbox.stateChanged.connect(
            self.toggle_auto_calculate_alpha_beta
        )
        auto_calculate_layout.addWidget(self._auto_calc_alpha_beta_checkbox)

        # Add auto calculate layout to container layout
        self._scroll_layout.addLayout(auto_calculate_layout)

    def toggle_auto_calculate_alpha_beta(self) -> None:
        """
        Toggle the auto calculate alpha beta checkbox

        :return: None
        """
        auto_calculate = self._auto_calc_alpha_beta_checkbox.isChecked()
        alpha_value = self._model_parameters_controller.get_model_alpha()
        beta_value = self._model_parameters_controller.get_model_beta()

        self._change_text_of_alpha_beta_fields(alpha_value, beta_value,
                                               auto_calculate)

        self._change_style_of_alpha_beta_fields()
        self._model_parameters_controller.set_model_alpha_beta_custom_enabled(
            not auto_calculate)

    def _change_style_of_alpha_beta_fields(self) -> None:
        """
        Change the style of the alpha and beta fields based on whether they
        are auto calculated or not.

        :return: None
        """
        auto_calculate = self._auto_calc_alpha_beta_checkbox.isChecked()
        if auto_calculate:
            self._alpha_value_input.setStyleSheet(
                self.disabled_input_stylesheet)
            self._beta_value_input.setStyleSheet(
                self.disabled_input_stylesheet)
        else:
            self._alpha_value_input.setStyleSheet(
                self.enabled_input_stylesheet)
            self._beta_value_input.setStyleSheet(
                self.enabled_input_stylesheet)

    def _change_text_of_alpha_beta_fields(self, alpha: float, beta: float,
                                          auto_calculate: bool) -> None:
        """
        Change the text in the alpha and beta input fields to the automatic
        value if auto_calculate is true
        :param alpha:
        :param beta:
        :param auto_calculate:
        :return:
        """
        alpha_beta_auto_string = self.get_alpha_beta_auto_string()
        alpha_text = alpha_beta_auto_string if auto_calculate else str(alpha)
        beta_text = alpha_beta_auto_string if auto_calculate else str(beta)
        self._alpha_value_input.setText(alpha_text)
        self._beta_value_input.setText(beta_text)
        self._alpha_value_input.setReadOnly(auto_calculate)
        self._beta_value_input.setReadOnly(auto_calculate)

    def set_field_values_from_backend(self) -> None:
        """
        Get the parameter values from the backend and put them in the
        text boxes in the frontend
        :return: None
        """
        super().set_field_values_from_backend()
        auto_calculate = not (self._model_parameters_controller
                              .get_model_alpha_beta_custom_enabled())
        self._change_text_of_alpha_beta_fields(
            self._model_parameters_controller.get_model_alpha(),
            self._model_parameters_controller.get_model_beta(),
            auto_calculate)
        self._auto_calc_alpha_beta_checkbox.setChecked(auto_calculate)

    def disable_checkbox(self, checkbox: QCheckBox) -> None:
        """
        Disable the checkbox

        :param checkbox: QCheckBox
        :return: None
        """
        checkbox.setEnabled(False)
        checkbox.setStyleSheet(self._disabled_checkbox_stylesheet)

    def enable_checkbox(self, checkbox: QCheckBox) -> None:
        """
        Enable the auto checkbox

        :param checkbox: QCheckBox
        :return: None
        """
        checkbox.setEnabled(True)
        checkbox.setStyleSheet(self._enabled_checkbox_stylesheet)

    def disable_input_fields_on_model_training(self) -> None:
        """
        Disable the input fields when the model is training
        :return: None
        """
        super().disable_input_fields_on_model_training()
        self.disable_input_field(self._alpha_value_input)
        self.disable_input_field(self._beta_value_input)
        self.disable_checkbox(self._auto_calc_alpha_beta_checkbox)

    def enable_input_fields_on_model_trained(self) -> None:
        """
        Enable the input fields when the model is training
        :return: None
        """
        super().enable_input_fields_on_model_trained()
        self.enable_checkbox(self._auto_calc_alpha_beta_checkbox)
        if self._auto_calc_alpha_beta_checkbox.isChecked():
            return

        self.enable_input_field(self._alpha_value_input)
        self.enable_input_field(self._beta_value_input)

    def get_alpha_beta_auto_string(self) -> str:
        """Get the automatic alpha and beta value string based on n_topics"""
        n_topics = self._model_parameters_controller.get_model_n_topics()
        return self.create_alpha_beta_auto_string(n_topics)

    @staticmethod
    def create_alpha_beta_auto_string(n_topics: int) -> str:
        """Create the string depicting the automatic value of alpha/beta"""
        return f"{1 / max(1, n_topics):.2g}"

    def on_n_topics_changed(self, n_topics: int) -> None:
        """Update the substitute strings of alpha/beta based on n_topics"""
        if self._auto_calc_alpha_beta_checkbox.isChecked():
            new_substitute_text = self.create_alpha_beta_auto_string(n_topics)
            self._alpha_value_input.setText(new_substitute_text)
            self._beta_value_input.setText(new_substitute_text)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
