from PySide6.QtWidgets import QWidget, QTabWidget

from interactive_topic_modeling.support.constant_variables import \
    hover_prim_col_red
from interactive_topic_modeling.view.observer.observer import Observer


class ModelSelectionView(QTabWidget, Observer):
    """A class to display options for selecting a model."""

    def __init__(self) -> None:
        """Initialize the GraphDisplay."""
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet(f"""        
                QTabWidget {{
                    color: black;
                    border: none;
                }}

                QTabBar::tab {{ 
                    background-color: #FFFFFF; 
                    color: gray;
                    font-size: 15px;
                    padding-left: 10px;
                    padding-right: 10px;
                    padding-top: 14px;
                    padding-bottom: 14px;
                    font-weight: bold;
                }}

                QTabBar::tab:selected {{
                    border-bottom: 3px solid {hover_prim_col_red};
                    color: #000000;
                    background-color: rgba(240, 240, 240, 1);
                }}

                QTabBar::tab:hover {{
                    color: #000000;
                }}
                
                QTabWidget::tab-bar {{
                    alignment: left;
                }}
            """)

        # Add first tab
        self.addTab(QWidget(), "lda_model")

        # TODO: For demo purposes, remove this tab later
        self.addTab(QWidget(), "nmf_model")

        # Events
        self.currentChanged.connect(self.tab_clicked_event)

    def get_active_tab_name(self) -> str:
        """
        Get the name of the active tab.

        :return: The name of the active tab
        """
        return self.tabText(self.currentIndex())

    def tab_clicked_event(self) -> None:
        """
        Handle a tab clicked event.
        """
        # TODO: Implement when Connector is implemented
        pass

    def update_observer(self, publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
