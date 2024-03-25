import pytest
from PySide6.QtCore import Qt
from tommy.backend.model.lda_model import GensimLdaModel


@pytest.fixture
def gensim_lda_model():
    # Prepare sample term lists and other required parameters
    term_lists = [["word1", "word2", "word3"], ["word4", "word5", "word6"]]
    num_topics = 2

    # Instantiate the model
    model = GensimLdaModel(term_lists, num_topics)

    return model


def test_train_model(gensim_lda_model):
    # Assert that the model has been trained and has the correct number of topics
    assert gensim_lda_model.num_topics == 2
    assert hasattr(gensim_lda_model, 'dictionary')
    assert hasattr(gensim_lda_model, 'model')
    assert hasattr(gensim_lda_model, 'bags_of_words')


if __name__ == '__main__':
    pytest.main()
