import os
from itertools import chain
from functools import reduce

from unittest.mock import MagicMock
import pytest
import pickle

from tommy.controller.language_controller import LanguageController
from tommy.controller.preprocessing_controller import PreprocessingController
from tommy.model.language_model import LanguageModel
from tommy.model.topic_model import TopicModel
from tommy.controller.topic_modelling_runners.bertopic_runner import (
    BertopicRunner)
from tommy.controller.stopwords_controller import StopwordsController

from tommy.controller.visualizations.correlation_matrix_creator import (
    CorrelationMatrixCreator)
from tommy.controller.visualizations.document_word_count_creator import (
    DocumentWordCountCreator)
from tommy.controller.visualizations.top_words_bar_plot_creator import (
    TopWordsBarPlotCreator)
from tommy.controller.visualizations.word_cloud_creator import (
    WordCloudCreator)
from tommy.controller.visualizations.word_topic_network_creator import (
    WordTopicNetworkCreator)
from tommy.controller.visualizations.document_topic_network_summary_creator \
    import DocumentTopicNetworkSummaryCreator
from tommy.support.supported_languages import SupportedLanguage

# Test data directory
TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             '..',
                                             '..',
                                             'test',
                                             'test_data',
                                             'test_bert_input'))


@pytest.fixture(scope="module")
def raw_bodies():
    # Load saved raw file bodies
    path = os.path.join(TEST_DATA_DIR,
                        'raw_bodies.pkl')
    with open(path, 'rb') as file:
        raw_bodies = pickle.load(file)
        return raw_bodies


@pytest.fixture(scope="module")
def metadata():
    # Load saved metadata
    path = os.path.join(TEST_DATA_DIR,
                        'metadata.pkl')
    with open(path, 'rb') as file:
        metadata = pickle.load(file)
        return metadata


@pytest.fixture(scope="module")
def num_words():
    return 6


@pytest.fixture(scope="module")
def max_num_topics():
    return 2


@pytest.fixture(scope="module")
def language_controller_dutch():
    language_controller = MagicMock()
    language_controller.get_language.return_value = SupportedLanguage.Dutch
    return language_controller


@pytest.fixture(scope="module")
def preprocessing_controller_dutch(language_controller_dutch):
    controller = PreprocessingController()
    controller.set_controller_refs(language_controller_dutch)
    return controller


@pytest.fixture(scope="module")
def bertopic_runner(raw_bodies, num_words, max_num_topics,
                    preprocessing_controller_dutch):
    mock_stopwords_controller = MagicMock()
    mock_stopwords_controller.stopwords_model.return_value = ["de",
                                                              "het",
                                                              "een",
                                                              "stopword4",
                                                              "stopword5"]

    mock_topic_model = MagicMock()

    lists_of_sentences = map(
        preprocessing_controller_dutch.split_into_sentences,
        raw_bodies)
    sentences = list(reduce(chain, lists_of_sentences))

    bert = BertopicRunner(mock_topic_model, mock_stopwords_controller, 0,
                          max_num_topics, num_words, raw_bodies, sentences,
                          0.1, 10_000)

    return bert


@pytest.fixture(scope="module")
def actual_n_topics(bertopic_runner):
    return bertopic_runner.get_n_topics()


def test_generate_document_word_count(bertopic_runner, metadata):
    document_word_count = DocumentWordCountCreator()
    figure = document_word_count._create_figure(bertopic_runner, metadata)
    assert figure


def test_generate_top_words_bar_plot(bertopic_runner, actual_n_topics):
    for topic_id in range(actual_n_topics):
        top_words_bar_plot = TopWordsBarPlotCreator()
        figure = top_words_bar_plot._create_figure(bertopic_runner, topic_id)
        assert figure


def test_generate_word_cloud(bertopic_runner, actual_n_topics):
    for topic_id in range(actual_n_topics):
        word_cloud_creator = WordCloudCreator()
        figure = word_cloud_creator._create_figure(bertopic_runner, topic_id)
        assert figure


def test_generate_word_topic_network(bertopic_runner):
    word_topic_network = WordTopicNetworkCreator()
    figure = word_topic_network._create_figure(bertopic_runner)
    assert figure


def test_get_topic_words(bertopic_runner, max_num_topics, num_words):
    assert max_num_topics >= bertopic_runner.get_n_topics()
    assert num_words == bertopic_runner.num_words_per_topic

    for n in range(bertopic_runner.get_n_topics()):
        assert (bertopic_runner.get_topic_with_scores(n, num_words).n_words
                == num_words)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
