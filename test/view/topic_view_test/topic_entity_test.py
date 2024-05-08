import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tommy.support.constant_variables import (sec_col_purple,
                                              pressed_seco_col_purple)
from tommy.view.topic_view.topic_entity_component.topic_entity import (
    TopicEntity)


@pytest.fixture(scope='function')
def topic_entity(qtbot: QtBot) -> TopicEntity:
    topic_entity = TopicEntity("test_topic",
                               ["word1", "word2", "word3"],
                               0)
    qtbot.addWidget(topic_entity)
    return topic_entity


def test_get_topic_name_no_edit(topic_entity: TopicEntity):
    """
    Test getting the topic name.
    """
    assert topic_entity.get_topic_name() == "test_topic"


def test_get_topic_name_edit(topic_entity: TopicEntity,
                             qtbot: QtBot):
    """
    Test getting the topic name after editing.
    """
    # Arrange
    new_name = "new_name"
    topic_entity.topic_label.clear()
    qtbot.keyClicks(topic_entity.topic_label, new_name)

    # Act
    topic_name = topic_entity.get_topic_name()

    # Assert
    assert topic_name == new_name


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


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
