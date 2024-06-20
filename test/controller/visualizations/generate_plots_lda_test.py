import os
import pytest
import pickle

from gensim import models, corpora

from tommy.model.topic_model import TopicModel
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner

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
from tommy.controller.visualizations.k_value_creator import KValueCreator
from tommy.controller.visualizations.documents_over_time_creator import (
    DocumentsOverTimeCreator)
from tommy.controller.visualizations.documents_over_time_per_topic_creator \
    import DocumentsOverTimePerTopicCreator
from tommy.controller.visualizations.sum_topics_in_documents import (
    SumTopicsInDocuments)


# Test data directory
TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             '..',
                                             '..',
                                             'test',
                                             'test_data'))


@pytest.fixture
def lda_model():
    # Load saved lda model which has 4 topics
    path = os.path.join(TEST_DATA_DIR, 'test_lda_model', 'lda_model')
    model = models.LdaModel.load(path)
    return model


@pytest.fixture
def lda_model_dictionary():
    # Load id2word file of saved lda model
    path = os.path.join(TEST_DATA_DIR, 'test_lda_model', 'lda_model.id2word')
    dictionary = (corpora.Dictionary.load(path))
    return dictionary


@pytest.fixture
def processed_files():
    # Load saved processed files
    path = os.path.join(TEST_DATA_DIR,
                        'test_processed_files',
                        'processed_files.pkl')
    with open(path, 'rb') as file:
        processed_files = pickle.load(file)
        return processed_files


@pytest.fixture
def lda_runner(lda_model, lda_model_dictionary, processed_files, mocker):
    topic_model = TopicModel()

    # Mock LdaRunner functions
    mocker.patch.object(LdaRunner, 'train_model')
    mocker.patch.object(LdaRunner, 'get_n_topics', return_value=4)

    # Construct a mocked instance of LdaRunner
    lda_runner = LdaRunner(topic_model, [], 0, 0)
    lda_runner._model = lda_model
    lda_runner._dictionary = lda_model_dictionary
    docs = [document.body.body for document in processed_files]
    lda_runner._bags_of_words = [lda_model_dictionary.doc2bow(tokens)
                                 for tokens in docs]
    return lda_runner


@pytest.fixture
def metadata(processed_files):
    # Extract metadata from processed_files
    metadata = [processed_file.metadata for processed_file in processed_files]
    return metadata


def test_generate_correlation_matrix(lda_runner):
    correlation_matrix = CorrelationMatrixCreator()
    figure = correlation_matrix._create_figure(lda_runner)
    assert figure


def test_generate_document_word_count(lda_runner, metadata):
    document_word_count = DocumentWordCountCreator()
    figure = document_word_count._create_figure(lda_runner, metadata)
    assert figure


@pytest.mark.parametrize("topic_id", [0, 1, 2, 3])
def test_generate_top_words_bar_plot(lda_runner, topic_id):
    top_words_bar_plot = TopWordsBarPlotCreator()
    figure = top_words_bar_plot._create_figure(lda_runner, topic_id)
    assert figure


@pytest.mark.parametrize("topic_id", [0, 1, 2, 3])
def test_generate_word_cloud(lda_runner, topic_id):
    word_cloud_creator = WordCloudCreator()
    figure = word_cloud_creator._create_figure(lda_runner, topic_id)
    assert figure


def test_generate_word_topic_network(lda_runner):
    word_topic_network = WordTopicNetworkCreator()
    figure = word_topic_network._create_figure(lda_runner)
    assert figure


def test_generate_document_topic_network_summary(lda_runner, processed_files):
    doc_topic_summary = DocumentTopicNetworkSummaryCreator()
    figure = doc_topic_summary._create_figure(lda_runner, processed_files)
    assert figure


def test_generate_k_value_plot(lda_runner):
    k_value_plot = KValueCreator()
    figure = k_value_plot._create_figure(lda_runner)
    assert figure


def test_generate_documents_over_time_plot(lda_runner, processed_files):
    documents_over_time_plot = DocumentsOverTimeCreator()
    figure = documents_over_time_plot._create_figure(lda_runner,
                                                     processed_files)
    assert figure


@pytest.mark.parametrize("topic_id", [0, 1, 2, 3])
def test_generate_documents_over_time_per_topic_plot(lda_runner,
                                                     processed_files,
                                                     topic_id):
    documents_over_time_per_topic_plot = DocumentsOverTimePerTopicCreator()
    figure = documents_over_time_per_topic_plot._create_figure(lda_runner,
                                                               topic_id,
                                                               processed_files)
    assert figure


def test_generate_sum_topics_in_documents_plot(lda_runner, processed_files):
    sum_topics_in_documents_plot = SumTopicsInDocuments()
    figure = sum_topics_in_documents_plot._create_figure(lda_runner,
                                                         processed_files)
    assert figure


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
