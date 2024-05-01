import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tommy.view.model_params_view import ModelParamsView
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from pytest_mock import mocker
from tommy.controller.controller import Controller


@pytest.fixture(scope='function')
def model_params_view(qtbot: QtBot) -> ModelParamsView:
    controller = Controller()
    model_params_view = ModelParamsView(controller.model_parameters_controller,
                                        controller,
                                        controller.config_controller)
    qtbot.addWidget(model_params_view)
    return model_params_view


def test_fetch_topic_num_default(model_params_view: ModelParamsView):
    assert model_params_view.fetch_topic_num() == 3


def test_fetch_topic_num_changed(model_params_view: ModelParamsView,
                                 qtbot: QtBot):
    # Arrange
    initial_value = model_params_view.fetch_topic_num()

    # Act
    new_value = 5
    qtbot.keyClicks(model_params_view.topic_input, str(new_value))

    # Assert
    assert (model_params_view.fetch_topic_num() ==
            int(str(initial_value) + str(new_value)))


def test_topic_input_return_pressed(model_params_view: ModelParamsView,
                                    qtbot: QtBot):
    # Arrange
    initial_value = model_params_view.fetch_topic_num()

    # Act
    new_value = 5
    qtbot.keyClicks(model_params_view.topic_input, str(new_value))
    model_params_view.topic_input.returnPressed.emit()

    # Assert
    assert (model_params_view.fetch_topic_num() ==
            int(str(initial_value) + str(new_value)))


def test_apply_button_clicked_changed_topic_num(
        model_params_view: ModelParamsView,
        qtbot: QtBot,
        mocker: mocker):
    # Arrange
    initial_value = model_params_view.fetch_topic_num()

    # mock topic modelling to curb execution time
    mock_on_run_topic_modelling = mocker.Mock()
    model_params_view._controller.on_run_topic_modelling = (
        mock_on_run_topic_modelling)

    # Act
    new_value = 5
    qtbot.keyClicks(model_params_view.topic_input, str(new_value))
    model_params_view.apply_button.clicked.emit()

    # Assert
    assert (model_params_view.fetch_topic_num() ==
            int(str(initial_value) + str(new_value)))


def test_apply_button_clicked_calls_on_run_topic_modelling(
        model_params_view: ModelParamsView,
        qtbot: QtBot,
        mocker: mocker):
    # Arrange
    mock_on_run_topic_modelling = mocker.Mock()
    model_params_view._controller.on_run_topic_modelling = (
        mock_on_run_topic_modelling)

    # Act
    qtbot.mouseClick(model_params_view.apply_button, Qt.LeftButton)

    # Assert
    assert mock_on_run_topic_modelling.call_count == 1


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
