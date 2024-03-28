import pytest
from PySide6.QtWidgets import QApplication

from tommy.view.graph_view import GraphView


@pytest.fixture
def graph_display() -> GraphView:
    """Fixture to create and return an instance of GraphDisplay
    for testing."""
    # Create a PySide6 application instance
    app = QApplication([])

    # Create an instance of GraphDisplay with the correct parent (QWidget)
    display = GraphView()
    # Set parent to None or an appropriate QWidget if needed
    display.setParent(None)

    app.setParent(None)

    yield display

    # Cleanup
    app.quit()


class TestGraphDisplay:
    """Class to test the GraphDisplay."""
    def test_next_plot(self, graph_display) -> None:
        """Test method to verify the behaviour of the next_plot method."""
        # Perform any necessary setup or trigger events
        # to reach the desired state
        # For example, clicking on a tab
        graph_display.setCurrentIndex(0)

        # Get the current tab name
        tab_name = graph_display.tabText(graph_display.currentIndex())

        # Get the current plot index
        assert len(graph_display.plot_index.items()) > 0
        current_plot_index = graph_display.plot_index[tab_name]

        # Trigger the next_plot method
        graph_display.next_plot(tab_name)

        # Check if the plot index has been updated correctly
        assert (graph_display.plot_index[tab_name] == (current_plot_index + 1)
                % len(graph_display.plots_container[tab_name]))


if __name__ == "__main__":
    pytest.main()
