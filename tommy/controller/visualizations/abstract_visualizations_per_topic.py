from abc import ABC, abstractmethod

import matplotlib.figure

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)


class AbstractVisualizationPerTopic(ABC):
    """
    Abstract class that defines the interface to create a matplotlib figure
    of a visualization about a topic given a topic runner object and a topic_id
    """
    _required_interfaces: []
    name: str

    # dict from used topic_id -> cache of the generated plot
    _cached_figures: dict[int, matplotlib.figure.Figure] = {}

    def get_figure(self, topic_runner: TopicRunner,
                   topic_id: int) -> matplotlib.figure.Figure:
        """
        Get the matplotlib figure showing the requested visualization
        :param topic_runner: the topic runner to extract the result data from
        :param topic_id: the index of the topic to create the visualization
        :return: The matplotlib figure showing the requested visualization
        """
        # check if cache exists first
        result_figure = self._get_cached_figure(topic_id=topic_id)
        if result_figure is None:
            result_figure = self._create_figure(topic_runner=topic_runner,
                                                topic_id=topic_id)
            # save new figure in cache list
            self._cached_figures[topic_id] = result_figure
        return result_figure

    @abstractmethod
    def _create_figure(self,
                       topic_runner: TopicRunner,
                       topic_id: int) -> matplotlib.figure.Figure:
        """
        Get the matplotlib figure showing the requested visualization
        :param topic_runner: the topic runner to extract the result data from
        :param topic_id: the topic_id of the topic to get the figure on
        :return: matplotlib figure showing the requested visualization
        """

    def _get_cached_figure(self, topic_id: int
                           ) -> matplotlib.figure.Figure | None:
        """
        Get the cached figure for the corresponding topic_id if it exists
        :param topic_id: The topic id of the requested figure, defaults to None
        :return: A matplotlib figure showing the requested plot, or None
        """
        return self._cached_figures.get(topic_id, None)

    def is_possible(self, topic_runner: TopicRunner) -> bool:
        """
        Test whether the topic runner implements the necessary interfaces
        for this visualization type
        :param topic_runner: the topic runner to check interfaces from
        :return: True iff the visualization is possible on given topic runner
        """
        return all(isinstance(topic_runner, requirement)
                   for requirement in self._required_interfaces)

    def delete_cache(self):
        """Delete all cached figures"""
        self._cached_figures = {}


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
