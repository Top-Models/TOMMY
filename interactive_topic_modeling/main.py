import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QStyle
from interactive_topic_modeling.main_window import MainWindow


# Program entry point
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
