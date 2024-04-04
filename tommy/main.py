import sys
from PySide6.QtWidgets import QApplication

from tommy.main_window import MainWindow

# Program entry point
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
