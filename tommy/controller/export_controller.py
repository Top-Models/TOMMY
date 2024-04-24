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
        # TODO maak een pad met OS
        # path_file = os.sep.join([path_dir, filename])
        # os.path.join
# FileNotFoundError: [Errno 2] No such file or directory: 'C:/dev/interactive-topic-modeling/tommy/jfsdk\\0.gexf'

    def export_graphs(self):
        pass

    # def set_controller_refs(self, graph_controller: GraphController) -> None:
    #     print("help me")
    #     self._graph_controller = graph_controller
