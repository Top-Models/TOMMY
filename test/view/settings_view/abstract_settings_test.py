import pytest
from PySide6.QtWidgets import QLineEdit
from pytestqt.qtbot import QtBot

from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings


@pytest.fixture(scope='function')
def abstract_settings() -> AbstractSettings:
    model_parameters_controller = ModelParametersController()
    abstract_settings = AbstractSettings(model_parameters_controller)
    return abstract_settings


@pytest.mark.parametrize("validate_topic_input, validate_word_input",
                         [(True, True), (False, True), (True, False),
                          (False, False)])
def test_all_fields_valid(abstract_settings: AbstractSettings,
                          validate_topic_input: bool,
                          validate_word_input: bool,
                          mocker):
    # Mock validate methods
    mocker.patch.object(abstract_settings, "validate_topic_amount_field",
                        return_value=validate_topic_input)
    mocker.patch.object(abstract_settings, "validate_amount_of_words_field",
                        return_value=validate_word_input)

    # Act
    result = abstract_settings.all_fields_valid()

    # Assert
    assert result == (validate_topic_input and
                      validate_word_input)


# TODO: Implement tests for the other methods in AbstractSettings


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
