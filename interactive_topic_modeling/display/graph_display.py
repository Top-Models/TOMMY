from PySide6.QtWidgets import QWidget, QTabWidget


class GraphDisplay(QTabWidget):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setMinimumSize(450, 400)

        # Add first tab
        self.init_model = QWidget()
        self.init_model.setStyleSheet("background-color: black;")
        self.addTab(self.init_model, "init_model")
