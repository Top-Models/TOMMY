from datetime import datetime

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.controller.file_import.metadata import Metadata
from tommy.view.imported_files_view.file_label import FileLabel
from tommy.view.selected_information_view import SelectedInformationView
from tommy.view.topic_view.topic_entity_component.topic_entity import \
    TopicEntity


@pytest.fixture(scope='function')
def selected_information_view(qtbot: QtBot) -> SelectedInformationView:
    controller = Controller()
    selected_information_view = SelectedInformationView(
        controller.graph_controller,
        controller.model_parameters_controller)
    qtbot.addWidget(selected_information_view)
    return selected_information_view


def test_display_no_component_selected(
        selected_information_view: SelectedInformationView):
    """
    Test displaying no component selected.
    """
    selected_information_view.display_no_component_selected()
    assert selected_information_view.scroll_layout.count() == 1
    assert (selected_information_view.scroll_layout.itemAt(0).
            widget().text() ==
            "Geen component\ngeselecteerd")


def test_clear_layout(selected_information_view: SelectedInformationView):
    """
    Test clearing the layout.
    """
    # Arrange
    selected_information_view.display_no_component_selected()

    # Act
    selected_information_view.clear_layout()

    # Assert
    assert selected_information_view.layout.count() == 2


def test_clear_sub_layout(selected_information_view: SelectedInformationView):
    """
    Test clearing the sub layout.
    """
    # Arrange
    selected_information_view.display_no_component_selected()

    # Act
    selected_information_view.clear_sub_layout(
        selected_information_view.layout)

    # Assert
    assert selected_information_view.layout.count() == 0


def test_display_file_info_file_selected(
        selected_information_view: SelectedInformationView):
    """
    Test displaying file information when a file is selected.
    """
    # Arrange
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
    file_label.selected = True

    # Act
    selected_information_view.display_file_info(file_label)

    # Assert
    assert selected_information_view.layout.count() == 2


def test_display_topic_info_topic_not_selected(
        selected_information_view: SelectedInformationView):
    """
    Test displaying topic information when no component is selected.
    """
    # Arrange
    topic_entity = TopicEntity("Test Topic",
                               ["word1", "word2", "word3"])
    topic_entity.selected = False

    # Act
    selected_information_view.display_topic_info(topic_entity)

    # Assert
    assert selected_information_view.scroll_layout.count() == 1
    assert (selected_information_view.scroll_layout.itemAt(0).
            widget().text() ==
            "Geen component\ngeselecteerd")


def test_display_topic_info_topic_selected(
        selected_information_view: SelectedInformationView):
    """
    Test displaying topic information when a topic is selected.
    """
    # Arrange
    topic_entity = TopicEntity("Test Topic",
                               ["word1", "word2", "word3"])
    topic_entity.selected = True

    # Act
    selected_information_view.display_topic_info(topic_entity)

    # Assert
    assert selected_information_view.layout.count() == 2


def test_display_run_info_valid_run_info(
        selected_information_view: SelectedInformationView):
    """
    Test displaying run information with valid run info.
    """
    # Arrange
    run_name = "Test Run"
    graph_controller = selected_information_view._graph_controller

    # Mock graph_controller get_number_of_topics to return 5
    graph_controller.get_number_of_topics = lambda: 5

    # Act
    selected_information_view.display_run_info(run_name)

    # Assert
    assert selected_information_view.layout.count() == 2


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
