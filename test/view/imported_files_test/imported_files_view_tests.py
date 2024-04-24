import pytest
import pytestqt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from tommy.view.imported_files_view.imported_files_view import (
    ImportedFilesView)


@pytest.fixture(scope='function')
def imported_files_view(qtbot):
    imported_files_view = ImportedFilesView()
    qtbot.addWidget(imported_files_view)
    return imported_files_view


def test_imported_files_view_initialization(imported_files_view):
    assert isinstance(imported_files_view, ImportedFilesView)


def test_imported_files_layout(imported_files_view: ImportedFilesView):
    assert imported_files_view is not None
    assert imported_files_view.file_reader is not None
    assert imported_files_view.title_widget is not None
    assert imported_files_view.scroll_area is not None
    assert imported_files_view.scroll_widget is not None
    assert imported_files_view.scroll_layout is not None
    assert imported_files_view.file_stats_view is not None
    assert imported_files_view.layout is not None
    assert imported_files_view.file_reader is not None


# Test if the header button press collapses the imported files view
def test_header_button_press(imported_files_view: ImportedFilesView,
                             qtbot: QtBot):
    # Check if imported files view is visible and the button style is correct
    assert imported_files_view.scroll_area.isHidden() is False
    assert imported_files_view.title_widget.title_button.text() == "🡻"

    # Click the collapse button
    qtbot.mouseClick(imported_files_view.title_widget.title_button,
                     Qt.LeftButton)

    # Check if imported files view is hidden and the button style changed
    assert imported_files_view.scroll_area.isVisible() is False
    assert imported_files_view.title_widget.title_button.text() == "🡹"


if __name__ == '__main__':
    pytest.main()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""