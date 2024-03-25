import sys
from PySide6.QtWidgets import QApplication

from tommy.main_window import MainWindow

"""This file is the program entry point."""

# Program entry point
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
