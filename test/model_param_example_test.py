import pytest
from PySide6.QtCore import Qt
from interactive_topic_modeling.display.model_params_display import ModelParamsDisplay


@pytest.fixture
def parameter_display(qtbot):
    # Create and return your parameter_display object here
    parameter_display = ModelParamsDisplay()
    # Attach the widget to the bot that will simulate the user
    qtbot.addWidget(parameter_display)
    return parameter_display


def test_model_params_display_user_interaction(parameter_display, qtbot):
    # Set some kind of input
    parameter_display.topic_input.setText("10")
    # Have the user simulate the action of validating the input
    qtbot.keyPress(parameter_display.topic_input, Qt.Key_Return)
    # See if the result is the same as expected
    assert parameter_display.fetch_topic_num() == 10


if __name__ == '__main__':
    pytest.main()
