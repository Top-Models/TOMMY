import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from interactive_topic_modeling.display.graph_display import GraphDisplay


@pytest.fixture
def graph_display():
    # Create a PySide6 application instance
    app = QApplication([])

    # Create an instance of GraphDisplay with the correct parent (QWidget)
    display = GraphDisplay()
    display.setParent(None)  # Set parent to None or an appropriate QWidget if needed

    app.setParent(None)

    yield display

    # Cleanup
    app.quit()


class TestGraphDisplay:
    def test_next_plot(self, graph_display):
        # Perform any necessary setup or trigger events to reach the desired state
        # For example, clicking on a tab
        graph_display.setCurrentIndex(0)

        # Get the current tab name
        tab_name = graph_display.tabText(graph_display.currentIndex())
        print(f"current tab name: {tab_name}")
        print(graph_display.plot_index)
        # Get the current plot index
        current_plot_index = graph_display.plot_index[tab_name]

        # Trigger the next_plot method
        graph_display.next_plot(tab_name)

        # Check if the plot index has been updated correctly
        assert graph_display.plot_index[tab_name] == (current_plot_index + 1) % len(
            graph_display.plots_container[tab_name])


if __name__ == "__main__":
    pytest.main()
