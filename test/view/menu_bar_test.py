import pytest
from pytestqt.qtbot import QtBot

from tommy.main_window import MainWindow
from tommy.view.menu_bar import MenuBar


@pytest.fixture(scope='function')
def menu_bar(qtbot: QtBot) -> MenuBar:
    main_window = MainWindow()
    menu_bar = MenuBar(main_window,
                       main_window.controller.project_settings_controller,
                       main_window.controller.saving_loading_controller,
                       main_window.controller.export_controller,
                       main_window.controller.topic_modelling_controller)
    qtbot.addWidget(menu_bar)
    return menu_bar


def test_disable_menu_on_start_topic_modelling(
        menu_bar: MenuBar):
    # Arrange
    menu_bar.import_input_folder_action.setEnabled(True)

    # Act
    menu_bar.disable_menu_on_start_topic_modelling()

    # Assert
    assert menu_bar.import_input_folder_action.isEnabled() is False


def test_enable_menu_on_finish_topic_modelling(
        menu_bar: MenuBar):
    # Arrange
    menu_bar.import_input_folder_action.setEnabled(False)

    # Act
    menu_bar.enable_menu_on_finish_topic_modelling()

    # Assert
    assert menu_bar.import_input_folder_action.isEnabled() is True


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""