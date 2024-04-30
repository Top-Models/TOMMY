from abc import abstractmethod

import networkx as nx

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)


class NxExporter:
    """
    Abstract class that defines the interface to create an nx graph of a
    visualization about a given topic runner object.
    """
    _required_interfaces: []
    name: str

    @abstractmethod
    def get_nx_graph(self,
                     topic_runner: TopicRunner
                     ) -> nx.Graph:
        """
        Get the nx graph data representing showing the requested visualization
        :param topic_runner: the topic runner to extract the result data from
        :return: matplotlib figure showing the requested visualization
        """

    def is_possible(self, topic_runner: TopicRunner) -> bool:
        """
        Test whether the topic runner implements the necessary interfaces
        for this visualization type
        :param topic_runner: the topic runner to check interfaces from
        :return: True iff the visualization is possible on given topic runner
        """
        return all(isinstance(topic_runner, requirement)
                   for requirement in self._required_interfaces)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
