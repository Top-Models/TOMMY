import pytest
from PySide6.QtCore import Qt

from tommy.controller.file_import.processed_body import ProcessedBody
from tommy.controller.file_import.processed_corpus import ProcessedCorpus
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.model.topic_model import TopicModel


@pytest.fixture
def gensim_lda_model():
    # Prepare sample term lists and other required parameters
    term_lists = [["word1", "word2", "word3"], ["word4", "word5", "word6"]]
    processed_corpus = ProcessedCorpus()
    processed_corpus.documents = [
        ProcessedFile(None, ProcessedBody(words)) for words in term_lists]

    num_topics = 2
    mock_topic_model = TopicModel()
    # Instantiate the model
    model = LdaRunner(topic_model=mock_topic_model,
                      processed_corpus=processed_corpus,
                      current_corpus_version_id=0,
                      num_topics=num_topics)

    return model


def test_train_model(gensim_lda_model):
    # Assert that the model has been trained and has the correct n. of topics
    assert gensim_lda_model.get_n_topics() == 2
    assert hasattr(gensim_lda_model, "get_topic_with_scores")
    assert hasattr(gensim_lda_model, "get_topics_with_scores")


if __name__ == '__main__':
    pytest.main()

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
