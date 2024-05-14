import pytest
from pytestqt.qtbot import QtBot

from tommy.main_window import MainWindow
from tommy.view.menu_bar import MenuBar


@pytest.fixture(scope='function')
def menu_bar(qtbot: QtBot) -> MenuBar:
    main_window = MainWindow()
    pj_controller = (main_window.controller.
                     project_settings_controller)

    menu_bar = MenuBar(main_window,
                       pj_controller)
    qtbot.addWidget(menu_bar)
    return menu_bar


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""