import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tommy.controller.config_controller import ConfigController
from tommy.controller.corpus_controller import CorpusController
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.topic_modelling_controller import \
    TopicModellingController
from tommy.view.imported_files_view.imported_files_view import (
    ImportedFilesView)
from tommy.view.topic_view.topic_entity_component.topic_entity import \
    TopicEntity


@pytest.fixture(scope='function')
def imported_files_view(qtbot):
    imported_files_view = ImportedFilesView(
        CorpusController(),
        TopicModellingController(),
        ConfigController())
    qtbot.addWidget(imported_files_view)
    return imported_files_view


def test_imported_files_view_initialization(imported_files_view):
    assert isinstance(imported_files_view, ImportedFilesView)


def test_imported_files_layout(imported_files_view: ImportedFilesView):
    assert imported_files_view is not None
    assert imported_files_view.title_widget is not None
    assert imported_files_view.scroll_area is not None
    assert imported_files_view.scroll_widget is not None
    assert imported_files_view.scroll_layout is not None
    assert imported_files_view.layout is not None
    assert imported_files_view.metadata is not None
    assert imported_files_view.document_topics is not None


# Test if the header button press collapses the imported files view
def test_header_button_press(imported_files_view: ImportedFilesView,
                             qtbot: QtBot):
    # Check if imported files view is visible and the button style is correct
    assert imported_files_view.scroll_area.isHidden() is False
    assert imported_files_view.title_widget.title_button.text() == "▽"

    # Click the collapse button
    qtbot.mouseClick(imported_files_view.title_widget.title_button,
                     Qt.LeftButton)

    # Check if imported files view is hidden and the button style changed
    assert imported_files_view.scroll_area.isVisible() is False
    assert imported_files_view.title_widget.title_button.text() == "△"


# Test whether the list is sorted if on_document_topics_calculated and
# on_topic_selected are called
def test_sorting(imported_files_view: ImportedFilesView, qtbot: QtBot):
    imported_files_view.on_document_topics_calculated(
        [(Metadata("file1", 0, 0, "txt"), [0.0, 0.5, 0.9]),
         (Metadata("file2", 0, 0, "txt"), [0.3, 0.1, 0.2]),
         (Metadata("file3", 0, 0, "txt"), [1.0, 0.3453, 0.0])
         ])

    # Select a topic
    imported_files_view.on_topic_selected(TopicEntity("topic1", [], 0))
    qtbot.wait(100)  # Wait for deletelater to be processed
    assert imported_files_view.scroll_layout.count() == 3

    # Check if the files are in the correct order
    assert (imported_files_view.scroll_layout.itemAt(0).widget()
            .file.name == "file3")
    assert (imported_files_view.scroll_layout.itemAt(1).widget()
            .file.name == "file2")
    assert (imported_files_view.scroll_layout.itemAt(2).widget()
            .file.name == "file1")

    # Select a topic
    imported_files_view.on_topic_selected(TopicEntity("topic2", [], 1))
    qtbot.wait(100)  # Wait for deletelater to be processed
    assert imported_files_view.scroll_layout.count() == 3

    # Check if the files are in the correct order
    assert (imported_files_view.scroll_layout.itemAt(0).widget()
            .file.name == "file1")
    assert (imported_files_view.scroll_layout.itemAt(1).widget()
            .file.name == "file3")
    assert (imported_files_view.scroll_layout.itemAt(2).widget()
            .file.name == "file2")

    # Select a topic
    imported_files_view.on_topic_selected(TopicEntity("topic3", [], 2))
    qtbot.wait(100)  # Wait for deletelater to be processed
    assert imported_files_view.scroll_layout.count() == 3

    # Check if the files are in the correct order
    assert (imported_files_view.scroll_layout.itemAt(0).widget()
            .file.name == "file1")
    assert (imported_files_view.scroll_layout.itemAt(1).widget()
            .file.name == "file2")
    assert (imported_files_view.scroll_layout.itemAt(2).widget()
            .file.name == "file3")


if __name__ == '__main__':
    pytest.main()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""