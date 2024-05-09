from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QCheckBox, \
    QVBoxLayout

from tommy.support.constant_variables import text_font, seco_col_blue
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings


class BertSettings(AbstractSettings):
    """
    Class for BERT settings
    """

    def __init__(self,
                 model_parameters_controller):
        """
        Constructor for BERT settings

        :param model_parameters_controller: ModelParametersController
        """
        super().__init__(model_parameters_controller)

        self._delta_value = QLineEdit()

    def initialize_parameter_widgets(self,
                                     scroll_layout: QVBoxLayout) -> None:
        """
        Initialize the parameter widgets

        :return: None
        """
        super().initialize_parameter_widgets(scroll_layout)
        self.add_header_label("Hyperparameters", 17)
        self.initialize_delta_field()

    def all_fields_valid(self) -> bool:
        """
        Validate all fields

        :return: bool
        """
        return (super().all_fields_valid() and
                self.validate_delta_field())

    def initialize_delta_field(self) -> None:
        """
        Initialize the delta field

        :return: None
        """
        delta_layout = QHBoxLayout()

        # Add alpha label
        delta_label = QLabel("Delta:")
        delta_label.setStyleSheet(f"font-size: 16px;"
                                  f"color: black;"
                                  f"font-family: {text_font};")
        delta_label.setAlignment(Qt.AlignmentFlag.AlignLeft |

                                 Qt.AlignmentFlag.AlignVCenter)
        delta_layout.addWidget(delta_label)

        # Add alpha input field
        self._delta_value_input = QLineEdit()
        self._delta_value_input.setValidator(QDoubleValidator())
        self._delta_value_input.setReadOnly(True)
        self._delta_value_input.setFixedWidth(100)
        self._delta_value_input.setPlaceholderText("Voer Delta in")
        self._delta_value_input.setText("-:-")
        self._delta_value_input.setStyleSheet(self.disabled_input_stylesheet)
        self._delta_value_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._delta_value_input.editingFinished.connect(
            self.delta_input_editing_finished_event)
        delta_layout.addWidget(self._delta_value_input)

        # Add alpha layout to container layout
        self._scroll_layout.addLayout(delta_layout)

    def delta_input_editing_finished_event(self):
        """
        Event handler for when the alpha field is edited

        :return: None
        """
        self._model_parameters_controller.set_model_alpha(
            float(self._delta_value_input.text()))

    def validate_gamma_field(self) -> bool:
        """
        Validate the alpha field

        :return: bool
        """
        is_valid = True

        # Check if alpha is a valid float
        try:
            alpha = float(self._delta_value_input.text())
            if alpha <= 0:
                is_valid = False
        except ValueError:
            is_valid = False

        if not is_valid:
            self._delta_value_input.setStyleSheet(
                self.topic_input_layout_invalid)
            return False

        self._delta_value_input.setStyleSheet(self.enabled_input_stylesheet)
        return True


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
