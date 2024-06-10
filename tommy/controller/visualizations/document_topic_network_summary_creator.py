import math

import matplotlib.figure
import networkx as nx
from matplotlib import pyplot as plt

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.controller.visualizations.document_topic_nx_exporter import (
    DocumentTopicNxExporter)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, ProcessedCorpus)

from tommy.support.constant_variables import plot_colors


class DocumentTopicNetworkSummaryCreator(AbstractVisualization):
    """
    A class for constructing a network showing the summary of topics and the
    number of documents that contain that topic for the topics in the given
    topic runner and the given preprocessed documents; and returning it as a
    matplotlib figure.
    """
    _required_interfaces = [DocumentTopicsInterface, TopicRunner]
    name = 'Topics en documenten die daar ten minste 5% bij horen'
    short_tab_name = 'Doc. Netwerk'
    vis_group = VisGroup.MODEL
    needed_input_data = [VisInputData.PROCESSED_CORPUS]

    def _create_figure(self,
                       topic_runner: TopicRunner | DocumentTopicsInterface,
                       processed_corpus: ProcessedCorpus = None,
                       **kwargs) -> matplotlib.figure.Figure:
        """
        Construct a summarized document-topic network plot showing the
        relations between documents and topics
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :param processed_corpus: The preprocessed corpus containing
            all files as bags of words after preprocessing.
        :return: matplotlib figure showing a document-topic network plot
        :raises ValueError: If the processed_corpus argument is None
        """
        if processed_corpus is None:
            raise ValueError("Preprocessed Corpus keyword argument is "
                             "necessary in the "
                             "document_topic_network_summary_creator")

        # Construct a plot and a graph
        fig = plt.figure(dpi=60)
        plt.title(self.name, pad=25)
        graph = self._construct_doc_topic_network(topic_runner,
                                                  processed_corpus)

        # Get graph elements
        edges = graph.edges()
        nodes = graph.nodes(data="color")

        # Get scaling factor used for scaling the nodes and edges to make sure
        # these don't increase when more documents are added
        scaling_factor = self._get_scaling_doc_topic(graph)

        # Get drawing function arguments
        node_sizes = []
        for node in nodes:
            # Give topic nodes a constant size
            if node[1] is not None:
                node_sizes.append(200)

            # Give doc_set nodes a scaling size
            else:
                first_neighbor = list(graph.neighbors(node[0]))[0]
                node_sizes.append(graph[node[0]][first_neighbor]["weight"]
                                  * scaling_factor * 6.9)

        node_colors = [node[1] if node[1] is not None else "black"
                       for node in nodes]

        edge_colors = [graph[u][v]["color"] for (u, v) in edges]
        edge_width = [(graph[u][v]["weight"]) * scaling_factor * 0.69
                      for u, v in edges]

        # Calculate the shortest paths using dijkstra's algorithm
        shortest_path_lengths = dict(
            nx.shortest_path_length(graph, weight="weight"))

        # Calculate new "shortest" paths to aid visualization
        for source in shortest_path_lengths:
            for target in shortest_path_lengths[source]:
                x = shortest_path_lengths[source][target]
                if x == 0:
                    continue
                shortest_path_lengths[source][target] = (
                    max(x + 5 * math.log(x, 2), 15))

        # Define a custom position using the new "shortest" paths
        pos = nx.kamada_kawai_layout(graph, dist=shortest_path_lengths)

        # Draw the network using the kamada-kawai algorithm to position the
        # nodes in an aesthetically pleasing way.
        nx.draw(graph,
                pos=pos,
                width=edge_width,
                node_size=node_sizes,
                edge_color=edge_colors,
                node_color=node_colors)

        # Add labels to the topic nodes
        labels = {}
        for topic_id in range(topic_runner.get_n_topics()):
            labels[topic_id] = topic_id + 1

        nx.draw_networkx_labels(graph, pos, labels=labels)

        # Adjust the figure
        fig.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)

        plt.close()
        return fig

    @staticmethod
    def _construct_doc_topic_network(topic_runner: TopicRunner
                                                   | DocumentTopicsInterface,
                                     processed_files: ProcessedCorpus
                                     ) -> nx.Graph:
        """
        Construct a summarized document-topic network plot which is used to
        plot the relations
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :param processed_files: The preprocessed corpus containing
            all files as bags of words after preprocessing.
        :return: matplotlib figure showing a document-topic network plot
        """

        # Construct a graph with topic nodes
        init_graph = DocumentTopicNxExporter.construct_doc_topic_network(
            topic_runner, processed_files, 0.05)

        # Construct simplified document topic network
        graph = nx.Graph()

        # Add topic nodes and nodes with degree one to graph
        num_topics: int = topic_runner.get_n_topics()
        for topic_id in range(num_topics):
            graph.add_node(topic_id,
                           color=plot_colors[topic_id % len(plot_colors)])
            lonely_nodes = [node for node in init_graph.neighbors(topic_id)
                            if init_graph.degree(node) == 1]
            if len(lonely_nodes) > 0:
                graph.add_edge(topic_id,
                               'doc_set_' + str(topic_id),
                               color=plot_colors[topic_id % len(plot_colors)],
                               weight=len(lonely_nodes))

        # Add nodes shared by multiple topics
        doc_set_id = num_topics - 1
        for topic_id in range(num_topics):
            for j in range(num_topics):
                doc_set_id += 1
                if topic_id >= j:
                    doc_set_id -= 1
                    continue

                # Calculate the intersection of two node's neighbors
                set1 = set(init_graph.neighbors(topic_id))
                set2 = set(init_graph.neighbors(j))
                intersection = set1.intersection(set2)

                # Add an edge from both topic nodes to a single "intersection"
                # node
                if len(intersection) != 0:
                    graph.add_edge(topic_id,
                                   "doc_set_" + str(doc_set_id),
                                   color=plot_colors[topic_id
                                                     % len(plot_colors)],
                                   weight=len(intersection))
                    graph.add_edge(j,
                                   "doc_set_" + str(doc_set_id),
                                   color=plot_colors[j
                                                     % len(plot_colors)],
                                   weight=len(intersection))

        return graph

    @staticmethod
    def _get_scaling_doc_topic(graph: nx.Graph) -> float:
        """
        Calculates the scale factor to make sure the biggest edge in a network
        is always the same size, regardless of the maximum edge weight
        :param graph: The graph model to calculate the scale factor for
        :return: The edge scale factor
        """

        # Find the maximum edge weight
        weight = [weight for node1, node2, weight in
                  graph.edges(data="weight")]
        max_edge_weight = max(weight)

        # A constant which is multiplied by the scale factor according to an
        # edge width that is visually pleasing
        chosen_weight = 10

        scale_factor = (1 / max_edge_weight)

        return scale_factor * chosen_weight


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
