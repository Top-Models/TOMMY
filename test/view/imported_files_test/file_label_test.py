from datetime import datetime

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot
from tommy.support.constant_variables import medium_light_gray, \
    hover_medium_light_gray, pressed_medium_light_gray, text_font
from tommy.controller.file_import.metadata import Metadata
from tommy.view.imported_files_view.file_label import FileLabel


@pytest.fixture(scope='function')
def file_label(qtbot: QtBot) -> FileLabel:
    file_metadata = Metadata("test_file",
                             1288778,
                             69420,
                             "csv",
                             "Rembrandt van Maas",
                             "Nijntje is een konijn",
                             date=datetime(year=2024, month=4, day=9),
                             url="https://www.google.com",
                             path="data/test_file.csv"
                             )
    file_label = FileLabel(file_metadata)
    qtbot.addWidget(file_label)
    return file_label


def test_enter_event_selected(file_label: FileLabel):
    """
    Test the enter event of the file label when it is selected.
    """
    file_label.selected = True
    file_label.enterEvent(None)
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            f"font-size: 15px;"
            f"background-color: {medium_light_gray};"
            f"color: black;"
            f"margin: 0px;"
            f"padding: 10px;")


def test_enter_event_not_selected(file_label: FileLabel):
    """
    Test the enter event of the file label when it is not selected.
    """
    file_label.selected = False
    file_label.enterEvent(None)
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            f"font-size: 15px;"
            f"background-color: "
            f"{hover_medium_light_gray};"
            f"color: black;"
            f"margin: 0px;"
            f"padding: 10px;")


def test_leave_event_selected(file_label: FileLabel):
    """
    Test the leave event of the file label when it is selected.
    """
    file_label.selected = True
    file_label.leaveEvent(None)
    assert (file_label.styleSheet() ==
            "font-family: Corbel;"
            "font-size: 15px;"
            f"background-color: {medium_light_gray};"
            "color: black;"
            "margin: 0px;"
            "padding: 10px;")


def test_leave_event_not_selected(file_label: FileLabel):
    """
    Test the leave event of the file label when it is not selected.
    """
    file_label.selected = False
    file_label.leaveEvent(None)
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            f"font-size: 15px;"
            f"background-color: {medium_light_gray};"
            f"color: black;"
            f"margin: 0px;"
            f"padding: 10px;")


def test_mouse_press_event_selected(file_label: FileLabel, qtbot: QtBot):
    """
    Test the mouse press event of the file label when it is selected.
    """
    file_label.selected = True
    qtbot.mousePress(file_label, Qt.LeftButton)
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            "font-size: 15px;"
            f"background-color: {medium_light_gray};"
            "color: black;"
            "margin: 0px;"
            "padding: 10px;")

    assert file_label.selected is False


def test_mouse_press_event_not_selected(file_label: FileLabel, qtbot: QtBot):
    """
    Test the mouse press event of the file label when it is not selected.
    """
    file_label.selected = False
    qtbot.mousePress(file_label, Qt.LeftButton)
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            f"font-size: 15px;"
            f"background-color: "
            f"{pressed_medium_light_gray};"
            f"color: black;"
            f"margin: 0px;"
            f"padding: 10px;")


def test_deselect(file_label: FileLabel):
    """
    Test deselecting the file label.
    """
    file_label.deselect()
    assert file_label.selected is False
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            f"font-size: 15px;"
            f"background-color: {medium_light_gray};"
            f"color: black;"
            f"margin: 0px;"
            f"padding: 10px;")


def test_select(file_label: FileLabel):
    """
    Test selecting the file label.
    """
    file_label.select()
    assert file_label.selected is True
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            f"font-size: 15px;"
            f"background-color: "
            f"{pressed_medium_light_gray};"
            f"color: black;"
            f"margin: 0px;"
            f"padding: 10px;")


def test_mouse_release_event_selected(file_label: FileLabel, qtbot: QtBot):
    """
    Test the mouse release event of the file label when it is selected.
    """
    file_label.selected = True
    qtbot.mouseRelease(file_label, Qt.LeftButton)
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            "font-size: 15px;"
            f"background-color: {medium_light_gray};"
            "color: black;"
            "margin: 0px;"
            "padding: 10px;"
            )

    assert file_label.selected is True


def test_mouse_release_event_not_selected(file_label: FileLabel, qtbot: QtBot):
    """
    Test the mouse release event of the file label when it is not selected.
    """
    file_label.selected = False
    qtbot.mouseRelease(file_label, Qt.LeftButton)
    assert (file_label.styleSheet() ==
            f"font-family: {text_font};"
            f"font-size: 15px;"
            f"background-color: {hover_medium_light_gray};"
            f"color: black;"
            f"margin: 0px;"
            f"padding: 10px;")

    assert file_label.selected is False
