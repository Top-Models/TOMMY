import matplotlib.figure
import networkx as nx
from matplotlib import pyplot as plt
from pathlib import Path
import os

from tommy.controller.controller import GraphController


class ExportController:
    """Class for exporting graphs and networks to file"""
    _graph_controller: GraphController = None

    def export_networks(self, path: str) -> None:
        """"
        Exports networks to gexf file for all available nx exports
        :param path: path to the folder where to save the gexf files
        :return: None
        """
        nx_exports = self._graph_controller.get_all_nx_exports()

        for i in range(len(nx_exports)):
            new_path = os.path.join(path, f"{i}.gexf")
            nx.write_gexf(nx_exports[i], new_path)

    def export_graphs(self, path: str) -> None:
        """"
        Exports graphs to png file for all available visualizations
        :param path: path to the folder where to save the png files
        :return: None
        """
        graph_exports = self._graph_controller.get_all_visualizations()

        for i in range(len(graph_exports)):
            new_path = os.path.join(path, f"{i}.png")
            graph_exports[i].savefig(new_path)

    def set_controller_refs(self, graph_controller: GraphController) -> None:
        self._graph_controller = graph_controller


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
