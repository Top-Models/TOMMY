from collections.abc import Iterable
from typing import TypeAliasType

import matplotlib.figure
import networkx as nx
from matplotlib import pyplot as plt

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.datatypes.topics import Topic, TopicWithScores
from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)
from tommy.controller.visualizations.visualization_input_datatypes import (
    ProcessedCorpus)

from tommy.controller.visualizations.abstract_visualization_on_data import (
        AbstractVisualizationOnData)


class DocumentTopicNetworkCreator(
        AbstractVisualizationOnData[ProcessedCorpus]):
    """
    A class for constructing a network showing the topics and the
    number of documents that contain that topic for the topics in the given
    topic runner and the given preprocessed documents; and returning it as a
    matplotlib figure.
    Note: this visualization is only to be used for exporting purposed
    """
    _required_interfaces = [DocumentTopicsInterface]
    name = 'Topics en documenten die daar ten minste 5% bij horen'

    @property
    def input_data_type(self) -> TypeAliasType:
        """Returns the type of the additional data needed in get_figure"""
        return ProcessedCorpus

    def get_figure(self,
                   topic_runner: TopicRunner | DocumentTopicsInterface,
                   data: ProcessedCorpus
                   ) -> matplotlib.figure.Figure:
        """
        Construct a document-topic network plot showing the
        relations between documents and topics
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :param data: The preprocessed corpus containing
            all files as bags of words after preprocessing.
        :return: matplotlib figure showing a document-topic network plot
        """
        # Construct a plot and graph
        fig = plt.figure(dpi=20)
        graph = self.construct_doc_topic_network(topic_runner, data)

        # Get graph elements
        edges = graph.edges()
        nodes = graph.nodes(data="color")

        # Get drawing function arguments
        node_sizes = [150 if node[1] is not None else 0 for node in nodes]
        node_colors = [node[1] if node[1] is not None else "black"
                       for node in nodes]

        edge_colors = [graph[u][v]["color"] for (u, v) in edges]
        edge_width = [(graph[u][v]["weight"]) for u, v in edges]

        # Draw the network using the kamada-kawai algorithm to position the
        # nodes in an aesthetically pleasing way
        nx.draw_kamada_kawai(graph,
                             width=edge_width,
                             node_size=node_sizes,
                             edge_color=edge_colors,
                             node_color=node_colors)

        return fig

    @staticmethod
    def construct_doc_topic_network(topic_runner:
                                    TopicRunner | DocumentTopicsInterface,
                                    processed_files: ProcessedCorpus
                                    ) -> nx.Graph:
        """
        Construct a document-topic network plot which is used to plot the
        relations
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :param processed_files: The preprocessed corpus containing
            all files as bags of words after preprocessing.
        :return: matplotlib figure showing a document-topic network plot
        """
        graph = nx.Graph()

        # List of simple, distinct colors from
        # https://sashamaps.net/docs/resources/20-colors/
        colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
                  '#9a6324', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
                  '#008080', '#e6beff', '#000075', '#fffac8', '#800000',
                  '#aaffc3', '#808000', '#ffd8b1', '#808080', '#911eb4']

        for topic_id in range(topic_runner.get_n_topics()):
            graph.add_node(topic_id, color=colors[topic_id % 20])

        # Generate initial document topic network
        for document_id, document in enumerate(processed_files):
            document_topic = (
                topic_runner.get_document_topics(document.body.body, 0.05))

            # Add edges from each document to all associated topics
            for (topic_id, topic_probability) in document_topic:
                graph.add_edge(topic_id,
                               'document:' + str(document_id),
                               color=colors[topic_id % 20],
                               weight=topic_probability)
        return graph


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
