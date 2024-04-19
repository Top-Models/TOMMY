import pytest
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.view.model_params_view import ModelParamsView


@pytest.fixture
def model_params_view(qtbot: QtBot):
    controller = Controller()
    mpv = ModelParamsView(controller.model_parameters_controller, controller)
    qtbot.addWidget(mpv)
    return mpv


@pytest.mark.parametrize("test_input,expected",
                         [("0", False), ("abc", False), ("1", True),
                          ("2.5", False), ("7", True), ("999", True),
                          ("1000", False)])
def test_validate_input_return_value(model_params_view: ModelParamsView,
                                     qtbot: QtBot, test_input, expected):
    model_params_view.topic_input.setText(test_input)
    assert model_params_view.validate_input() is expected


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
