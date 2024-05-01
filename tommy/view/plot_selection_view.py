from PySide6.QtWidgets import QWidget, QTabWidget

from tommy.view.graph_view import GraphView

from tommy.controller.graph_controller import GraphController
from tommy.controller.visualizations.possible_visualization import (
    PossibleVisualization, VisGroup)


class PlotSelectionView(QTabWidget):
    """A class to display options for selecting a plot."""

    ORDER_OF_VIS_GROUPS: list[VisGroup] = [VisGroup.CORPUS,
                                           VisGroup.MODEL,
                                           VisGroup.TOPIC]
    assert len(ORDER_OF_VIS_GROUPS) == len(VisGroup), (
        "Not all visualization groups have a corresponding order in the plots "
        "selection view")

    def __init__(self, graph_controller: GraphController,
                 graph_view: GraphView) -> None:
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

        # Set reference to the graph-controller and graphview
        self._graph_controller = graph_controller
        self._graph_controller.plots_changed_event.subscribe(self._create_tabs)
        self._graph_view = graph_view

        # Initialize a dict from tab index to the corresponding visualization
        self._tabs_plots: dict[int, PossibleVisualization] = {}

        # Add tabChanged event
        self.currentChanged.connect(self._tab_clicked_event)

    def _tab_clicked_event(self) -> None:
        """Update the currently selected tab in the graph-view"""
        selected_tab_index = self.currentIndex()

        assert selected_tab_index in self._tabs_plots

        new_possible_vis = self._tabs_plots[selected_tab_index]
        new_plot = self._graph_controller.get_visualization(
            new_possible_vis.index)
        self._graph_view.display_plot(new_plot)

    def _create_tabs(self, possible_vis_list: list[PossibleVisualization]
                     ) -> None:
        """
        Create new tabs for all the possible visualizations
        :param possible_vis_list: The list of all possible visualization to
            create tabs for
        """
        # Clear layout and list of indices
        if self.count() > 0:
            self.clear()
        self._tabs_plots = {}

        # Partition all tabs based on in which visualization group they belong
        partitioned_tabs: dict[VisGroup, list[PossibleVisualization]] = {
            vis_group: []
            for vis_group in VisGroup}

        for vis in possible_vis_list:
            partitioned_tabs[vis.type].append(vis)

        # Create all tabs
        for vis_group in self.ORDER_OF_VIS_GROUPS:
            # add all tabs in the group
            tabs_in_group = partitioned_tabs[vis_group]
            self._add_multiple_tabs(tabs_in_group)

            # Add disabled tab as a spacer between groups
            self._add_spacer_tab()

    def _add_multiple_tabs(self, visualizations: list[PossibleVisualization]):
        """Add a tab and save the plot index for each visualization given"""
        for vis in visualizations:
            self._tabs_plots[self.count()] = vis
            self.addTab(QWidget(), vis.name)

    def _add_spacer_tab(self):
        """Add a disabled tab to the tabs bar as a spacer"""
        self.addTab(QWidget(), "     ")
        self.setTabEnabled(self.count() - 1, False)

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
