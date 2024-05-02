import pytest
from gensim import models

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.controller.visualizations.correlation_matrix_creator import (
    CorrelationMatrixCreator)
from tommy.model.topic_model import TopicModel


@pytest.fixture
def gensim_lda_model():
    model = models.LdaModel.load('../../test_data/test_lda_model/lda_model')
    return model

@pytest.fixture
def lda_runner(gensim_lda_model, mocker):
    topic_model = TopicModel()
    mocker.patch.object(LdaRunner, 'train_model')
    lda_runner = LdaRunner(topic_model, [], 0, 0)
    lda_runner._model = gensim_lda_model
    return lda_runner


def test_generate_correlation_matrix(gensim_lda_model, lda_runner):
    correlation_matrix = CorrelationMatrixCreator()
    figure = correlation_matrix.get_figure(lda_runner)
    #figure.show()
    assert figure
