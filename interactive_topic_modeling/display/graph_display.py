from PySide6.QtWidgets import QWidget, QTabWidget


class GraphDisplay(QTabWidget):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("""
                QTabBar::tab { 
                    background-color: #FFFFFF; 
                    color: gray;
                    font-size: 15px;
                    padding: 7px;
                    font-weight: bold;
                }
                
                QTabBar::tab:selected {
                    border-bottom: 2px solid #E40046;
                    color: #000000;
                }
                
                QTabBar::tab:hover {
                    color: #000000;
                }
            """)

        # Add first tab
        self.init_model = QWidget()
        self.init_model.setStyleSheet("background-color: black;")
        self.addTab(self.init_model, "init_model")

        # Add second tab (for demonstration)
        self.demo_second_tab = QWidget()
        self.demo_second_tab.setStyleSheet("background-color: pink;")
        self.addTab(self.demo_second_tab, "demo_second_tab")
