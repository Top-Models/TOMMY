from unittest import mock

import pytest
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.view.model_params_view import ModelParamsView


@pytest.fixture
def model_params_view(qtbot: QtBot):
    controller = Controller()
    mpv = ModelParamsView(controller.model_parameters_controller,
                          controller, controller.config_controller)
    # qtbot.addWidget(mpv)
    return mpv


@pytest.mark.parametrize("test_input,expected",
                         [("0", False), ("abc", False), ("1", True),
                          ("2.5", False), ("7", True), ("999", True),
                          ("1000", False)])
def test_validate_input(model_params_view: ModelParamsView, test_input: str,
                        expected: bool):
    model_params_view.topic_input.setText(test_input)
    assert model_params_view.validate_input() == expected


@pytest.mark.parametrize("test_input,expected",
                         [("0", 0), ("abc", 0), ("1", 1),
                          ("2.5", 0), ("7", 7), ("999", 999),
                          ("1000", 0)])
def test_fetch_topic_num(model_params_view: ModelParamsView, test_input: str,
                         expected: int):
    model_params_view.topic_input.setText(test_input)
    assert model_params_view.fetch_topic_num() == expected


def test_apply_validates_input(model_params_view: ModelParamsView,
                               mocker: mock):
    # mock topic modelling to curb execution time
    mock_on_run_topic_modelling = mocker.Mock()
    model_params_view._controller.on_run_topic_modelling = (
        mock_on_run_topic_modelling)

    # test if validate_input is called by apply_button_clicked_event
    method_spy = mocker.spy(model_params_view, "validate_input")
    model_params_view.apply_button_clicked_event()
    method_spy.assert_called_once()


def test_editing_finished_validates_input(model_params_view: ModelParamsView,
                                          mocker: mock):
    # test if validate_input is called by topic_input_editing_finished_event
    method_spy = mocker.patch.object(model_params_view, "validate_input")
    model_params_view.topic_input_editing_finished_event()
    method_spy.assert_called_once()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
