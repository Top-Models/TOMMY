from PySide6.QtWidgets import QWidget, QTabWidget

from tommy.controller.graph_controller import GraphController
from tommy.support.constant_variables import (
    hover_prim_col_red)


class PlotSelectionView(QTabWidget):
    """A class to display options for selecting a plot."""

    def __init__(self, graph_controller: GraphController) -> None:
        """Initialize the GraphDisplay."""
        super().__init__()

        # Initialize widget properties
        self.setFixedHeight(50)
        self.setStyleSheet(f"""        
                QTabWidget {{
                    color: black;
                    border: none;
                }}

                QTabBar::tab {{ 
                    background-color: rgba(210, 210, 210, 1);
                    color: rgba(120, 120, 120, 1);
                    font-size: 15px;
                    padding-left: 10px;
                    padding-right: 10px;
                    padding-top: 15px;
                    padding-bottom: 15px;
                    font-weight: bold;
                }}

                QTabBar::tab:disabled {{
                    background-color: white;
                    color: white;
                }}

                QTabBar::tab:selected {{
                    color: #000000;
                    background-color: rgba(230, 230, 230, 1);
                }}

                QTabBar::tab:hover {{
                    background-color: rgba(230, 230, 230, 1);
                }}
                
                QTabWidget::tab-bar {{
                    alignment: left;
                }}
            """)

        # Set reference to the graph-controller
        self._graph_controller = graph_controller

        # Non-topic modelling tabs
        self.addTab(QWidget(), "Woordaantal")
        self.addTab(QWidget(), "     ")

        # General tabs
        self.addTab(QWidget(), "Correlatie")
        self.addTab(QWidget(), "Topic Netwerk")
        self.addTab(QWidget(), "Doc. Netwerk")
        self.addTab(QWidget(), "     ")

        # Topic specific tabs
        self.addTab(QWidget(), "Woordenwolk")
        self.addTab(QWidget(), "Woordgewichten")

        # Disable the empty space tabs
        self.setTabEnabled(1, False)
        self.setTabEnabled(5, False)

        # Initially hide topic specific tabs
        self.toggle_topic_specific_tabs(False)

        # Add tabChanged event
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
        self._tab_clicked_event()

    def toggle_topic_specific_tabs(self, visible: bool) -> None:
        """
        Toggle the visibility of the topic specific tabs.

        :param visible: Whether to make the tabs visible
        """
        if not visible and self.currentIndex() in [6, 7]:
            self.setCurrentIndex(0)

        # Hide or show the tabs
        self.setTabVisible(6, visible)
        self.setTabVisible(7, visible)

    def _tab_clicked_event(self) -> None:
        """Update the currently selected tab"""
        tab_index = self.currentIndex()
        if tab_index in [2, 3, 4]:
            self._graph_controller.set_tab_index(tab_index - 1)
        elif tab_index in [6, 7]:
            self._graph_controller.set_tab_index(tab_index - 2)
        else:
            self._graph_controller.set_tab_index(tab_index)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""