import pytest
from tommy.controller.stopwords_controller import StopwordsModel


@pytest.fixture
def stopwords():
    """
    Fixture to create a StopWords object with predefined stop words.
    """
    return StopwordsModel()


def test_stopwords_initialization(stopwords):
    """
    Test StopWords initialization and basic functionality.
    """
    assert "af" in stopwords
    assert "al" in stopwords
    assert "als" in stopwords
    assert len(stopwords) == 352


def test_stopwords_contains(stopwords):
    """
    Test containment check for stop words.
    """
    assert "al" in stopwords
    assert "hahahapoep" not in stopwords


def test_stopwords_iteration(stopwords):
    """
    Test iteration over stop words.
    """
    for word in stopwords:
        assert word in stopwords


def test_stopwords_add_single_word(stopwords):
    """
    Test adding a single word to stop words.
    """
    stopwords.add("hoimam")
    assert "hoimam" in stopwords
    assert len(stopwords) == 374


def test_stopwords_add_multiple_words(stopwords):
    """
    Test adding multiple words to stop words.
    """
    stopwords.add("hoimam", "hoipap", "hoibroer")
    assert "hoimam" in stopwords
    assert "hoipap" in stopwords
    assert "hoibroer" in stopwords
    assert len(stopwords) == 355


def test_stopwords_add_list(stopwords):
    """
    Test adding a list of words to stop words.
    """
    stopwords.add(["hoimam", "hoipap", "hoibroer"])
    assert "hoimam" in stopwords
    assert "hoipap" in stopwords
    assert "hoibroer" in stopwords
    assert len(stopwords) == 355


def test_stopwords_remove_single_word(stopwords):
    """
    Test removing a single word from stop words.
    """
    stopwords.remove("al")
    assert "al" not in stopwords
    assert len(stopwords) == 372


def test_stopwords_remove_multiple_words(stopwords):
    """
    Test removing multiple words from stop words.
    """
    stopwords.remove('al', 'als')
    assert "al" not in stopwords
    assert "als" not in stopwords
    assert len(stopwords) == 371


def test_stopwords_remove_list(stopwords):
    """
    Test removing a list of words from stop words.
    """
    stopwords.remove(["al", "als"])
    assert "al" not in stopwords
    assert "als" not in stopwords
    assert len(stopwords) == 350


#def test_stopwords_add_invalid_argument_type(stopwords):
#    """
#    Test adding an invalid argument type to stop words.
#    """
#    with pytest.raises(TypeError):
#        stopwords.add(123)


#def test_stopwords_remove_invalid_argument_type(stopwords):
#    """
#    Test removing an invalid argument type to stop words.
#    """
#    with pytest.raises(TypeError):
#        stopwords.remove(123)