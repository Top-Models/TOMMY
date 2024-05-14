import csv
import os
import networkx as nx
from matplotlib import pyplot as plt
from pathlib import Path
from tommy.controller.graph_controller import GraphController

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

    def export_topic_words_csv(self, path: str) -> None:
        """
        Export words related to topics to a CSV file.
        :param path: Path to the CSV file
        :return: None
        """
        with open(path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Topic', 'Word', 'Score'])  # Write header row

            for i in range(self._graph_controller.get_number_of_topics()):
                topic_name = f"Topic {i + 1}"
                topic = self._graph_controller.get_topic_with_scores(i, 100)

                for word, score in zip(topic.top_words, topic.word_scores):
                    csv_writer.writerow([topic_name, word, score])

    def set_controller_refs(self, graph_controller) -> None:
        self._graph_controller = graph_controller
