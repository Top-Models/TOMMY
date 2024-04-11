import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from pytestqt.qtbot import QtBot

from tommy.controller.graph_controller import GraphController
from tommy.datatypes.topics import Topic
from tommy.support.constant_variables import sec_col_orange
from tommy.view.topic_view.fetched_topics_view import FetchedTopicsView
from tommy.view.topic_view.topic_entity.topic_entity import TopicEntity


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


def test_refresh_topics(fetched_topics_view: FetchedTopicsView, qtbot: QtBot,
                        mocker: pytest.MockFixture):
    """
    Test refreshing the topics in the fetched topics view.
    """
    # Arrange
    fetched_topics_view._add_topic(
        "lda_model",
        "test_topic",
        ["word1", "word2", "word3"])
    fetched_topics_view._display_topics("lda_model")


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
