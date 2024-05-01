from tommy.model.config_model import ConfigModel
from tommy.model.model import Model

from tommy.controller.file_import.processed_body import ProcessedBody
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.controller.graph_controller import GraphController
from tommy.controller.topic_modelling_controller import (
    TopicModellingController)
from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.preprocessing_controller import PreprocessingController
from tommy.controller.corpus_controller import CorpusController
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
from tommy.controller.save_controller import SaveController
from tommy.controller.config_controller import ConfigController


class Controller:
    """The main controller for the tommy that creates all sub-controllers"""
    _model: Model

    _model_parameters_controller: ModelParametersController

    @property
    def model_parameters_controller(self) -> ModelParametersController:
        return self._model_parameters_controller

    _graph_controller: GraphController

    @property
    def graph_controller(self) -> GraphController:
        return self._graph_controller

    _topic_modelling_controller: TopicModellingController
    _stopwords_controller: StopwordsController

    @property
    def stopwords_controller(self) -> StopwordsController:
        return self._stopwords_controller

    _preprocessing_controller: PreprocessingController
    _corpus_controller: CorpusController

    @property
    def corpus_controller(self) -> CorpusController:
        return self._corpus_controller

    @property
    def project_settings_controller(self) -> ProjectSettingsController:
        return self._project_settings_controller

    _project_settings_controller: ProjectSettingsController
    _save_controller: SaveController

    @property
    def config_controller(self) -> ConfigController:
        return self._config_controller

    def __init__(self) -> None:
        """Initialize the main controller and its sub-controllers."""
        self._initialize_components()

        self._model = Model()
        self._set_model_references()

    def _initialize_components(self):
        """Initialize all sub-components"""
        self._model_parameters_controller = ModelParametersController()
        self._graph_controller = GraphController()
        self._topic_modelling_controller = TopicModellingController()
        self._stopwords_controller = StopwordsController()
        self._preprocessing_controller = PreprocessingController()
        self._corpus_controller = CorpusController()
        self._project_settings_controller = ProjectSettingsController()
        self._save_controller = SaveController()
        self._config_controller = ConfigController()

    def _set_controller_references(self) -> None:
        """
        Some controllers need references to other controllers, for example
        to subscribe to events. This method gives each controller a
        reference to the other controllers which it needs
        :return: None
        """
        self._corpus_controller.set_controller_refs(
            self._project_settings_controller)

        self._graph_controller.set_controller_refs(
            self._topic_modelling_controller, self._corpus_controller)

        self._topic_modelling_controller.set_controller_refs(
            self._model_parameters_controller, self._corpus_controller)

        self._config_controller.config_switched_event.subscribe(
            self.update_config_model_references)

    def _set_model_references(self) -> None:
        """
        Give each controller the correct references to the model
        :return: None
        """
        self._project_settings_controller.set_model_refs(
            self._model.project_settings_model)

        self._config_controller.set_model_refs(
            self._model)

        self.update_config_model_references(self._model.config_model)

    def on_run_topic_modelling(self) -> None:
        """
        Run the topic modelling algorithm on the currently selected corpus
        and using the current model parameters
        :return: None
        """
        raw_files = self._corpus_controller.get_raw_files()

        # todo: move running the preprocessing to corpus_controller
        processed_files = [ProcessedFile(doc.metadata, ProcessedBody(
            self._preprocessing_controller.process_text(doc.body.body))) for
                           doc in raw_files]

        self._corpus_controller.set_processed_corpus(processed_files)
        self._topic_modelling_controller.train_model()

    def update_config_model_references(self, config_model: ConfigModel):
        self._model_parameters_controller.set_model_refs(
            config_model.model_parameters_model)

        self._topic_modelling_controller.set_model_refs(
            config_model.topic_model)

        self._stopwords_controller.set_model_refs(
            config_model.stopwords_model)

        self._preprocessing_controller.set_model_refs(
            config_model.stopwords_model)

        self._corpus_controller.set_model_refs(
            config_model.corpus_model)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
