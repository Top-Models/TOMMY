from PySide6.QtWidgets import QVBoxLayout

from tommy.controller.language_controller import LanguageController
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings


class NmfSettings(AbstractSettings):
    """
    Class for NMF settings
    """

    def __init__(self,
                 model_parameters_controller,
                 config_controller,
                 language_controller: LanguageController):
        """
        Constructor for NMF settings

        :param model_parameters_controller: ModelParametersController
        """
        super().__init__(model_parameters_controller,
                         config_controller,
                         language_controller)

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
