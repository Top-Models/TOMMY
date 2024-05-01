from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QCheckBox, \
    QVBoxLayout

from tommy.support.constant_variables import text_font, seco_col_blue
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings


class LdaSettings(AbstractSettings):
    """
    Class for LDA settings
    """

    def __init__(self,
                 model_parameters_controller):
        """
        Constructor for LDA settings

        :param model_parameters_controller: ModelParametersController
        """
        super().__init__(model_parameters_controller)

        self._alpha_value_input = QLineEdit()
        self._beta_value_input = QLineEdit()
        self._auto_calc_alpha_beta_checkbox = QCheckBox()

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
        alpha_label.setStyleSheet(f"font-size: 16px;"
                                  f"color: black;"
                                  f"font-family: {text_font};")
        alpha_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                 Qt.AlignmentFlag.AlignVCenter)
        alpha_layout.addWidget(alpha_label)

        # Add alpha input field
        self._alpha_value_input = QLineEdit()
        self._alpha_value_input.setValidator(QDoubleValidator())
        self._alpha_value_input.setReadOnly(True)
        self._alpha_value_input.setFixedWidth(100)
        self._alpha_value_input.setPlaceholderText("Voer alpha in")
        self._alpha_value_input.setText("-:-")
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
        self._model_parameters_controller.set_model_alpha(
            float(self._alpha_value_input.text()))

    def validate_alpha_field(self) -> bool:
        """
        Validate the alpha field

        :return: bool
        """
        is_valid = True

        # Check if alpha is auto calculated
        if self._auto_calc_alpha_beta_checkbox.isChecked():
            is_valid = True

        # Check if alpha is 0
        if self._alpha_value_input.text() == "0":
            is_valid = False

        # Check if alpha is a valid float
        try:
            alpha = float(self._alpha_value_input.text())
            if alpha < 0:
                is_valid = False
        except ValueError:
            is_valid = False

        if not is_valid:
            self._alpha_value_input.setStyleSheet(
                self.topic_input_layout_invalid)
            return False

        self._alpha_value_input.setStyleSheet(self.topic_input_layout_valid)
        return True

    def initialize_beta_field(self):
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
        self._beta_value_input = QLineEdit()
        self._beta_value_input.setValidator(QDoubleValidator())
        self._beta_value_input.setReadOnly(True)
        self._beta_value_input.setFixedWidth(100)
        self._beta_value_input.setPlaceholderText("Voer beta in")
        self._beta_value_input.setText("-:-")
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
            is_valid = True

        # Check if beta is 0
        if self._beta_value_input.text() == "0":
            is_valid = False

        # Check if beta is a valid float
        try:
            beta = float(self._beta_value_input.text())
            if beta < 0:
                is_valid = False
        except ValueError:
            is_valid = False

        if not is_valid:
            self._beta_value_input.setStyleSheet(
                self.topic_input_layout_invalid)
            return False

        self._beta_value_input.setStyleSheet(self.topic_input_layout_valid)
        return True

    def initialize_auto_calculate_alpha_beta_checkbox(self) -> None:
        """
        Initialize the auto calculate alpha beta checkbox

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
        self._auto_calc_alpha_beta_checkbox = QCheckBox()
        self._auto_calc_alpha_beta_checkbox.setFixedWidth(20)
        self._auto_calc_alpha_beta_checkbox.setFixedHeight(20)
        self._auto_calc_alpha_beta_checkbox.setStyleSheet(f"""
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
        if auto_calculate:
            self._alpha_value_input.setText("-:-")
            self._beta_value_input.setText("-:-")
            self._alpha_value_input.setReadOnly(True)
            self._beta_value_input.setReadOnly(True)
        else:
            alpha_value = self._model_parameters_controller.get_model_alpha()
            beta_value = self._model_parameters_controller.get_model_beta()
            self._alpha_value_input.setText(str(alpha_value))
            self._beta_value_input.setText(str(beta_value))
            self._alpha_value_input.setReadOnly(False)
            self._beta_value_input.setReadOnly(False)

        self.change_style_of_alpha_beta_fields()
        self._model_parameters_controller.set_model_alpha_beta_custom_enabled(
            not auto_calculate)

    def change_style_of_alpha_beta_fields(self) -> None:
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


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
