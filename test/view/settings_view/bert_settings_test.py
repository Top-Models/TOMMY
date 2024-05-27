import pytest
import locale

from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.model.model_parameters_model import ModelParametersModel
from tommy.view.settings_view.abstract_settings.bert_settings import (
    BertSettings)
from tommy.view.settings_view.abstract_settings.abstract_settings import (
    AbstractSettings)


@pytest.fixture(scope='function')
def bert_settings(mocker) -> BertSettings:
    mock_language_controller = mocker.MagicMock()

    model_parameters_model = ModelParametersModel()
    model_parameters_controller = ModelParametersController()
    model_parameters_controller.set_model_refs(model_parameters_model)

    bert_settings = BertSettings(model_parameters_controller,
                                 mock_language_controller)
    return bert_settings


@pytest.mark.parametrize("text, expected",
                         [(locale.str(-0.5), False),
                          (locale.str(1.5), False),
                          (locale.str(912), False),
                          (locale.str(0.1), True),
                          (locale.str(0.5), True),
                          ("abc", False),
                          ("0.1.2", False),
                          ("0,1,2", False),
                          ("", True)])
def test_validate_min_df(bert_settings: BertSettings,
                         text: str,
                         expected: bool,
                         mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    bert_settings.initialize_parameter_widgets(scroll_layout)
    bert_settings._min_df_input.setText(text)

    # Act
    result = bert_settings.validate_min_df_field()

    # Assert
    assert result == expected


@pytest.mark.parametrize("text, expected",
                         [(locale.str(-5), False),
                          (locale.str(1.5), False),
                          (locale.str(912), True),
                          (locale.str(0.5), False),
                          ("abc", False),
                          ("0,1,2.1.2", False),
                          ("", True)])
def test_validate_max_features(bert_settings: BertSettings,
                               text: str,
                               expected: bool,
                               mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    bert_settings.initialize_parameter_widgets(scroll_layout)
    bert_settings._max_features_input.setText(text)

    # Act
    result = bert_settings.validate_max_features_field()

    # Assert
    assert result == expected


@pytest.mark.parametrize("validate_super, validate_min_df, "
                         "validate_max_features",
                         [(True, True, True), (False, False, True),
                          (True, True, False), (False, False, False)])
def test_all_fields_valid(bert_settings: BertSettings,
                          validate_super: bool,
                          validate_min_df: bool,
                          validate_max_features: bool,
                          mocker):
    # Mock validate methods
    mocker.patch.object(AbstractSettings, "all_fields_valid",
                        return_value=validate_super)
    mocker.patch.object(bert_settings, "validate_min_df_field",
                        return_value=validate_min_df)
    mocker.patch.object(bert_settings, "validate_max_features_field",
                        return_value=validate_max_features)

    # Act
    result = bert_settings.all_fields_valid()

    # Assert
    assert result == all([validate_super, validate_min_df,
                          validate_max_features])


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
