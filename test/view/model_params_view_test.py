import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from pytest_mock import mocker, MockerFixture
from tommy.support.model_type import ModelType
from tommy.view.settings_view.model_params_view import ModelParamsView
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


def test_get_current_settings_view_returns_correct_settings_view(
        model_params_view: ModelParamsView):
    # Arrange
    model_params_view._model_parameters_controller.set_model_type(
        ModelType.LDA)

    # Act
    settings_view = model_params_view.get_current_settings_view()

    # Assert
    assert (settings_view ==
            model_params_view.algorithm_specific_settings_views[ModelType.LDA])


def test_apply_button_clicked_not_all_fields_valid_does(
        model_params_view: ModelParamsView,
        qtbot: QtBot,
        mocker: MockerFixture):
    # Arrange
    mock_all_fields_valid = mocker.patch.object(
        model_params_view.get_current_settings_view(), "all_fields_valid")
    mock_all_fields_valid.return_value = False

    # Act
    qtbot.mouseClick(model_params_view.apply_button, Qt.LeftButton)

    # Assert
    assert mock_all_fields_valid.call_count == 1


def test_apply_button_clicked_calls_on_run_topic_modelling(
        model_params_view: ModelParamsView,
        qtbot: QtBot,
        mocker: MockerFixture):
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
