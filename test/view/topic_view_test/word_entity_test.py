import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot
from tommy.support.constant_variables import text_font, \
    pressed_medium_light_gray
from tommy.view.topic_view.topic_entity_component.word_entity import WordEntity


@pytest.fixture(scope='function')
def word_entity(qtbot: QtBot) -> WordEntity:
    word_entity = WordEntity("test_word")
    qtbot.addWidget(word_entity)
    return word_entity


def test_enter_event_selected(word_entity: WordEntity):
    """
    Test the enter event of the word entity when it is selected.
    """
    word_entity.selected = True
    word_entity.enterEvent(None)
    assert word_entity.styleSheet() == f"font-family: {text_font}; " \
                                       f"font-size: 12px; " \
                                       f"background-color: white; " \
                                       f"padding: 10px; " \
                                       f"color: black"


def test_enter_event_not_selected(word_entity: WordEntity):
    """
    Test the enter event of the word entity when it is not selected.
    """
    word_entity.selected = False
    word_entity.enterEvent(None)
    assert word_entity.styleSheet() == f"font-family: {text_font}; " \
                                       f"font-size: 12px; " \
                                       f"background-color: lightgray; " \
                                       f"padding: 10px; " \
                                       f"color: black"


def test_leave_event_selected(word_entity: WordEntity):
    """
    Test the leave event of the word entity when it is selected.
    """
    word_entity.selected = True
    word_entity.leaveEvent(None)
    assert word_entity.styleSheet() == f"font-family: {text_font}; " \
                                       f"font-size: 12px; " \
                                       f"background-color: white; " \
                                       f"padding: 10px; " \
                                       f"color: black"


def test_leave_event_not_selected(word_entity: WordEntity):
    """
    Test the leave event of the word entity when it is not selected.
    """
    word_entity.selected = False
    word_entity.leaveEvent(None)
    assert word_entity.styleSheet() == f"font-family: {text_font}; " \
                                       f"font-size: 12px; " \
                                       f"background-color: white; " \
                                       f"padding: 10px; " \
                                       f"color: black"


def test_mouse_press_event(word_entity: WordEntity, qtbot: QtBot):
    """
    Test the mouse press event of the word entity.
    """
    qtbot.mousePress(word_entity, Qt.LeftButton)
    assert (word_entity.styleSheet() ==
            f"font-family: {text_font}; "
            f"font-size: 12px; "
            f"background-color: {pressed_medium_light_gray}; "
            f"padding: 10px; "
            f"color: black")


def test_mouse_release_event(word_entity: WordEntity, qtbot: QtBot):
    """
    Test the mouse release event of the word entity.
    """
    qtbot.mouseRelease(word_entity, Qt.LeftButton)
    assert word_entity.styleSheet() == f"font-family: {text_font}; " \
                                       f"font-size: 12px; " \
                                       f"background-color: white; " \
                                       f"padding: 10px; " \
                                       f"color: black"


def test_mouse_release_event_signal_emission(word_entity: WordEntity,
                                             qtbot: QtBot):
    """
    Test if the mouse release event emits the 'clicked' signal
    with the correct word.
    """
    clicked_word = None

    def on_clicked(word: str):
        nonlocal clicked_word
        clicked_word = word

    word_entity.clicked.connect(on_clicked)

    qtbot.mouseRelease(word_entity, Qt.LeftButton)
    assert clicked_word == "test_word"
