import pytest
from gensim import models

import tommy.controller.visualizations.visualization_input_datatypes

from tommy.model.topic_model import TopicModel
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.controller.file_import.metadata import Metadata

from tommy.controller.visualizations.correlation_matrix_creator import (
    CorrelationMatrixCreator)
from tommy.controller.visualizations.document_word_count_creator import (
    DocumentWordCountCreator)
from tommy.controller.visualizations.top_words_bar_plot_creator import (
    TopWordsBarPlotCreator)
from tommy.controller.visualizations.word_cloud_creator import (
    WordCloudCreator)
from tommy.controller.visualizations.word_topic_network_creator import \
    WordTopicNetworkCreator


@pytest.fixture
def lda_model():
    # Load lda model which has 4 topics
    model = models.LdaModel.load('../../test_data/test_lda_model/lda_model')
    return model


@pytest.fixture
def lda_runner(lda_model, mocker):
    topic_model = TopicModel()
    mocker.patch.object(LdaRunner, 'train_model')
    lda_runner = LdaRunner(topic_model, [], 0, 0)
    lda_runner._model = lda_model
    return lda_runner


def test_generate_correlation_matrix(lda_runner):
    correlation_matrix = CorrelationMatrixCreator()
    figure = correlation_matrix.get_figure(lda_runner)
    assert figure


# def test_generate_document_word_count(lda_runner):
#     document_word_count = DocumentWordCountCreator()
#     # enkel lijst met Metadata nodig en Metadata.length moet aangemaakt zijn


@pytest.mark.parametrize("topic_id", [0, 1, 2, 3])
def test_generate_top_words_bar_plot(lda_runner, topic_id):
    top_words_bar_plot = TopWordsBarPlotCreator()
    figure = top_words_bar_plot.get_figure(lda_runner, topic_id)
    assert figure


@pytest.mark.parametrize("topic_id", [0, 1, 2, 3])
def test_generate_word_cloud(lda_runner, topic_id):
    word_cloud_creator = WordCloudCreator()
    figure = word_cloud_creator.get_figure(lda_runner, topic_id)
    assert figure


def test_generate_word_topic_network(lda_runner):
    word_topic_network = WordTopicNetworkCreator()
    figure = word_topic_network.get_figure(lda_runner)
    assert figure


# def test_generate_document_topic_network_summary(lda_runner, processed_corpus):
#     # enkel processed corpus nodig!
