# from abc import ABC, abstractmethod
# from collections.abc import Iterable
#
# import matplotlib.figure
#
# from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
#     TopicRunner)
# from tommy.controller.file_import.processed_file import ProcessedFile, Metadata
# from tommy.controller.visualizations.possible_visualization import VisGroup
#
#
# class AbstractVisualizationOnData[T: Iterable[ProcessedFile]
#                                   | list[Metadata]
#                                   ](ABC):
#     """
#     Abstract class that defines the interface to create a matplotlib figure
#     of a visualization about a given topic runner object using additional data
#     of a generic type supplied by the graph-controller.
#     """
#     _required_interfaces: []
#     name: str
#     vis_group: VisGroup
#
#     @property
#     @abstractmethod
#     def input_data_type(self) -> type:
#         pass
#
#     @abstractmethod
#     def get_figure(self,
#                    topic_runner: TopicRunner,
#                    data: T
#                    ) -> matplotlib.figure.Figure:
#         """
#         Get the matplotlib figure showing the requested visualization
#         :param topic_runner: the topic runner to extract the result data from
#         :param data: the additional data to be used in the visualization.
#         :return: matplotlib figure showing the requested visualization
#         """
#
#     def is_possible(self, topic_runner: TopicRunner) -> bool:
#         """
#         Test whether the topic runner implements the necessary interfaces
#         for this visualization type
#         :param topic_runner: the topic runner to check interfaces from
#         :return: True iff the visualization is possible on given topic runner
#         """
#         return all(isinstance(topic_runner, requirement)
#                    for requirement in self._required_interfaces)
#
#
# """
# This program has been developed by students from the bachelor Computer Science
# at Utrecht University within the Software Project course.
# © Copyright Utrecht University
# (Department of Information and Computing Sciences)
# """
