import csv
import os
import networkx as nx
from pathlib import Path
from tommy.controller.graph_controller import GraphController
from tommy.controller.topic_modelling_controller import \
    TopicModellingController
from tommy.support.types import Document_topics


def hex_to_rgb(hex_color: str) -> tuple:
    """
    Convert hex color string to RGB tuple
    :param hex_color: Hex color string (e.g., "#RRGGBB")
    :return: RGB tuple (e.g., (R, G, B))
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


class ExportController:
    """Class for exporting graphs and networks to file"""
    _graph_controller: GraphController = None
    _topic_modelling_controller: TopicModellingController = None
    document_topics: Document_topics = []

    def is_topic_modelling_done(self) -> bool:
        """Check if topic modeling has been run"""
        try:
            return self._graph_controller.get_number_of_topics() > 0
        except RuntimeError:
            return False

    def export_networks(self, path: str) -> None:
        """
        Exports networks to gexf file for all available nx exports
        :param path: path to the folder where to save the gexf files
        :return: None
        """

        nx_exports = self._graph_controller.get_all_nx_exports()

        for i, graph in enumerate(nx_exports):
            new_path = os.path.join(path, f"{i}.gexf")

            # Create a new graph with the same nodes and edges to store colors
            graph_with_colors = nx.Graph(graph)

            # Store node and edge colors in the new graph
            for node, data in graph_with_colors.nodes(data=True):
                if 'color' in data:
                    color = data['color']
                    if isinstance(color, str):
                        color = hex_to_rgb(color)
                    graph_with_colors.nodes[node]['viz'] = \
                        {'color': {'r': color[0],
                                   'g': color[1],
                                   'b': color[2]}}

            for u, v, data in graph_with_colors.edges(data=True):
                if 'color' in data:
                    color = data['color']
                    if isinstance(color, str):
                        color = hex_to_rgb(color)
                    graph_with_colors[u][v]['viz'] = \
                        {'color': {
                            'r': color[0],
                            'g': color[1],
                            'b': color[2]}}

            nx.write_gexf(graph_with_colors, new_path)

    def export_graphs(self, path: str) -> None:
        """"
        Exports graphs to png file for all available visualizations
        :param path: path to the folder where to save the png files
        :return: None
        """
        # cache is ignored because it may give an error when trying to save
        # a figure that has already been used by pyqt
        graph_exports = self._graph_controller.get_all_visualizations(
                ignore_cache=True)

        for i in range(len(graph_exports)):
            new_path = os.path.join(path, f"{i}.png")
            figure, _ = graph_exports[i]
            figure.savefig(new_path)

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

    def on_document_topics_calculated(
            self,
            document_topics: Document_topics) -> None:
        """
        Update stored topic document correspondence reference.
        :param document_topics: The list of documents related to topics
        :return: None
        """

        self.document_topics = document_topics

    def export_document_topics_csv(self, path: str) -> list[str]:
        """
        Export documents related to topics to a CSV file.
        :param path: Path to the CSV file
        :return: List of error messages
        """



        errors = []
        try:
            with open(path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                header = ['Filename'] + ['Length'] + ['Author'] + ['Title'] + [
                    'Date'] + ['Path'] + [f'Topic {i + 1} Probability'
                                          for i in range(
                            len(self.document_topics[0][1]))]
                csv_writer.writerow(header)

                for metadata, probabilities in self.document_topics:
                    row = [metadata.name + "." + metadata.format,
                           str(metadata.length), metadata.author,
                           metadata.title, str(metadata.date),
                           metadata.path] + probabilities
                    csv_writer.writerow(row)
        except Exception as e:
            errors.append(f"Error exporting document topics to CSV: {repr(e)}")
        return errors

    def set_controller_refs(
            self,
            graph_controller: GraphController,
            topic_modelling_controller: TopicModellingController) -> None:
        self._graph_controller = graph_controller
        self._topic_modelling_controller = topic_modelling_controller
        topic_modelling_controller.calculate_topic_documents_event.subscribe(
                self.on_document_topics_calculated)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
