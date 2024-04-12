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

