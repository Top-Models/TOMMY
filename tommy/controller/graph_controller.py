from itertools import product

import matplotlib.figure

from tommy.controller.corpus_controller import CorpusController
from tommy.controller.publisher.event_handler import EventHandler
from tommy.datatypes.topics import TopicWithScores
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.file_import.metadata import Metadata

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.topic_modelling_controller import (
    TopicModellingController)
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.controller.visualizations.abstract_visualizations_per_topic import (
    AbstractVisualizationPerTopic)
from tommy.controller.visualizations.abstract_visualization_on_data import (
    AbstractVisualizationOnData)
from tommy.controller.visualizations.correlation_matrix_creator import (
    CorrelationMatrixCreator)
from tommy.controller.visualizations.top_words_bar_plot_creator import (
    TopWordsBarPlotCreator)
from tommy.controller.visualizations.word_cloud_creator import WordCloudCreator
from tommy.controller.visualizations.word_topic_network_creator import (
    WordTopicNetworkCreator)
from tommy.controller.visualizations.document_topic_network_summary_creator \
    import DocumentTopicNetworkSummaryCreator
from tommy.controller.visualizations.document_topic_network_creator import (
    DocumentTopicNetworkCreator)
from tommy.controller.visualizations.document_word_count_creator import (
    DocumentWordCountCreator)
from tommy.controller.visualizations.visualization_input_datatypes import (
    ProcessedCorpus, MetadataCorpus)


