from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QCheckBox,
                               QVBoxLayout)

from tommy.controller.language_controller import LanguageController
from tommy.support.constant_variables import text_font, seco_col_blue
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings


class BertSettings(AbstractSettings):
    """
    Class for BERT settings
    """
    MIN_DF_MIN_VALUE = 0
    MIN_DF_MAX_VALUE = 1_000

    MAX_N_TERMS_MIN_VALUE = 1
    MAX_N_TERMS_MAX_VALUE = 1_000_000_000

    def __init__(self,
                 model_parameters_controller,
                 language_controller: LanguageController):
        """
        Constructor for BERT settings

        :param model_parameters_controller: ModelParametersController
        """
        super().__init__(model_parameters_controller, language_controller)

        self._min_df_input = QLineEdit()
        self._max_n_terms_input = QLineEdit()

    def initialize_parameter_widgets(self,
                                     scroll_layout: QVBoxLayout) -> None:
        """
        Initialize the parameter widgets

        :return: None
        """
        super().initialize_parameter_widgets(scroll_layout)

        self.add_header_label("Hyperparameters", 17)
        self.initialize_min_term_freq_field()
        # self.initialize_max_n_terms_field() todo
        self.add_margin(10)

    def all_fields_valid(self) -> bool:
        """
        Validate all fields

        :return: bool
        """
        return super().all_fields_valid() and self.validate_min_df_field()

    def initialize_min_term_freq_field(self) -> None:
        """
        Initialize the minimal term frequency field

        :return: None
        """
        min_term_freq_layout = QHBoxLayout()

        # Add label
        min_df = QLabel("Min. Term Freq.:")
        min_df.setStyleSheet(f"font-size: 16px;"
                             f"color: black;"
                             f"font-family: {text_font};")
        min_df.setAlignment(Qt.AlignmentFlag.AlignLeft |
                            Qt.AlignmentFlag.AlignVCenter)
        min_term_freq_layout.addWidget(min_df)

        # Define layout for whether min_term_freq is valid or invalid
        self.min_df_layout_valid = (f"border-radius: 5px;"
                                    f"font-size: 14px;"
                                    f"font-family: {text_font};"
                                    f"color: black;"
                                    f"border: 2px solid {seco_col_blue};"
                                    f"padding: 5px;"
                                    f"background-color: white;")
        self.min_df_layout_invalid = (f"border-radius: 5px;"
                                      f"font-size: 14px;"
                                      f"font-family: {text_font};"
                                      f"color: black;"
                                      f"border: 2px solid red;"
                                      f"padding: 5px;"
                                      f"background-color: white;")

        # Add input field
        self._min_df_input = QLineEdit()
        self._min_df_input.setFixedWidth(100)
        self._min_df_input.setStyleSheet(self.min_df_layout_valid)
        # QIntValidator prevents user from typing
        # anything that isn't an integer
        self._min_df_input.setValidator(QIntValidator(self.MIN_DF_MIN_VALUE,
                                                      self.MIN_DF_MAX_VALUE))
        self._min_df_input.setPlaceholderText("Voer evt. minimale "
                                              "woord-frequentie in")
        self._min_df_input.setStyleSheet(self.min_df_layout_valid)
        self._min_df_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        min_term_freq_layout.addWidget(self._min_df_input)
        self._min_df_input.editingFinished.connect(
            self.min_df_editing_finished_event)

        # Add topic amount layout to container layout
        self._scroll_layout.addLayout(min_term_freq_layout)

    def min_df_editing_finished_event(self) -> None:
        new_min_df_value = (None if self._min_df_input.text() == ""
                            else int(self._min_df_input.text()))
        self._model_parameters_controller.set_bert_min_df(new_min_df_value)

    def validate_min_df_field(self) -> bool:
        """
        Validate the minimal term frequency (min_df) field

        :return: bool
        """
        is_valid: bool

        # Check if beta is a valid float
        try:
            min_df = int(self._min_df_input.text())
            is_valid = self.MIN_DF_MIN_VALUE <= min_df <= self.MIN_DF_MAX_VALUE
        except ValueError:
            is_valid = False

        self._min_df_input.setStyleSheet(self.min_df_layout_valid
                                         if is_valid else
                                         self.min_df_layout_invalid)
        return is_valid


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
