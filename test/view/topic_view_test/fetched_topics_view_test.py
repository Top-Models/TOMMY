import pytest
from PySide6.QtCore import Qt
from pytest_mock import mocker
from pytestqt.qtbot import QtBot

from tommy.controller.graph_controller import GraphController
from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.model.topic_model import TopicModel
from tommy.support.constant_variables import sec_col_purple
from tommy.view.topic_view.fetched_topics_view import FetchedTopicsView
from tommy.view.topic_view.topic_entity_component.topic_entity import (
    TopicEntity)


@pytest.fixture(scope='function')
def fetched_topics_view(qtbot: QtBot) -> FetchedTopicsView:
    graph_controller = GraphController()
    model_parameters_controller = ModelParametersController()
    fetched_topics_view = FetchedTopicsView(graph_controller,
                                            model_parameters_controller)
    qtbot.addWidget(fetched_topics_view)
    return fetched_topics_view


def test_add_topic(fetched_topics_view: FetchedTopicsView):
    """
    Test adding a topic to the fetched topics view.
    """
    # Act
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"],
        0)

    # Assert
    assert (fetched_topics_view.topic_container ==
            {"lda_model": [("test_topic", ["word1", "word2", "word3"])]})


def test_display_topics(fetched_topics_view: FetchedTopicsView):
    """
    Test displaying topics in the fetched topics view.
    """
    # Arrange
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"],
        0)

    # Act
    fetched_topics_view._display_topics("lda_model")

    # Assert
    assert (fetched_topics_view.layout.count() == 1)


def test_remove_tab_from_container(fetched_topics_view: FetchedTopicsView):
    """
    Test removing a tab from the topic container.
    """
    # Arrange
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"],
        0)

    # Act
    fetched_topics_view.remove_tab_from_container("lda_model")

    # Assert
    assert (fetched_topics_view.topic_container == {})


def test_clear_topics(fetched_topics_view: FetchedTopicsView, qtbot: QtBot):
    """
    Test clearing the topics from the fetched topics view.
    """
    # Arrange
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"],
        0)

    # Act
    fetched_topics_view._display_topics("lda_model")
    fetched_topics_view._clear_topics()
    qtbot.wait(100)

    # Assert
    assert (fetched_topics_view.topic_container == {})
    assert (fetched_topics_view.layout.count() == 0)


def test_on_topic_clicked(fetched_topics_view: FetchedTopicsView):
    """
    Test the topic clicked event of the fetched topics view.
    """
    # Add a topic and display it
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"],
        0)
    fetched_topics_view._display_topics("lda_model")

    # Find the TopicEntity widget
    topic_entity = None
    for i in range(fetched_topics_view.layout.count()):
        widget = fetched_topics_view.layout.itemAt(i).widget()
        if isinstance(widget, TopicEntity):
            topic_entity = widget
            break

    # Ensure we found the TopicEntity widget
    assert topic_entity is not None

    # Simulate topic click
    fetched_topics_view._on_topic_clicked(topic_entity)

    # Ensure the topic is selected
    assert fetched_topics_view.selected_topic == topic_entity

    # Simulate topic click again
    fetched_topics_view._on_topic_clicked(topic_entity)

    # Ensure the topic is deselected
    assert fetched_topics_view.selected_topic is None


def test_deselect_all_topics(fetched_topics_view: FetchedTopicsView):
    """
    Test deselecting all topics in the fetched topics view.
    """
    # Add a topic and display it
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"],
        0)
    fetched_topics_view._display_topics("lda_model")

    # Find the TopicEntity widget
    topic_entity = None
    for i in range(fetched_topics_view.layout.count()):
        widget = fetched_topics_view.layout.itemAt(i).widget()
        if isinstance(widget, TopicEntity):
            topic_entity = widget
            break

    # Ensure we found the TopicEntity widget
    assert topic_entity is not None

    # Select the topic
    topic_entity.select()

    # Deselect all topics
    fetched_topics_view.deselect_all_topics()

    # Ensure the topic is deselected
    assert not topic_entity.selected
    assert topic_entity.styleSheet() == (
        f"background-color: {sec_col_purple}; "
        f"color: white;")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
