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

    def initialize_parameter_widgets(self,
                                     scroll_layout: QVBoxLayout) -> None:
        """
        Initialize the parameter widgets

        :return: None
        """
        super().initialize_parameter_widgets(scroll_layout)

    def all_fields_valid(self) -> bool:
        """
        Validate all fields

        :return: bool
        """
        return super().all_fields_valid()

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
