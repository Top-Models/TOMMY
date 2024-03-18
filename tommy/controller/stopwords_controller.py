from tommy.model.stopwords_model import StopWordsModel


class StopwordsController:
    stopwords_model: StopWordsModel = None

    @staticmethod
    def set_stopwords_model(stopwords_model: StopWordsModel):
        StopwordsController.stopwords_model = stopwords_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
