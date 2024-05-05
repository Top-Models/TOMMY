from abc import ABC, abstractmethod
from collections.abc import Iterable

import matplotlib.figure

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.file_import.processed_file import ProcessedFile, Metadata


class AbstractVisualizationOnData[T: Iterable[ProcessedFile]
                                  | list[Metadata]
                                  ](ABC):
    """
    Abstract class that defines the interface to create a matplotlib figure
    of a visualization about a given topic runner object using additional data
    of a generic type supplied by the graph-controller.
    """
    _required_interfaces: []
    name: str

    @property
    @abstractmethod
    def input_data_type(self) -> type:
        pass

    # cache of the generated plot
    _cached_figure: matplotlib.figure.Figure | None = None

    def get_figure(self, topic_runner: TopicRunner,
                   data: T) -> matplotlib.figure.Figure:
        """
        Get the matplotlib figure showing the requested visualization
        :param topic_runner: the topic runner to extract the result data from
        :param data: the additional data to be used in the visualization.
        :return: matplotlib figure showing the requested visualization
        """
        # check if cache exists first
        result_figure = self._get_cached_figure()
        if result_figure is None:
            result_figure = self._create_figure(topic_runner=topic_runner,
                                                data=data)
            # save new figure in cache list
            self._cached_figure = result_figure
        return result_figure

    def _get_cached_figure(self) -> matplotlib.figure.Figure | None:
        """
        Get the cached figure  if it exists
        :return: A matplotlib figure showing the requested plot, or None
        """
        return self._cached_figure

    @abstractmethod
    def _create_figure(self, topic_runner: TopicRunner,
                       data: T) -> matplotlib.figure.Figure:
        """
        Generate the matplotlib figure showing the requested visualization
        :param topic_runner: the topic runner to extract the result data from
        :param data: the additional data to be used in the visualization.
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

    def delete_cache(self):
        """Delete all cached figures"""
        self._cached_figure = None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
