from tommy.model.stopwords_model import StopwordsModel


class PreprocessingController:
    stopwords_model: StopwordsModel = None

    @staticmethod
    def set_stopwords_model(stopwords_model: StopwordsModel):
        PreprocessingController.stopwords_model = stopwords_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
