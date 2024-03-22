from tommy.model.model import Model
from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.controller.graph_controller import GraphController
from tommy.controller.topic_modelling_controller import TopicModellingController
from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.preprocessing_controller import PreprocessingController
from tommy.controller.corpus_controller import CorpusController
from tommy.controller.project_settings_controller import \
    ProjectSettingsController
from tommy.controller.save_controller import SaveController


class Controller:
    _models: [Model] = []
    _selected_model: int = -1

    @staticmethod
    def select_model(model_index: int):
        # TODO: input validation
        Controller._selected_model = model_index

    @staticmethod
    def new_model():
        # TODO: doc-strings
        new_model = Model()
        Controller._models.append(new_model)
        Controller._selected_model = len(Controller._models) - 1

        # set references in sub-controller to sub-models
        ModelParametersController.set_model_parameters_model(
            new_model.model_parameters_model)

        GraphController.set_model_parameters_model(
            new_model.model_parameters_model)

        TopicModellingController.set_model_parameters_model(
            new_model.model_parameters_model)
        TopicModellingController.set_topic_model(new_model.topic_model)

        StopwordsController.set_stopwords_model(new_model.stopwords_model)

        PreprocessingController.set_stopwords_model(new_model.stopwords_model)

        CorpusController.set_corpus_model(new_model.corpus_model)
        CorpusController.set_project_settings_model(
            new_model.project_settings_model)

        ProjectSettingsController.set_project_settings_model(
            new_model.project_settings_model)

        SaveController.set_model(new_model)

    @staticmethod
    def on_run_topic_modelling():
        # TODO: call pre-processing and Gensim
        pass

    @staticmethod
    def on_input_folder_selected(input_folder):
        # TODO: store input folder in model
        pass
