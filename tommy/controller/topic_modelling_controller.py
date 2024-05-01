from tommy.controller.model_parameters_controller import (
    ModelParametersController,
    ModelType)
from tommy.controller.corpus_controller import CorpusController

from tommy.model.topic_model import TopicModel

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.support.event_handler import EventHandler


class TopicModellingController:
    """
    Controller that runs the selected topic modelling algorithm on a call of
    train_model and supplies a topic runner object from which results can be
    extracted.
    """
    _model_parameters_controller: ModelParametersController = None
    _topic_model: TopicModel = None
    _corpus_controller: CorpusController = None
    _topic_runner: TopicRunner = None
    _model_trained_event: EventHandler[TopicRunner] = None

    @property
    def model_trained_event(self) -> EventHandler[TopicRunner]:
        return self._model_trained_event

    def __init__(self) -> None:
        """Initialize the publisher of the topic-modelling-controller"""
        super().__init__()
        self._model_trained_event = EventHandler[TopicRunner]()

    def set_model_refs(self, parameters_controller: ModelParametersController,
                       topic_model: TopicModel,
                       corpus_controller: CorpusController) -> None:
        """
        Set the references to the parameters controller, topic model and
        corpus controller.
        :return: None
        """
        self._model_parameters_controller = parameters_controller
        self._topic_model = topic_model
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
            case _:
                raise NotImplementedError(
                    f"model type {new_model_type.name} is not supported by "
                    f"topic modelling controller")

        self._model_trained_event.publish(self._topic_runner)

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
        self._topic_runner = LdaRunner(topic_model=self._topic_model,
                                       docs=corpus,
                                       num_topics=num_topics)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
