from PySide6.QtWidgets import QWidget, QTabWidget


class ModelSelectionView(QTabWidget):
    """A class to display options for selecting a model."""

    def __init__(self) -> None:
        """Initialize the GraphDisplay."""
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("""        
                QTabWidget {
                    color: black;
                    border: none;
                }

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

        # Add first tab
        self.addTab(QWidget(), "lda_model")

    def get_active_tab_name(self) -> str:
        """
        Get the name of the active tab.

        :return: The name of the active tab
        """
        return self.tabText(self.currentIndex())


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
