import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot
from tommy.support.constant_variables import sec_col_purple, \
    pressed_seco_col_purple, hover_seco_col_purple
from tommy.view.topic_view.topic_entity_component.topic_entity import (
    TopicEntity)


@pytest.fixture(scope='function')
def topic_entity(qtbot: QtBot) -> TopicEntity:
    topic_entity = TopicEntity("test_topic",
                               ["word1", "word2", "word3"])
    qtbot.addWidget(topic_entity)
    return topic_entity


def test_enter_event_selected(topic_entity: TopicEntity):
    """
    Test the enter event of the topic entity when it is selected.
    """
    topic_entity.selected = True
    topic_entity.enterEvent(None)
    assert (topic_entity.styleSheet() ==
            f"background-color: {sec_col_purple}; color: white;")


def test_enter_event_not_selected(topic_entity: TopicEntity):
    """
    Test the enter event of the topic entity when it is not selected.
    """
    topic_entity.selected = False
    topic_entity.enterEvent(None)
    assert (topic_entity.styleSheet() ==
            f"background-color: {hover_seco_col_purple}; color: white;")


def test_leave_event_selected(topic_entity: TopicEntity):
    """
    Test the leave event of the topic entity when it is selected.
    """
    topic_entity.selected = True
    topic_entity.leaveEvent(None)
    assert (topic_entity.styleSheet() ==
            f"background-color: {sec_col_purple}; color: white;")


def test_leave_event_not_selected(topic_entity: TopicEntity):
    """
    Test the leave event of the topic entity when it is not selected.
    """
    topic_entity.selected = False
    topic_entity.leaveEvent(None)
    assert (topic_entity.styleSheet() ==
            f"background-color: {sec_col_purple}; color: white;")


def test_select(topic_entity: TopicEntity):
    """
    Test selecting the topic entity.
    """
    topic_entity.select()
    assert topic_entity.selected is True
    assert (topic_entity.styleSheet() ==
            f"background-color: {pressed_seco_col_purple}; color: white;")


def test_deselect(topic_entity: TopicEntity):
    """
    Test deselecting the topic entity.
    """
    topic_entity.deselect()
    assert topic_entity.selected is False
    assert (topic_entity.styleSheet() ==
            f"background-color: {sec_col_purple}; color: white;")


def test_mouse_press_event(topic_entity: TopicEntity,
                           qtbot: QtBot):
    """
    Test the mouse press event of the topic entity.
    """
    qtbot.mousePress(topic_entity, Qt.LeftButton)
    assert (topic_entity.styleSheet() ==
            f"background-color: {pressed_seco_col_purple};")


def test_mouse_release_signal_emission(topic_entity: TopicEntity,
                                       qtbot: QtBot):
    """
    Test the mouse release event of the topic entity.
    """
    clicked = None

    def on_clicked():
        nonlocal clicked
        clicked = topic_entity

    topic_entity.clicked.connect(on_clicked)
    qtbot.mouseRelease(topic_entity, Qt.LeftButton)
    assert clicked == topic_entity



