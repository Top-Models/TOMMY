import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.view.settings_view.abstract_settings.lda_settings import LdaSettings


@pytest.fixture(scope='function')
def lda_settings() -> LdaSettings:
    controller = Controller()
    lda_settings = LdaSettings(controller.model_parameters_controller,
                               controller.config_controller,
                               controller.language_controller)
    return lda_settings



def test_alpha_input_editing_finished_event_enabled(lda_settings: LdaSettings,
                                                    qtbot: QtBot,
                                                    mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)
    lda_settings._auto_calc_alpha_beta_checkbox.setChecked(False)
    lda_settings._alpha_value_input.setText("")

    # Act
    qtbot.keyClicks(lda_settings._alpha_value_input, "0.1")

    # Assert
    assert lda_settings._alpha_value_input.text() == "0.1"


def test_alpha_input_editing_finished_event_disabled(lda_settings: LdaSettings,
                                                     qtbot: QtBot,
                                                     mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)
    lda_settings._auto_calc_alpha_beta_checkbox.setChecked(True)

    # Act
    qtbot.keyClicks(lda_settings._alpha_value_input, "0.1")

    # Assert
    assert lda_settings._alpha_value_input.text() == "-:-"


@pytest.mark.parametrize("text, expected",
                         [("-1", False), ("0", False), ("abc", False),
                          ("1", True), ("2.5", True), ("7", True),
                          ("999", True), ("1000", True), ("0.5", True),
                          ("0.001", True), ("0,5", False), ("0,005", False)])
def test_validate_alpha_field_not_auto(lda_settings: LdaSettings,
                                       text: str,
                                       expected: bool,
                                       mocker,
                                       qtbot: QtBot):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)
    qtbot.mouseClick(lda_settings._auto_calc_alpha_beta_checkbox,
                     Qt.LeftButton)
    lda_settings._alpha_value_input.setText(text)

    # Act
    result = lda_settings.validate_alpha_field()

    # Assert
    assert result == expected


def test_validate_alpha_field_auto(lda_settings: LdaSettings,
                                   mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)
    lda_settings._auto_calc_alpha_beta_checkbox.setChecked(True)

    # Act
    result = lda_settings.validate_alpha_field()

    # Assert
    assert result


def test_beta_input_editing_finished_event_enabled(lda_settings: LdaSettings,
                                                   qtbot: QtBot,
                                                   mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)
    lda_settings._auto_calc_alpha_beta_checkbox.setChecked(False)
    lda_settings._beta_value_input.setText("")

    # Act
    qtbot.keyClicks(lda_settings._beta_value_input, "0.1")

    # Assert
    assert lda_settings._beta_value_input.text() == "0.1"


def test_beta_input_editing_finished_event_disabled(lda_settings: LdaSettings,
                                                    qtbot: QtBot,
                                                    mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)
    lda_settings._auto_calc_alpha_beta_checkbox.setChecked(True)

    # Act
    qtbot.keyClicks(lda_settings._beta_value_input, "0.1")

    # Assert
    assert lda_settings._beta_value_input.text() == "-:-"


@pytest.mark.parametrize("text, expected",
                         [("-1", False), ("0", False), ("abc", False),
                          ("1", True), ("2.5", True), ("7", True),
                          ("999", True), ("1000", True), ("0.5", True),
                          ("0.001", True), ("0,5", False), ("0,005", False)])
def test_validate_beta_field_not_auto(lda_settings: LdaSettings,
                                      text: str,
                                      expected: bool,
                                      mocker,
                                      qtbot: QtBot):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)
    qtbot.mouseClick(lda_settings._auto_calc_alpha_beta_checkbox,
                     Qt.LeftButton)
    lda_settings._beta_value_input.setText(text)

    # Act
    result = lda_settings.validate_beta_field()

    # Assert
    assert result == expected


def test_validate_beta_field_auto(lda_settings: LdaSettings,
                                  mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)
    lda_settings._auto_calc_alpha_beta_checkbox.setChecked(True)

    # Act
    result = lda_settings.validate_beta_field()

    # Assert
    assert result


def test_toggle_auto_calculate_alpha_beta(lda_settings: LdaSettings,
                                          qtbot: QtBot,
                                          mocker):
    # Arrange
    scroll_layout = mocker.MagicMock()
    lda_settings.initialize_parameter_widgets(scroll_layout)

    # Assert
    assert lda_settings._alpha_value_input.text() == "-:-"
    assert lda_settings._beta_value_input.text() == "-:-"
    assert lda_settings._alpha_value_input.isReadOnly()
    assert lda_settings._beta_value_input.isReadOnly()

    # Act
    qtbot.mouseClick(lda_settings._auto_calc_alpha_beta_checkbox,
                     Qt.LeftButton)

    # Assert
    assert lda_settings._alpha_value_input.text() == "1.0"
    assert lda_settings._beta_value_input.text() == "0.01"
    assert not lda_settings._alpha_value_input.isReadOnly()
    assert not lda_settings._beta_value_input.isReadOnly()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
