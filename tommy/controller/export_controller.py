import matplotlib.figure
import networkx as nx
from matplotlib import pyplot as plt
from pathlib import Path
import os

from tommy.controller.controller import GraphController


class ExportController:
    def __init__(self, graph_controller):
        self._graph_controller = graph_controller

    def export_networks(self, path: str) -> None:
        nx_exports = self._graph_controller.get_all_nx_exports()

        for i in range(len(nx_exports)):
            new_path = os.path.join(path, f"{i}.gexf")
            nx.write_gexf(nx_exports[i], new_path)

    def export_graphs(self, path: str) -> None:
        graph_exports = self._graph_controller.get_all_visualizations()

        for i in range(len(graph_exports)):
            new_path = os.path.join(path, f"{i}.png")
            graph_exports[i].savefig(new_path)
