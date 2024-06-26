import ctypes
import os
import platform
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from tommy.main_window import MainWindow
from tommy.support.application_settings import get_assets_folder
from tommy.support.constant_variables import initialize_fonts

"""This file is the program entry point."""


def set_app_user_model_id():
    """
    Set the AppUserModelID for the application.

    :return: None
    """
    if platform.system() == "Windows":
        try:
            app_id = "top-models.tommy.tommy.1"
            (ctypes.windll.shell32.
             SetCurrentProcessExplicitAppUserModelID(app_id))
        except (ImportError, AttributeError):
            print("Failed to set AppUserModelID.")


if __name__ == "__main__":
    # Program entry point
    app = QApplication(sys.argv)
    set_app_user_model_id()

    # Set window icon based on the operating system
    if platform.system() == "Windows":
        app.setWindowIcon(QIcon(os.path.join(get_assets_folder(), "tommy.ico"))
                          )
    elif platform.system() == "Darwin":
        app.setWindowIcon(QIcon(os.path.join(get_assets_folder(),
                                             "tommy_icon_macos.ico")))
    else:
        app.setWindowIcon(QIcon(os.path.join(get_assets_folder(),
                                             "tommy.ico")))

    # Set application name
    app.setApplicationDisplayName("TOMMY")

    # Initialize & load application fonts
    initialize_fonts()

    # Create and show main window
    window = MainWindow()
    window.show()

    # Execute the application
    app.exec()

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
