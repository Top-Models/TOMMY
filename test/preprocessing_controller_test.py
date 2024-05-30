import pytest
import spacy.tokens

from tommy.controller.controller import Controller
from tommy.controller.language_controller import LanguageController
from tommy.controller.stopwords_controller import StopwordsController
from tommy.model.language_model import LanguageModel
from tommy.model.stopwords_model import StopwordsModel
from tommy.controller.preprocessing_controller import PreprocessingController
from tommy.support.supported_languages import SupportedLanguage


@pytest.fixture
def preprocessing_controller_dutch():
    controller = PreprocessingController()
    controller.load_pipeline(SupportedLanguage.Dutch)
    return controller


@pytest.fixture
def preprocessing_controller_english():
    controller = PreprocessingController()
    controller.load_pipeline(SupportedLanguage.English)
    return controller


@pytest.fixture
def stopwords_model_dutch():
    stopwords_controller = StopwordsController()
    stopwords_controller.set_model_refs(StopwordsModel())
    stopwords_controller.load_default_stopwords(SupportedLanguage.Dutch)
    return stopwords_controller.stopwords_model


@pytest.fixture
def stopwords_model_english():
    stopwords_controller = StopwordsController()
    stopwords_controller.set_model_refs(StopwordsModel())
    stopwords_controller.load_default_stopwords(SupportedLanguage.English)
    return stopwords_controller.stopwords_model


def test_process_text_dutch(preprocessing_controller_dutch,
                            stopwords_model_dutch):
    """
    Test the process_text method of PreprocessingController.
    """
    preprocessing_controller_dutch.set_model_refs(stopwords_model_dutch)
    text = "Dit is een test zin token2."
    tokens = preprocessing_controller_dutch.process_text(text)
    assert isinstance(tokens, list)
    # Check the expected number of tokens
    assert len(tokens) == 2

    # Ensure all tokens are strings
    assert all(isinstance(token, str) for token in
               tokens)

    # Check if specific tokens are present
    assert "test" in tokens
    assert "token2" in tokens


def test_process_text_english(preprocessing_controller_english,
                              stopwords_model_english):
    """
    Test the process_text method of PreprocessingController.
    """
    preprocessing_controller_english.load_pipeline(
        SupportedLanguage.English)
    preprocessing_controller_english.set_model_refs(stopwords_model_english)
    text = "This is a test sentence token2."
    tokens = preprocessing_controller_english.process_text(text)
    assert isinstance(tokens, list)
    # Check the expected number of tokens
    assert len(tokens) == 3

    # Ensure all tokens are strings
    assert all(isinstance(token, str) for token in
               tokens)

    # Check if specific tokens are present
    assert "test" in tokens
    assert "token2" in tokens


def test_process_tokens(preprocessing_controller_dutch, stopwords_model_dutch):
    """
    Test the process_tokens method of PreprocessingController.
    """
    preprocessing_controller_dutch.set_model_refs(stopwords_model_dutch)
    text = "Dit is een test zin token2."
    doc = preprocessing_controller_dutch._nlp(text)
    tokens = preprocessing_controller_dutch.process_tokens(doc)
    assert isinstance(tokens, list)

    # Check the expected number of tokens after processing
    assert len(
        tokens) == 2

    # Ensure all tokens are strings
    assert all(isinstance(token, str) for token in
               tokens)

    # Check if specific tokens are present
    assert "test" in tokens


def test_filter_stopwords(preprocessing_controller_dutch,
                          stopwords_model_dutch):
    """
    Test the filter_stopwords method of PreprocessingController.
    """
    preprocessing_controller_dutch.set_model_refs(stopwords_model_dutch)
    tokens = ["dit", "is", "een", "test", "zin"]
    filtered_tokens = preprocessing_controller_dutch.filter_stopwords(tokens)
    assert isinstance(filtered_tokens, list)

    # Check the expected number of tokens after filtering
    assert len(
        filtered_tokens) == 3

    # Ensure all tokens are strings
    assert all(isinstance(token, str) for token in
               filtered_tokens)

    # Check if specific stopwords are removed
    assert "dit" not in filtered_tokens


def test_n_gram_merging(preprocessing_controller_dutch,
                        stopwords_model_dutch):
    """
    Test the n_gram_merging method of PreprocessingController.
    """
    preprocessing_controller_dutch.set_model_refs(stopwords_model_dutch)
    tokens = "Hello Kitty is beter dan Ben Ten"
    n_grams = preprocessing_controller_dutch._nlp(tokens)
    assert isinstance(n_grams, spacy.tokens.Doc)

    # Check whether the n_grams are merged
    assert len(n_grams) == 5

    # Check if specific n_grams are present
    assert "Hello Kitty" in [token.text for token in n_grams]
    assert "Ben Ten" in [token.text for token in n_grams]


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
