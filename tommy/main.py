import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from tommy.main_window import MainWindow

"""This file is the program entry point."""

# Program entry point
app = QApplication(sys.argv)

# Set window icon
icon_path = os.path.abspath("../assets/tommy.ico")
app.setWindowIcon(QIcon(icon_path))

# Set application name
app.setApplicationDisplayName("TOMMY")

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
