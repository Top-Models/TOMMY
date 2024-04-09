import matplotlib.figure
import networkx as nx
from matplotlib import pyplot as plt

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.datatypes.topics import Topic, TopicWithScores

from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)


class WordTopicNetworkCreator(AbstractVisualization):
    """
    A class for construct a word-topic network to plot the relations
    between topics and probable words and returning it as a matplotlib figure
    """
    _required_interfaces = []
    name = 'Topics en 15 meest voorkomende woorden'

    def get_figure(self,
                   topic_runner: TopicRunner
                   ) -> matplotlib.figure.Figure:
        """
        Construct a word-topic network which is used to plot the relations
        between topics and probable words
        :param topic_runner: The topic runner to extract topic data from
        :return: matplotlib figure showing a word-topic network plot
        """
        # Construct a plot and graph
        fig = plt.figure()
        graph = self._construct_word_topic_network(topic_runner)

        # Get the scale factor used for the displayed edge weight (width)
        edge_scale_factor = self._get_edge_scale_factor(topic_runner)

        # Get graph elements
        edges = graph.edges()
        nodes = graph.nodes(data="color")

        # Get drawing function arguments
        node_sizes = [150 if node[1] is not None else 0 for node in nodes]
        node_colors = [node[1] if node[1] is not None else "black" for node in
                       nodes]

        edge_colors = [graph[u][v]["color"] for (u, v) in edges]
        edge_width = [(graph[u][v]["weight"] * edge_scale_factor) for u, v in
                      edges]

        # Draw the graph
        nx.draw_kamada_kawai(graph,
                             node_size=node_sizes,
                             with_labels=True,
                             width=edge_width,
                             edge_color=edge_colors,
                             node_color=node_colors,
                             font_size=8)

        return fig

    @staticmethod
    def _construct_word_topic_network(topic_runner: TopicRunner) -> nx.Graph:
        """
        Construct a word-topic network which is used to plot the relations
        between topics and probable words
        :param topic_runner: The topic runner to extract topic data from
        :return: matplotlib figure showing a word-topic network plot
        """
        graph = nx.Graph()

        # List of simple, distinct colors from
        # https://sashamaps.net/docs/resources/20-colors/
        colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
                  '#9a6324', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
                  '#008080', '#e6beff', '#000075', '#fffac8', '#800000',
                  '#aaffc3', '#808000', '#ffd8b1', '#808080', '#911eb4']

        # Amount of words displayed for each topic
        node_amount = 15

        for topic in topic_runner.get_topics_with_scores(
                n_words=node_amount):
            # Add topic node to graph
            graph.add_node(topic.topic_id + 1,
                           color=colors[topic.topic_id % 20])

            # Add edge from topic node to its words
            for word, score in topic.top_words_with_scores:
                graph.add_edge(
                    topic.topic_id + 1,
                    word,
                    color=colors[topic.topic_id % 20],
                    weight=score)

        return graph

    @staticmethod
    def _get_edge_scale_factor(topic_runner: TopicRunner) -> float:
        """
        Calculates the scale factor to make sure the biggest edge in a network
        is always the same size, regardless of the maximum edge weight
        :param topic_runner: The topic runner on which the network will be
            made and the scale factor will be calculated for
        :return: The edge scale factor
        """

        # Find the maximum topic weight
        max_topic_weight = max(
            topic.word_scores[0]
            for topic
            in topic_runner.get_topics_with_scores(n_words=1)
        )

        # A constant which is multiplied by the scale factor according to an
        # edge width that is visually pleasing
        chosen_weight = 1.5

        scale_factor = (1 / max_topic_weight)

        return scale_factor * chosen_weight


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
