import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.support.model_type import ModelType
from tommy.support.supported_languages import SupportedLanguage
from tommy.view.settings_view.abstract_settings.abstract_settings import \
    AbstractSettings
from test.helper_fixtures import controller_no_pipeline


@pytest.fixture
def controller(controller_no_pipeline):
    return controller_no_pipeline


@pytest.fixture(scope='function')
def abstract_settings(controller) -> AbstractSettings:
    abstract_settings = AbstractSettings(
        controller.model_parameters_controller,
        controller.config_controller,
        controller.language_controller)
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


@pytest.mark.parametrize("text, expected",
                         [("0", False), ("abc", False), ("1", True),
                          ("2.5", False), ("7", True), ("999", True),
                          ("1000", False)])
def test_validate_topic_amount_field(abstract_settings: AbstractSettings,
                                     text: str, expected: bool,
                                     mocker):
    # Mock scroll_layout
    scroll_layout = mocker.MagicMock()
    abstract_settings.initialize_parameter_widgets(scroll_layout)

    # Mock get_model_n_topics from ModelParametersController
    mocker.patch.object(abstract_settings._model_parameters_controller,
                        "get_model_n_topics", return_value=text)

    # Act
    abstract_settings._topic_amount_field.setText(text)
    result = abstract_settings.validate_topic_amount_field()

    # Assert
    assert result == expected


def test_get_topic_amount(abstract_settings: AbstractSettings, mocker):
    # Mock scroll_layout
    scroll_layout = mocker.MagicMock()
    abstract_settings.initialize_parameter_widgets(scroll_layout)

    # Act
    abstract_settings._topic_amount_field.setText("7")
    result = abstract_settings.get_topic_amount()

    # Assert
    assert result == 7


def test_get_topic_amount_empty(abstract_settings: AbstractSettings, mocker):
    # Mock scroll_layout
    scroll_layout = mocker.MagicMock()
    abstract_settings.initialize_parameter_widgets(scroll_layout)

    # Act
    abstract_settings._topic_amount_field.setText("")
    result = abstract_settings.get_topic_amount()

    # Assert
    assert result == 0


def test_get_topic_amount_invalid(abstract_settings: AbstractSettings, mocker):
    # Mock scroll_layout
    scroll_layout = mocker.MagicMock()
    abstract_settings.initialize_parameter_widgets(scroll_layout)

    # Act
    abstract_settings._topic_amount_field.setText("abc")
    result = abstract_settings.get_topic_amount()

    # Assert
    assert result == 0


@pytest.mark.parametrize("text, expected",
                         [("0", False), ("abc", False), ("1", True),
                          ("2.5", False), ("7", True), ("999", True),
                          ("1000", False)])
def test_validate_amount_of_words_field(abstract_settings: AbstractSettings,
                                        text: str, expected: bool,
                                        mocker):
    # Mock scroll_layout
    scroll_layout = mocker.MagicMock()
    abstract_settings.initialize_parameter_widgets(scroll_layout)

    # Act
    abstract_settings._amount_of_words_field.setText(text)
    result = abstract_settings.validate_amount_of_words_field()

    # Assert
    assert result == expected


@pytest.mark.parametrize("text, expected",
                         [("0", 0), ("abc", 0), ("1", 1),
                          ("2.5", 0), ("7", 7), ("999", 999),
                          ("1000", 0)])
def test_get_amount_of_words(abstract_settings: AbstractSettings,
                             text: str, expected: int, mocker):
    # Mock scroll_layout
    scroll_layout = mocker.MagicMock()
    abstract_settings.initialize_parameter_widgets(scroll_layout)

    # Act
    abstract_settings._amount_of_words_field.setText(text)
    result = abstract_settings.get_amount_of_words()

    # Assert
    assert result == expected