class GraphController:
    """
    The central interface for extracting results from topic modelling results
    and creating visualizations.
    Contains a publisher for when the plots are changed and a publisher for
    when the topics have changed.
    """
    _topic_modelling_controller: TopicModellingController = None
    _corpus_controller: CorpusController = None

    GLOBAL_VISUALIZATIONS: list[AbstractVisualization
                                | AbstractVisualizationOnData] = [
        CorrelationMatrixCreator(),
        WordTopicNetworkCreator(),
        DocumentTopicNetworkSummaryCreator(),
        DocumentWordCountCreator()
    ]
    TOPIC_VISUALIZATIONS: list[AbstractVisualizationPerTopic] = [
        WordCloudCreator(),
        TopWordsBarPlotCreator()
    ]
    _possible_global_visualizations: list[int] = None
    _possible_topic_visualizations: list[int] = None

    _current_visualization_index: int = None

    _current_topic_runner: TopicRunner = None

    _plots_changed_event: EventHandler[matplotlib.figure.Figure] = None
    _topics_changed_event: EventHandler[None] = None

    @property
    def plots_changed_event(self) -> EventHandler[matplotlib.figure.Figure]:
        """Get publisher that notifies when (selected) plots are changed."""
        return self._plots_changed_event

    @property
    def topics_changed_event(self) -> EventHandler[None]:
        """Get the publisher that notifies when the topics are changed."""
        return self._topics_changed_event

    def __init__(self) -> None:
        """Initialize the graph-controller and its two publishers"""
        super().__init__()
        self._plots_changed_event = EventHandler[matplotlib.figure.Figure]()
        self._topics_changed_event = EventHandler[None]()

    def set_model_refs(self,
                       topic_modelling_controller: TopicModellingController,
                       ) -> None:
        """Set reference to the TM controller and add self to its publisher"""
        self._topic_modelling_controller = topic_modelling_controller
        self._topic_modelling_controller.model_trained_event.subscribe(
            self.on_topic_runner_complete)

    def set_controller_refs(self,
                            corpus_controller: CorpusController):
        self._corpus_controller = corpus_controller

    def get_number_of_topics(self) -> int:
        """
        Get the number of topics in the topic modelling results
        :return: the number of topics in the topic modelling results
        :raises RuntimeError: if the topic runner has not finished running yet.
        """
        if self._current_topic_runner is None:
            raise RuntimeError("Amount of topics requested before topic "
                               "runner has finished running")
        return self._current_topic_runner.get_n_topics()

    def get_topic_with_scores(self, topic_id, n_words) -> TopicWithScores:
        """
        Return a topic object containing top n terms and their corresponding
        score for the topic identified by the topic_id.

        :param topic_id: the index of the requested topic
        :param n_words: number of terms in the resulting topic object
        :return: topic object containing top n terms and their corresponding
            scores
        """
        return self._current_topic_runner.get_topic_with_scores(
            topic_id=topic_id,
            n_words=n_words)

    def _calculate_possible_visualizations(self) -> None:
        """(re-)calculates and saves the list of possible visualizations"""
        # check each global visualization
        self._possible_global_visualizations = [
            vis_index
            for (vis_index, visualization)
            in enumerate(self.GLOBAL_VISUALIZATIONS)
            if visualization.is_possible(self._current_topic_runner)
        ]

        # check each topic visualization
        possible_topic_visualizations_indices = [
            vis_index
            for (vis_index, visualization)
            in enumerate(self.TOPIC_VISUALIZATIONS)
            if visualization.is_possible(self._current_topic_runner)
        ]

        # add all combinations of topic_id and topic visualization type
        self._possible_topic_visualizations = list(product(
            possible_topic_visualizations_indices,
            range(self.get_number_of_topics())
        ))

        # make sure that the visualization index does not become invalid
        if self._current_visualization_index is None:
            self._current_visualization_index = 0
        self._current_visualization_index %= self.get_visualization_count()

    def get_visualization_count(self) -> int:
        """Return the number of possible visualization that can be requested"""
        return (len(self._possible_global_visualizations)
                + len(self._possible_topic_visualizations))

    def get_current_visualization(self) -> matplotlib.figure.Figure:
        """
        Get the currently selected visualization as a matplotlib figure
        :return: the currently selected visualization as a matplotlib figure
        :raises Exception: if the topic runner has not finished running yet."""
        if self._current_visualization_index is None:
            raise Exception("Visualizations requested while visualizations"
                            "were not available yet.")
        return self._get_visualization(self._current_visualization_index)

    def _get_visualization(self, vis_index: int) -> matplotlib.figure.Figure:
        """
        Returns the visualization corresponding to the given index in the list
        of possible visualizations.
        :param vis_index: Index of the visualization to be requested
        :return: matplotlib figure of visualization corresponding to the index
        :raises IndexError: if the index is negative or bigger than the number
            of possible visualizations as calculated by this class.
        """
        # if not, the index is out of range
        if self._current_visualization_index < 0:
            raise IndexError(f'Negative index of {vis_index} is not accepted '
                             'in _get_visualization')

        # checks if the index of the visualization corresponds to a global vis.
        if vis_index < len(self._possible_global_visualizations):
            return self._get_global_visualization(vis_index)

        # checks if the index corresponds to a per-topic vis.
        topic_vis_index = vis_index - len(self._possible_global_visualizations)
        if topic_vis_index < len(self._possible_topic_visualizations):
            return self._get_topic_visualization(topic_vis_index)

        # if not, the index is out of range
        raise IndexError(f'No visualization with index {vis_index} available')

    def _get_global_visualization(self,
                                  vis_index: int) -> matplotlib.figure.Figure:
        """
        Returns the global visualization corresponding to the given index
        in the list of possible global visualizations
        :param vis_index: Index of the visualization to be requested
        :return: matplotlib figure of visualization corresponding to the index
        """
        selected_vis = self._possible_global_visualizations[vis_index]

        vis_creator = self.GLOBAL_VISUALIZATIONS[selected_vis]
        # check if the visualization creator needs processed corpus as input
        if isinstance(vis_creator,
                      AbstractVisualizationOnData):
            return self._run_global_visualization_on_data(vis_creator)

        # otherwise run the visualization without additional data
        return vis_creator.get_figure(self._current_topic_runner)

    def _run_global_visualization_on_data(self,
            vis_creator: AbstractVisualizationOnData):
        """
        Runs the global visualization on the additional data that it needs
        :param vis_creator: Index of the visualization to be requested
        :return: matplotlib figure of visualization corresponding to the index
        """

        if vis_creator.input_data_type == ProcessedCorpus:
            processed_corpus = self._corpus_controller.get_processed_corpus()
            return vis_creator.get_figure(self._current_topic_runner,
                                          processed_corpus)
        if vis_creator.input_data_type == MetadataCorpus:
            metadata = self._corpus_controller.get_metadata()
            return vis_creator.get_figure(self._current_topic_runner,
                                          metadata)

        raise Exception("The graph-controller is asked to supply data of type"
                        f" {vis_creator.input_data_type}, which is not "
                        " supported")

    def _get_topic_visualization(self,
                                 vis_index: int) -> matplotlib.figure.Figure:
        """
        Returns the topic visualization corresponding to the given index
        from the list of possible topic visualizations
        :param vis_index: Index of the visualization to be requested
        :return: matplotlib figure of visualization corresponding to the index
        """
        vis_index, vis_topic = (self._possible_topic_visualizations[vis_index])
        return (self.TOPIC_VISUALIZATIONS[vis_index]
                .get_figure(self._current_topic_runner, vis_topic))

    def on_next_plot(self) -> None:
        """
        Change the selected plot to the next one and notify the graph-view
        :raises RuntimeWarning: if the next plot is requested while the topic
            runner has not finished running yet.
        :return: None
        """
        if self._current_visualization_index is None:
            raise RuntimeWarning("Next plot requested while visualizations "
                                 "were not available yet.")
        self._current_visualization_index = (
                (self._current_visualization_index + 1)
                % self.get_visualization_count())
        self._plots_changed_event.publish(self.get_current_visualization())

    def on_previous_plot(self) -> None:
        """
        Change the selected plot to the previous one and notify the graph-view
        :raises RuntimeWarning: if the next plot is requested while the topic
            runner has not finished running yet.
        :return: None
        """
        if self._current_visualization_index is None:
            raise RuntimeWarning("Previous plot requested while "
                                 "visualizations were not available yet.")
        self._current_visualization_index = (
                (self._current_visualization_index - 1)
                % self.get_visualization_count())
        self._plots_changed_event.publish(self.get_current_visualization())

    def on_topic_runner_complete(self, topic_runner: TopicRunner) -> None:
        """
        Signal the graph-controller that a topic runner has finished training
        and is ready to provide results. Notify the subscribes of the plots
        and topics
        :param topic_runner: The newly trained topic runner object
        :return: None
        """
        self._current_topic_runner = topic_runner
        self._calculate_possible_visualizations()
        self._topics_changed_event.publish(None)
        self._plots_changed_event.publish(self.get_current_visualization())


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
