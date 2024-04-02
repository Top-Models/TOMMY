import pytest
from tommy.model.stopwords_model import StopwordsModel
from tommy.controller.preprocessing_controller import PreprocessingController


@pytest.fixture
def preprocessing_controller():
    return PreprocessingController()


@pytest.fixture
def stopwords_model():
    return StopwordsModel()


def test_process_text(preprocessing_controller, stopwords_model):
    """
        Test the process_text method of PreprocessingController.
    """
    preprocessing_controller.set_model_refs(stopwords_model)
    text = "Dit is een test zin token2."
    tokens = preprocessing_controller.process_text(text)
    assert isinstance(tokens, list)
    assert len(tokens) == 2  # Check the expected number of tokens
    assert all(isinstance(token, str) for token in
               tokens)  # Ensure all tokens are strings
    assert "test" in tokens  # Check if specific tokens are present
    assert "token2" in tokens


def test_process_tokens(preprocessing_controller, stopwords_model):
    """
        Test the process_tokens method of PreprocessingController.
    """
    preprocessing_controller.set_model_refs(stopwords_model)
    text = "Dit is een test zin token2."
    doc = preprocessing_controller._nlp(text)
    tokens = preprocessing_controller.process_tokens(doc)
    assert isinstance(tokens, list)
    assert len(
        tokens) == 2  # Check the expected number of tokens after processing
    assert all(isinstance(token, str) for token in
               tokens)  # Ensure all tokens are strings
    assert "test" in tokens  # Check if specific tokens are present


def test_filter_stopwords(preprocessing_controller, stopwords_model):
    """
       Test the filter_stopwords method of PreprocessingController.
    """
    preprocessing_controller.set_model_refs(stopwords_model)
    tokens = ["dit", "is", "een", "test", "zin"]
    filtered_tokens = preprocessing_controller.filter_stopwords(tokens)
    assert isinstance(filtered_tokens, list)
    assert len(
        filtered_tokens) == 3  # Check the expected number of tokens after filtering
    assert all(isinstance(token, str) for token in
               filtered_tokens)  # Ensure all tokens are strings
    assert "dit" not in filtered_tokens  # Check if specific stopwords are removed


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
