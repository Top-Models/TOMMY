from interactive_topic_modeling.model.model import Model


class Controller:
    def __init__(self):
        self.model = Model()

    def set_model(self, model: Model):
        self.model = model

    def on_run_topic_modelling(self):
        # TODO: call pre-processing and Gensim
        pass

    def on_input_folder_selected(self, input_folder):
        # TODO: store input folder in model
        pass
