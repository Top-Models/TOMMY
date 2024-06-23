from tommy.controller.saving_loading_controller import SavingLoadingController
from tommy.model.config_model import ConfigModel
from tommy.model.model import Model

from tommy.controller.file_import.processed_body import ProcessedBody
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.controller.graph_controller import GraphController
from tommy.controller.topic_modelling_controller import (
    TopicModellingController)
from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.synonyms_controller import SynonymsController
from tommy.controller.preprocessing_controller import PreprocessingController
from tommy.controller.corpus_controller import CorpusController
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
from tommy.controller.config_controller import ConfigController
from tommy.controller.export_controller import ExportController
from tommy.controller.language_controller import LanguageController


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
    _synonyms_controller: SynonymsController

    @property
    def stopwords_controller(self) -> StopwordsController:
        return self._stopwords_controller

    @property
    def synonyms_controller(self) -> SynonymsController:
        return self._synonyms_controller

    _preprocessing_controller: PreprocessingController
    _corpus_controller: CorpusController

    @property
    def corpus_controller(self) -> CorpusController:
        return self._corpus_controller

    @property
    def topic_modelling_controller(self) -> TopicModellingController:
        return self._topic_modelling_controller

    @property
    def project_settings_controller(self) -> ProjectSettingsController:
        return self._project_settings_controller

    @property
    def language_controller(self) -> LanguageController:
        return self._language_controller

    _project_settings_controller: ProjectSettingsController
    _saving_loading_controller: SavingLoadingController

    _export_controller: ExportController
    _language_controller: LanguageController

    @property
    def export_controller(self) -> ExportController:
        return self._export_controller

    @property
    def config_controller(self) -> ConfigController:
        return self._config_controller

    @property
    def saving_loading_controller(self):
        return self._saving_loading_controller

    def __init__(self) -> None:
        """Initialize the main controller and its sub-controllers."""
        self._initialize_components()

        self._model = Model()
        self._set_model_references()
        self._set_controller_references()

    def _initialize_components(self):
        """
        Initialize all sub-controllers
        :return: None
        """
        self._model_parameters_controller = ModelParametersController()
        self._language_controller = LanguageController()
        self._graph_controller = GraphController()
        self._topic_modelling_controller = TopicModellingController()
        self._stopwords_controller = StopwordsController()
        self._synonyms_controller = SynonymsController()
        self._preprocessing_controller = PreprocessingController()
        self._corpus_controller = CorpusController()
        self._project_settings_controller = ProjectSettingsController()
        self._saving_loading_controller = SavingLoadingController()
        self._config_controller = ConfigController()
        self._export_controller = ExportController()

    def _set_controller_references(self) -> None:
        """
        Some controllers need references to other controllers, for example
        to subscribe to events. This method gives each controller a
        reference to the other controllers which it needs
        :return: None
        """
        self._corpus_controller.set_controller_refs(
            self._project_settings_controller,
            self._preprocessing_controller)
        self._export_controller.set_controller_refs(
            self._graph_controller,
            self._topic_modelling_controller)

        self._graph_controller.set_controller_refs(
            self._topic_modelling_controller, self._corpus_controller,
            self.project_settings_controller)

        self._topic_modelling_controller.set_controller_refs(
            self._model_parameters_controller, self._corpus_controller,
            self._stopwords_controller, self._synonyms_controller,
            self._preprocessing_controller)

        self._preprocessing_controller.set_controller_refs(
            self.language_controller)

        self._stopwords_controller.set_controller_refs(
            self.language_controller)

        self._config_controller.set_controller_refs(self._graph_controller)

        # subscribe methods of Controller to events from sub-controllers
        self._config_controller.config_switched_event.subscribe(
            self._update_model_on_config_switch)
        self._saving_loading_controller.model_changed_event.subscribe(
            self._update_model_on_load)

    def _set_model_references(self) -> None:
        """
        Give each controller the correct references to each model
        :return: None
        """
        self._project_settings_controller.set_model_refs(
            self._model.project_settings_model)

        self._config_controller.set_model_refs(
            self._model)

        self._model_parameters_controller.set_model_refs(
            self._model.model_parameters_model)

        self._topic_modelling_controller.set_model_refs(
            self._model.topic_model,
            self._model.config_model)

        self._stopwords_controller.set_model_refs(
            self._model.stopwords_model)

        self._synonyms_controller.set_model_refs(
            self._model.synonyms_model)

        self._preprocessing_controller.set_model_refs(
            self._model.stopwords_model,
            self._model.synonyms_model)

        self._corpus_controller.set_model_refs(
            self._model.corpus_model)

        self._project_settings_controller.set_model_refs(
            self._model.project_settings_model)

        self._language_controller.set_model_refs(
            self._model.language_model)

        self._saving_loading_controller.set_model_refs(
            self._model)

        self._graph_controller.set_model_refs(self._model.topic_name_model)

    def _update_model_on_config_switch(
            self, data: ConfigModel) -> None:
        """
        When the user switches configuration, this event handler makes sure
        that every controller gets a reference to the models of the currently
        selected config. It then asks the controllers to notify the frontend
        components of the new model.
        :param data: unused parameter, since the selected config
        model can be accessed using the model
        :return: None
        """
        self._set_model_references()
        self._notify_model_swapped()

    def _update_model_on_load(self, model: Model) -> None:
        """
        Update the model of the controller, update the references for the
        other controllers and notify the frontend components of the new model
        :param model: The new model
        :return: None
        """
        self._model = model
        self._set_model_references()

        # load default stopwords for the new language
        new_language = model.language_model.selected_language
        self._language_controller.set_language(new_language)

        # load new input folder path
        new_input_folder_path = model.project_settings_model.input_folder_path
        self._project_settings_controller.set_input_folder_path(
            new_input_folder_path)

        self._notify_model_swapped()

    def _notify_model_swapped(self) -> None:
        """
        When the user switches configuration, this event handler makes
        sure that every controller gets a reference to the models of the
        currently selected config
        :return: None
        """
        self._model_parameters_controller.on_model_swap()
        self._topic_modelling_controller.on_model_swap()
        self._stopwords_controller.on_model_swap()
        self._synonyms_controller.on_model_swap()
        self._language_controller.on_model_swap()
        self._graph_controller.on_model_swap()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
