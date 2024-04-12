import pytest
from PySide6.QtCore import Qt
from pytest_mock import mocker
from pytestqt.qtbot import QtBot

from tommy.controller.graph_controller import GraphController
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.model.topic_model import TopicModel
from tommy.support.constant_variables import sec_col_purple
from tommy.view.topic_view.fetched_topics_view import FetchedTopicsView
from tommy.view.topic_view.topic_entity_component.topic_entity import (
    TopicEntity)


@pytest.fixture(scope='function')
def fetched_topics_view(qtbot: QtBot) -> FetchedTopicsView:
    graph_controller = GraphController()
    fetched_topics_view = FetchedTopicsView(graph_controller)
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
        ["word1", "word2", "word3"])

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
        ["word1", "word2", "word3"])

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
        ["word1", "word2", "word3"])

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
        ["word1", "word2", "word3"])

    # Act
    fetched_topics_view._display_topics("lda_model")
    fetched_topics_view._clear_topics()
    qtbot.wait(100)

    # Assert
    assert (fetched_topics_view.topic_container == {})
    assert (fetched_topics_view.layout.count() == 0)


def test_refresh_topics_lda(fetched_topics_view: FetchedTopicsView,
                             mocker: mocker):
    """
    Test refreshing the topics in the fetched topics view.
    """
    # Arrange
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"])

    # Mock TopicRunner in GraphController
    mock_topic_model = TopicModel()

    # Instantiate the model
    term_lists = [["word1", "word2", "word3"], ["word4", "word5", "word6"]]
    num_topics = 2
    model = LdaRunner(topic_model=mock_topic_model,
                      docs=term_lists,
                      num_topics=num_topics)
    fetched_topics_view._graph_controller._current_topic_runner = model
    mocker.patch.object(
        fetched_topics_view._graph_controller._current_topic_runner,
        "get_topics_with_scores",
        return_value=[])

    # Act
    fetched_topics_view._refresh_topics()

    # Assert
    assert fetched_topics_view.topic_container == {
        'lda_model': [('Topic 1',
                       ('word5',
                        'word4',
                        'word6',
                        'word1',
                        'word3',
                        'word2')),
                      ('Topic 2',
                       ('word2',
                        'word3',
                        'word1',
                        'word6',
                        'word4',
                        'word5'))]}
    assert fetched_topics_view.layout.count() == 2


def test_on_word_clicked(fetched_topics_view: FetchedTopicsView, qtbot: QtBot):
    """
    Test the word clicked event of the fetched topics view.
    """
    # Add a topic and display it
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"])
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

    # Spy on the emit method of wordClicked signal
    with qtbot.waitSignal(topic_entity.wordClicked) as word_clicked:
        # Simulate word click
        qtbot.mouseClick(topic_entity.word_entities[0], Qt.LeftButton)

    # Ensure the wordClicked signal was emitted
    assert word_clicked.args == ["word1"]


def test_on_topic_clicked(fetched_topics_view: FetchedTopicsView,
                          qtbot: QtBot):
    """
    Test the topic clicked event of the fetched topics view.
    """
    # Add a topic and display it
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"])
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

    # Spy on the emit method of clicked signal
    with qtbot.waitSignal(fetched_topics_view.topicClicked) as topic_clicked:
        # Simulate topic click
        qtbot.mouseClick(topic_entity, Qt.LeftButton)

    # Ensure the topicClicked signal was emitted
    assert topic_clicked


def test_deselect_all_topics(fetched_topics_view: FetchedTopicsView):
    """
    Test deselecting all topics in the fetched topics view.
    """
    # Add a topic and display it
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"])
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
