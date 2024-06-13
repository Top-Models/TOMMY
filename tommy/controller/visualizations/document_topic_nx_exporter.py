from typing import TypeAliasType

import networkx as nx

from tommy.support.constant_variables import plot_colors
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)

from tommy.controller.visualizations.visualization_input_datatypes import (
    ProcessedCorpus)
from tommy.controller.visualizations.nx_exporter_on_data import (
    NxExporterOnData)


class DocumentTopicNxExporter(NxExporterOnData[ProcessedCorpus]):
    """
    A class for constructing a network showing the topics and the
    number of documents that contain that topic for the topics in the given
    topic runner and the given preprocessed documents; and returning it as an
    nx.Graph.
    Note: this visualization is only to be used for exporting purposes
    """
    _required_interfaces = [DocumentTopicsInterface, TopicRunner]
    name = 'Topics en documenten netwerk'

    @property
    def input_data_type(self) -> TypeAliasType:
        """Returns the type of the additional data needed in get_nx_graph"""
        return ProcessedCorpus

    def get_nx_graph(self,
                     topic_runner: TopicRunner | DocumentTopicsInterface,
                     data: ProcessedCorpus
                     ) -> nx.Graph:
        """
        Construct a document-topic nx graph representing plot of the
        relations between documents and topics
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :param data: The preprocessed corpus containing
            all files as bags of words after preprocessing.
        :return: nx graph representing a document-topic network plot
        """
        return self.construct_doc_topic_network(topic_runner, data, 0.05)

    @staticmethod
    def construct_doc_topic_network(topic_runner: TopicRunner
                                                  | DocumentTopicsInterface,
                                    processed_files: ProcessedCorpus,
                                    minimum_probability: float
                                    ) -> nx.Graph:
        """
        Construct a document-topic network plot which is used to plot the
        relations
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :param processed_files: The preprocessed corpus containing
            all files as bags of words after preprocessing.
        :param minimum_probability: the minimum probability of a document 
            belonging to a topic for it to be included.
        :return: matplotlib figure showing a document-topic network plot
        """
        graph = nx.Graph()

        for topic_id in range(topic_runner.get_n_topics()):
            graph.add_node(topic_id,
                           color=plot_colors[topic_id % len(plot_colors)])

        # Generate initial document topic network
        for document_id, document in enumerate(processed_files):
            document_topic = (
                topic_runner.get_document_topics(document.body.body,
                                                 minimum_probability))

            # Add edges from each document to all associated topics
            for (topic_id, topic_probability) in document_topic:
                graph.add_edge(topic_id,
                               'document:' + str(document_id),
                               color=plot_colors[topic_id % len(plot_colors)],
                               weight=topic_probability)
        return graph


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
