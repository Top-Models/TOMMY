import pytest
from gensim import models
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.model.topic_model import TopicModel
from tommy.controller.visualizations import correlation_matrix_creator


@pytest.fixture
def gensim_lda_model():
    model = models.LdaModel.load('../../test_data/test_lda_model/lda_model')
    return model

def test_generate_plots(gensim_lda_model):
    assert gensim_lda_model.print_topics()