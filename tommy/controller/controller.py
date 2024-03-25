from tommy.model.model import Model

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

from typing import List


class Controller:
    """The main controller for the tommy that creates all sub-controllers"""
    _models: List[Model]
    _selected_model: int

    _model_parameters_controller: ModelParametersController

    @property
    def model_parameters_controller(self) -> ModelParametersController:
        return self._model_parameters_controller

    _graph_controller: GraphController
    _topic_modelling_controller: TopicModellingController
    _stopwords_controller: StopwordsController
    _preprocessing_controller: PreprocessingController
    _corpus_controller: CorpusController

    @property
    def corpus_controller(self) -> CorpusController:
        return self._corpus_controller

    _project_settings_controller: ProjectSettingsController
    _save_controller: SaveController

    def __init__(self):
        self._initialize_components()

        self._models = self._save_controller.get_models()
        self.select_model(0)

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

        self._corpus_controller.set_controller_refs(
            self._project_settings_controller)

    def select_model(self, model_index: int):
        """
        Select a model corresponding to the given index
        :param model_index: The index of the model to be selected
        """
        # TODO: input validation
        self._selected_model = model_index

        self._model_parameters_controller.set_model_refs(
            self._models[model_index].model_parameters_model)

        self._graph_controller.set_model_refs(
            self._models[model_index].model_parameters_model)

        self._topic_modelling_controller.set_model_refs(
            self._models[model_index].model_parameters_model,
            self._models[model_index].topic_model)

        self._stopwords_controller.set_model_refs(
            self._models[model_index].stopwords_model)

        self._preprocessing_controller.set_model_refs(
            self._models[model_index].stopwords_model)

        self._corpus_controller.set_model_refs(
            self._models[model_index].corpus_model)

        self._project_settings_controller.set_model_refs(
            self._models[model_index].project_settings_model)

    def on_run_topic_modelling(self):
        """
        Run the topic modelling algorithm on the currently selected corpus
        and using the current model parameters
        """
        # TODO: call pre-processing and Gensim
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
