from PySide6.QtWidgets import QWidget, QTabWidget

from interactive_topic_modeling.display.topic_display.fetched_topics_display import FetchedTopicsDisplay


class GraphDisplay(QTabWidget):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("""
                QTabWidget::pane {
                    border: none; 
                }
                
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

        # Initialize widgets
        self.fetched_topics_display = FetchedTopicsDisplay()

        # Add first tab
        self.init_model = QWidget()
        self.init_model.setStyleSheet("background-color: black;")
        self.addTab(self.init_model, "init_model")

        # Add second tab (for demonstration)
        self.demo_second_tab = QWidget()
        self.demo_second_tab.setStyleSheet("background-color: pink;")
        self.addTab(self.demo_second_tab, "demo_second_tab")

        # Event handling
        self.tabBarClicked.connect(self.on_tab_clicked)

    def on_tab_clicked(self, index) -> None:
        """
        Event handler for when a tab is clicked
        :param index: Index of the clicked tab
        :return: None
        """

        clicked_tab_name = self.tabText(index)
        self.fetched_topics_display.display_topics(clicked_tab_name)