def test_initialize_algorithm_field(abstract_settings: AbstractSettings,
                                    mocker):
    # Mock the ModelParametersController
    model_parameters_controller = mocker.MagicMock()
    abstract_settings._model_parameters_controller = (
        model_parameters_controller)

    # Mock the selection field
    algorithm_field = mocker.MagicMock()
    abstract_settings._algorithm_field = algorithm_field

    # Mock the scroll layout
    scroll_layout = mocker.MagicMock()
    abstract_settings._scroll_layout = scroll_layout

    # Set the return value of get_model_type
    model_parameters_controller.get_model_type.return_value = ModelType.LDA

    # Act
    abstract_settings.initialize_algorithm_field()

    # Check if the algorithm field is added to the scroll layout
    scroll_layout.addLayout.assert_called()


def test_algorithm_field_changed_event(abstract_settings: AbstractSettings,
                                       mocker):
    # Mock the ModelParametersController
    model_parameters_controller = mocker.MagicMock()
    abstract_settings._model_parameters_controller = (
        model_parameters_controller)

    # Mock the selction field
    algorithm_field = mocker.MagicMock()
    abstract_settings._algorithm_field = algorithm_field

    # Change the model to nmf
    algorithm_field.currentText.return_value = "NMF"
    abstract_settings.algorithm_field_changed_event()

    # Assert
    model_parameters_controller.set_model_type.assert_called_with(
        ModelType.NMF)


def test_initialize_language_field(abstract_settings: AbstractSettings,
                                   mocker):
    # Mock the languageController
    language_controller = mocker.MagicMock()
    abstract_settings._language_controller = language_controller

    # Mock the scroll layout
    scroll_layout = mocker.MagicMock()
    abstract_settings._scroll_layout = scroll_layout

    # Set the return value of get_language
    language_controller.get_language.return_value = SupportedLanguage.Dutch

    # Act
    abstract_settings.initialize_language_field()

    # Check if the language field is added to the scroll layout
    scroll_layout.addLayout.assert_called()


def test_language_field_changed_event(abstract_settings: AbstractSettings,
                                      mocker):
    # Mock the LanguageController
    language_controller = mocker.MagicMock()
    abstract_settings._language_controller = (
        language_controller)

    # Mock the selection field
    language_field = mocker.MagicMock()
    abstract_settings._language_field = language_field

    # Change the model to nmf
    language_field.currentText.return_value = "Nederlands"
    abstract_settings.language_field_changed_event()

    # Assert
    language_controller.set_language.assert_called_with(
        SupportedLanguage.Dutch)


def test_disable_input_field(abstract_settings: AbstractSettings, mocker):
    # Mock the input field
    input_field = mocker.MagicMock()
    abstract_settings._topic_amount_field = input_field

    # Act
    abstract_settings.disable_input_field(input_field)

    # Assert
    input_field.setDisabled.assert_called_with(True)


def test_enable_input_field(abstract_settings: AbstractSettings, mocker):
    # Mock the input field
    input_field = mocker.MagicMock()
    abstract_settings._topic_amount_field = input_field

    # Act
    abstract_settings.enable_input_field(input_field)

    # Assert
    input_field.setDisabled.assert_called_with(False)


def test_disable_combobox(abstract_settings: AbstractSettings, mocker):
    # Mock the combobox
    combobox = mocker.MagicMock()
    abstract_settings._algorithm_field = combobox

    # Act
    abstract_settings.disable_combobox(combobox)

    # Assert
    combobox.setDisabled.assert_called_with(True)


def test_enable_combobox(abstract_settings: AbstractSettings, mocker):
    # Mock the combobox
    combobox = mocker.MagicMock()
    abstract_settings._algorithm_field = combobox

    # Act
    abstract_settings.enable_combobox(combobox)

    # Assert
    combobox.setDisabled.assert_called_with(False)


def test_enable_button(abstract_settings: AbstractSettings, mocker):
    # Mock the button
    button = mocker.MagicMock()
    abstract_settings._apply_button = button

    # Act
    abstract_settings.enable_button(button)

    # Assert
    button.setDisabled.assert_called_with(False)


def test_disable_button(abstract_settings: AbstractSettings, mocker):
    # Mock the button
    button = mocker.MagicMock()
    abstract_settings._apply_button = button

    # Act
    abstract_settings.disable_button(button)

    # Assert
    button.setDisabled.assert_called_with(True)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
