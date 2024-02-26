from PySide6.QtWidgets import QWidget, QTabWidget


class GraphDisplay(QTabWidget):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setMinimumSize(450, 400)
        self.setStyleSheet("""
                QTabBar::tab { 
                    background-color: #E40046; 
                    border-radius: 2px;
                    padding: 7px;
                    font-weight: bold;
                }
            """)

        # Add first tab
        self.init_model = QWidget()
        self.init_model.setStyleSheet("background-color: black;")
        self.addTab(self.init_model, "init_model")
