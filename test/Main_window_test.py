import pytest
from PySide6 import QtCore
from PySide6.QtCore import Qt
from interactive_topic_modeling.main_window import MainWindow
from interactive_topic_modeling.support.constant_variables import text_font, heading_font, seco_col_blue, \
    hover_seco_col_blue

@pytest.fixture
def mainwindow(qtbot):
    # Create and return your parameter_display object here
    mainwindow = MainWindow()
    # Attach the widget to the bot that will simulate the user
    qtbot.addWidget(mainwindow)
    return mainwindow


def test_validate_input_incorrect(mainwindow, qtbot):
    # Simulate correct input (e.g., topic_input between 1 and 1000)
    mainwindow.model_params_display.topic_input.setText("0")
    qtbot.mouseClick(mainwindow.apply_button, QtCore.Qt.LeftButton)

    # Assert that the expected action was performed
    assert "Incorrect Input" in mainwindow.model_params_display.topic_input.placeholderText()

def test_validate_input_correct(mainwindow, qtbot):
    # Simulate correct input (e.g., topic_input between 1 and 1000)
    mainwindow.model_params_display.topic_input.setText("10")
    qtbot.mouseClick(mainwindow.apply_button, QtCore.Qt.LeftButton)

    # Assert that the expected action was performed
    assert "10" in mainwindow.model_params_display.topic_input.text()

def test_validate_input_reset_style(mainwindow, qtbot):
    # Simulate correct input (e.g., topic_input between 1 and 1000)
    mainwindow.model_params_display.topic_input.setText("0")
    qtbot.mouseClick(mainwindow.apply_button, QtCore.Qt.LeftButton)

    # Assert that the expected action was performed
    assert f"border-radius: 5px;font-size: 14px;font-family: {text_font};color: black;border: 4px solid red;padding: 5px;background-color: white;" in mainwindow.model_params_display.topic_input.styleSheet()

    mainwindow.model_params_display.topic_input.setText("10")
    qtbot.mouseClick(mainwindow.apply_button, QtCore.Qt.LeftButton)
    # Assert that style has reset
    assert f"border-radius: 5px;font-size: 14px;font-family: {text_font};color: black;border: 2px solid #00968F;padding: 5px;background-color: white;" in mainwindow.model_params_display.topic_input.styleSheet()



if __name__ == '__main__':
    pytest.main()
