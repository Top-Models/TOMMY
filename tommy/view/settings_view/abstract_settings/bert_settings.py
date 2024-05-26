import locale

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QVBoxLayout)

from tommy.controller.language_controller import LanguageController
from tommy.support.constant_variables import text_font, seco_col_blue
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings


class BertSettings(AbstractSettings):
    """
    Class for BERT settings
    """
    MIN_DF_MIN_VALUE = 0.0
    MIN_DF_MAX_VALUE = 0.96

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
        self._max_features_input = QLineEdit()

        # Define layout for whether min_term_freq is valid or invalid
        self.layout_valid = (f"border-radius: 5px;"
                             f"font-size: 14px;"
                             f"font-family: {text_font};"
                             f"color: black;"
                             f"border: 2px solid {seco_col_blue};"
                             f"padding: 5px;"
                             f"background-color: white;")
        self.layout_invalid = (f"border-radius: 5px;"
                               f"font-size: 14px;"
                               f"font-family: {text_font};"
                               f"color: black;"
                               f"border: 2px solid red;"
                               f"padding: 5px;"
                               f"background-color: white;")

    def initialize_parameter_widgets(self,
                                     scroll_layout: QVBoxLayout) -> None:
        """
        Initialize the parameter widgets

        :return: None
        """
        super().initialize_parameter_widgets(scroll_layout)

        self.add_header_label("Hyperparameters", 17)
        self.initialize_min_term_freq_field()
        self.initialize_max_features_field()

        self.add_margin(10)

    def all_fields_valid(self) -> bool:
        """
        Validate all fields

        :return: bool
        """
        return (super().all_fields_valid() and
                self.validate_min_df_field() and
                self.validate_max_features_field())

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

        # Add input field
        self._min_df_input = QLineEdit()
        self._min_df_input.setFixedWidth(100)
        self._min_df_input.setStyleSheet(self.layout_valid)

        self._min_df_input.setPlaceholderText(f"{self.MIN_DF_MIN_VALUE:.1f} .."
                                              f" {self.MIN_DF_MAX_VALUE:.2f}")
        self._min_df_input.setStyleSheet(self.layout_valid)
        self._min_df_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        min_term_freq_layout.addWidget(self._min_df_input)
        self._min_df_input.editingFinished.connect(
            self.min_df_editing_finished_event)

        # Add layout to container layout
        self._scroll_layout.addLayout(min_term_freq_layout)

    def min_df_editing_finished_event(self) -> None:
        """Save the value from the min_df field in the backend model"""
        new_min_df_value = (None if (self._min_df_input.text() == "" or
                                     not self.validate_min_df_field())
                            else locale.atof(self._min_df_input.text()))

        self._model_parameters_controller.set_bert_min_df(new_min_df_value)

    def validate_min_df_field(self) -> bool:
        """
        Validate the minimal term frequency (min_df) field

        :return: bool
        """
        is_valid: bool

        # Check if min_df is a valid float between the min and max
        try:
            min_df = locale.atof(self._min_df_input.text())
            is_valid = self.MIN_DF_MIN_VALUE <= min_df <= self.MIN_DF_MAX_VALUE
        except ValueError:
            is_valid = self._min_df_input.text() == ""

        self._min_df_input.setStyleSheet(self.layout_valid
                                         if is_valid else
                                         self.layout_invalid)
        return is_valid

    def initialize_max_features_field(self) -> None:
        """
        Initialize the maximum features field

        :return: None
        """
        max_features_layout = QHBoxLayout()

        # Add label
        max_features = QLabel("Max. #termen:")
        max_features.setStyleSheet(f"font-size: 16px;"
                                   f"color: black;"
                                   f"font-family: {text_font};")
        max_features.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                  Qt.AlignmentFlag.AlignVCenter)
        max_features_layout.addWidget(max_features)

        # Add input field
        self._max_features_input = QLineEdit()
        self._max_features_input.setFixedWidth(100)
        self._max_features_input.setStyleSheet(self.layout_valid)
        # QIntValidator prevents user from typing
        # anything that isn't an integer
        self._max_features_input.setValidator(
            QIntValidator(self.MAX_N_TERMS_MIN_VALUE,
                          self.MAX_N_TERMS_MAX_VALUE))
        self._max_features_input.setPlaceholderText("b.v.: 100_000")
        self._max_features_input.setStyleSheet(self.layout_valid)
        self._max_features_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        max_features_layout.addWidget(self._max_features_input)
        self._max_features_input.editingFinished.connect(
            self.max_features_editing_finished_event)

        # Add topic amount layout to container layout
        self._scroll_layout.addLayout(max_features_layout)

    def max_features_editing_finished_event(self) -> None:
        """Save the value from the max_features field in the backend model"""
        new_value = (None if (self._max_features_input.text() == "" or
                              not self.validate_max_features_field())
                     else int(self._max_features_input.text()))

        self._model_parameters_controller.set_bert_max_features(new_value)

    def validate_max_features_field(self) -> bool:
        """
        Validate the maximum number of features field

        :return: bool
        """
        is_valid: bool

        # Check if beta is a valid integer between the min and max
        try:
            max_features = int(self._max_features_input.text())
            is_valid = (self.MAX_N_TERMS_MIN_VALUE <= max_features
                        <= self.MAX_N_TERMS_MAX_VALUE)
        except ValueError:
            is_valid = self._max_features_input.text() == ""

        self._max_features_input.setStyleSheet(self.layout_valid
                                               if is_valid else
                                               self.layout_invalid)
        return is_valid

    def set_field_values_from_backend(self):
        """
        Get the parameter values from the backend and put them in the
        text boxes in the frontend. The dropdown for the model type has already
        been set in initialize_algorithm_field. If it was set here,
        it would trigger the algorithm_changed event and cause an infinite
        recursion.
        :return: None
        """
        super().set_field_values_from_backend()
        min_df = self._model_parameters_controller.get_bert_min_df()
        self._min_df_input.setText(locale.str(min_df)
                                   if min_df is not None
                                   else "")
        max_feat = self._model_parameters_controller.get_bert_max_features()
        self._max_features_input.setText(str(max_feat)
                                         if max_feat is not None
                                         else "")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
