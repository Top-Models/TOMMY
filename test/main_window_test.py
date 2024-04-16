import pytest

from tommy.controller.file_import.metadata import Metadata
from tommy.main_window import MainWindow
from tommy.view.imported_files_view.file_label import FileLabel


@pytest.fixture(scope='function')
def main_window(qtbot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    return main_window


def test_on_file_clicked_selected_file(main_window, mocker):
    # Arrange
    metadata = Metadata(name='test', size=1, length=1, format='test')
    file_label = FileLabel(metadata)
    file_label.selected = True
    mocked_fetched_topics_view = mocker.patch.object(
        main_window.fetched_topics_view, 'deselect_all_topics')
    mocked_selected_information_view = mocker.patch.object(
        main_window.selected_information_view, 'display_file_info')

    # Act
    main_window.on_file_clicked(file_label)

    # Assert
    mocked_fetched_topics_view.assert_called_once_with()
    mocked_selected_information_view.assert_called_once_with(file_label)


def test_on_file_clicked_file_not_selected(main_window, mocker):
    # Arrange
    metadata = Metadata(name='test', size=1, length=1, format='test')
    file_label = FileLabel(metadata)
    file_label.selected = False
    mocked_fetched_topics_view = mocker.patch.object(
        main_window.fetched_topics_view, 'deselect_all_topics')
    mocked_selected_information_view = mocker.patch.object(
        main_window.selected_information_view, 'display_run_info')

    # Act
    main_window.on_file_clicked(file_label)

    # Assert
    mocked_fetched_topics_view.assert_called_once_with()
    mocked_selected_information_view.assert_called_once_with("lda_model")


def test_on_topic_clicked(main_window, mocker):
    # Arrange
    topic_entity = mocker.Mock()
    mocked_imported_files_view = mocker.patch.object(
        main_window.imported_files_view, 'deselect_all_files')
    mocked_selected_information_view = mocker.patch.object(
        main_window.selected_information_view, 'display_topic_info')

    # Act
    main_window.on_topic_clicked(topic_entity)

    # Assert
    mocked_imported_files_view.assert_called_once_with()
    mocked_selected_information_view.assert_called_once_with(topic_entity)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
