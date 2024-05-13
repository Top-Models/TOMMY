from abc import ABC, abstractmethod

import matplotlib.figure

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, TopicID, MetadataCorpus, ProcessedCorpus)


class AbstractVisualization(ABC):
    """
    Abstract class that defines the interface to create a matplotlib figure
    of a visualization given a topic runner object
    """
    _required_interfaces: list[type] = NotImplemented
    name: str = NotImplemented
    short_tab_name: str = NotImplemented
    vis_group: VisGroup = NotImplemented
    needed_input_data: list[VisInputData] = NotImplemented

    # dict from used topic_id -> cache of the generated plot
    _cached_figures: dict[int | None, matplotlib.figure.Figure] = {}

    def get_figure(self, topic_runner: TopicRunner,
                   topic_id: TopicID = None,
                   metadata_corpus: MetadataCorpus = None,
                   processed_corpus: ProcessedCorpus = None
                   ) -> matplotlib.figure.Figure:
        """
        Get the matplotlib figure showing the requested visualization
        :param topic_runner: the topic runner to extract the result data from
        :param topic_id: the index of the topic to create the visualization
            about if applicable, defaults to None
        :param metadata_corpus: the metadata of all documents in the corpus if
            applicable, defaults to None
        :param processed_corpus: the entire preprocessed corpus if applicable,
            defaults to None
        :return: The matplotlib figure showing the requested visualization
        """
        # check if cache exists first
        result_figure = self._get_cached_figure(topic_id=topic_id)
        if result_figure is None:
            result_figure = self._create_figure(topic_runner=topic_runner,
                                                topic_id=topic_id,
                                                metadata_corpus
                                                =metadata_corpus,
                                                processed_corpus
                                                =processed_corpus)
            # save new figure in cache list
            self._cached_figures[topic_id] = result_figure
        return result_figure

    def _get_cached_figure(self, topic_id: TopicID = None
                           ) -> matplotlib.figure.Figure | None:
        """
        Get the cached figure for the corresponding topic_id if it exists
        :param topic_id: The topic id of the requested figure, defaults to None
        :return: A matplotlib figure showing the requested plot, or None
        """
        return self._cached_figures.get(topic_id, None)

    @abstractmethod
    def _create_figure(self, topic_runner: TopicRunner,
                       topic_id: TopicID = None,
                       metadata_corpus: MetadataCorpus = None,
                       processed_corpus: ProcessedCorpus = None
                       ) -> matplotlib.figure.Figure:
        """
        Generate the matplotlib figure showing the requested visualization
        :param topic_runner: the topic runner to extract the result data from
        :param topic_id: the index of the topic to create the visualization
            about if applicable, defaults to None
        :param metadata_corpus: the metadata of all documents in the corpus if
            applicable, defaults to None
        :param processed_corpus: the entire preprocessed corpus if applicable,
            defaults to None
        :return: The matplotlib figure showing the requested visualization
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
        self._cached_figures = {}


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
