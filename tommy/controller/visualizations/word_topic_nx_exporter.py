import networkx as nx

from tommy.support.constant_variables import plot_colors
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)

from tommy.controller.visualizations.nx_exporter import (NxExporter)


class WordTopicNxExporter(NxExporter):
    """
    A class for constructing a network showing the words and its relation to
    the topics for the given topic runner, returning it as an nx.Graph.
    Note: this visualization is only to be used for exporting purposes
    """
    _required_interfaces = [TopicRunner]
    name = 'Topics en woorden die daarbij horen'

    def get_nx_graph(self,
                     topic_runner: TopicRunner | DocumentTopicsInterface
                     ) -> nx.Graph:
        """
        Construct a word-topic nx graph representing plot of the
        relations between words and topics
        :param topic_runner: The topic runner to extract topic data from
        :return: nx graph representing a word-topic network plot
        """
        return self.construct_word_topic_network(topic_runner, 50)

    @staticmethod
    def construct_word_topic_network(topic_runner: TopicRunner
                                     , node_amount: int) -> nx.Graph:
        """
        Construct a word-topic network which is used to plot the relations
        between topics and probable words
        :param topic_runner: The topic runner to extract topic data from
        :param node_amount: The amount of words connected to each topic
        :return: matplotlib figure showing a word-topic network plot
        """
        graph = nx.Graph()

        for topic in topic_runner.get_topics_with_scores(
                n_words=node_amount):
            # Add topic node to graph
            graph.add_node(topic.topic_id + 1,
                           color=plot_colors[topic.topic_id
                                             % len(plot_colors)])

            # Add edge from topic node to its words
            for word, score in topic.top_words_with_scores:
                graph.add_edge(
                    topic.topic_id + 1,
                    word,
                    color=plot_colors[topic.topic_id % len(plot_colors)],
                    weight=score)

        return graph


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
