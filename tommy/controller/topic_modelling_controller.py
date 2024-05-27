from tommy.controller.file_import.processed_corpus import ProcessedCorpus
from tommy.controller.model_parameters_controller import (
    ModelParametersController,
    ModelType)
from tommy.controller.corpus_controller import CorpusController
from tommy.model.config_model import ConfigModel
from tommy.controller.result_interfaces.document_topics_interface import \
    DocumentTopicsInterface

from tommy.model.topic_model import TopicModel

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.controller.topic_modelling_runners.nmf_runner import NmfRunner
from tommy.support.event_handler import EventHandler


class TopicModellingController:
    """
    Controller that runs the selected topic modelling algorithm on a call of
    train_model and supplies a topic runner object from which results can be
    extracted.
    """
    _model_parameters_controller: ModelParametersController = None
    _topic_model: TopicModel = None
    _config_model: ConfigModel = None
    _corpus_controller: CorpusController = None
    _model_trained_event: EventHandler[TopicRunner] = None
    _topic_model_switched_event: EventHandler[TopicRunner] = None
    _calculate_document_topics_event: \
        EventHandler[ProcessedCorpus] = None

    @property
    def model_trained_event(self) -> EventHandler[TopicRunner]:
        return self._model_trained_event

    @property
    def topic_model_switched_event(self) -> EventHandler[TopicRunner]:
        return self._topic_model_switched_event

    @property
    def calculate_topic_documents_event(self) -> (
            EventHandler)[ProcessedCorpus]:
        return self._calculate_document_topics_event

    def __init__(self) -> None:
        """Initialize the publisher of the topic-modelling-controller"""
        super().__init__()
        self._model_trained_event = EventHandler[TopicRunner]()
        self._topic_model_switched_event = EventHandler[TopicRunner]()
        self._calculate_document_topics_event = (
            EventHandler[ProcessedCorpus]())

    def set_model_refs(self,
                       topic_model: TopicModel,
                       config_model: ConfigModel) -> None:
        """
        Set the references to the topic model
        :return: None
        """
        self._topic_model = topic_model
        self._config_model = config_model

    def change_config_model_refs(self,
                                 topic_model: TopicModel,
                                 config_model: ConfigModel) -> None:
        """
        Set the references to the topic model when switching configs
        :return: None
        """
        # TODO: send event to view and other controllers that the
        #  visualizations should change
        self._topic_model = topic_model
        self._config_model = config_model
        self._topic_model_switched_event.publish(config_model.topic_runner)

    def set_controller_refs(self,
                            parameters_controller: ModelParametersController,
                            corpus_controller: CorpusController):
        self._model_parameters_controller = parameters_controller
        self._corpus_controller = corpus_controller

    def train_model(self) -> None:
        """
        Trains the selected model from scratch on the currently loaded data
        and notifies the observers that a (new) topic runner is ready
        :raises NotImplementedError: if selected model type is not supported
        :return: None
        """
        new_model_type = self._model_parameters_controller.get_model_type()

        match new_model_type:
            case ModelType.LDA:
                self._train_lda()
            case ModelType.NMF:
                self._train_nmf()
            case _:
                raise NotImplementedError(
                    f"model type {new_model_type.name} is not supported by "
                    f"topic modelling controller")

        self._model_trained_event.publish(self._config_model.topic_runner)

    def calculate_document_topics(self):
        processed_files = self._corpus_controller.get_processed_corpus()
        # inherit both TopicRunner and DocumentTopicsInterface
        topic_runner: TopicRunner | DocumentTopicsInterface = (
            self._config_model.topic_runner) # TODO: fix unsafe cast
        topics_amount = topic_runner.get_n_topics()

        for document_id, document in enumerate(processed_files):
            document_topic = (
                topic_runner.get_document_topics(document.body.body, 0.0))

            if len(document_topic) != topics_amount:
                print(f"Document {document_id} has {len(document_topic)} topics ")

            document.topic_correspondence = [0.0] * topics_amount

            # Add edges from each document to all associated topics
            for (topic_id, topic_probability) in document_topic:
                document.topic_correspondence[topic_id] = topic_probability

        self._calculate_document_topics_event.publish(
            processed_files)

    def _train_lda(self) -> None:
        """
        Retrieves the corpus and model parameters,
        then runs the LDA model on the corpus and saves the topic runner.
        :return: None
        """
        corpus = [document.body.body
                  for document
                  in self._corpus_controller.get_processed_corpus()]
        num_topics = self._model_parameters_controller.get_model_n_topics()
        alpha_value = self._model_parameters_controller.get_model_alpha()
        beta_value = self._model_parameters_controller.get_model_beta()
        alpha_beta_custom_enabled = (
            self._model_parameters_controller.
            get_model_alpha_beta_custom_enabled())

        if alpha_beta_custom_enabled:
            self._config_model.topic_runner = LdaRunner(
                topic_model=self._topic_model,
                docs=corpus,
                num_topics=num_topics,
                alpha=alpha_value,
                beta=beta_value)
            return

        self._config_model.topic_runner = LdaRunner(
            topic_model=self._topic_model,
            docs=corpus,
            num_topics=num_topics)

    def _train_nmf(self) -> None:
        """
        Retrieves the corpus and model parameters,
        then runs the NMF model on the corpus and saves the topic runner.
        :return: None
        """
        corpus = [document.body.body
                  for document
                  in self._corpus_controller.get_processed_corpus()]
        num_topics = self._model_parameters_controller.get_model_n_topics()

        self._config_model.topic_runner = NmfRunner(
                topic_model=self._topic_model,
                docs=corpus,
                num_topics=num_topics)


"""        
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
