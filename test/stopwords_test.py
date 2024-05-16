import pytest

from tommy.controller.stopwords_controller import (StopwordsController,
                                                   StopwordsModel,
                                                   LanguageController,
                                                   SupportedLanguage)
from tommy.model.language_model import LanguageModel


@pytest.fixture
def dutch_stopwords():
    """
    Fixture to create a StopWords object with predefined Dutch stop words.
    """

    language_controller = LanguageController()
    language_controller.set_model_refs(LanguageModel())
    stopwords_controller = StopwordsController(language_controller)
    stopwords_controller.set_model_refs(StopwordsModel())
    stopwords_controller.load_default_stopwords(SupportedLanguage.Dutch)
    return stopwords_controller.stopwords_model


@pytest.fixture
def english_stopwords():
    """
    Fixture to create a StopWords object with predefined English stop words.
    """

    language_controller = LanguageController()
    language_controller.set_model_refs(LanguageModel())
    stopwords_controller = StopwordsController(language_controller)
    stopwords_controller.set_model_refs(StopwordsModel())
    stopwords_controller.load_default_stopwords(SupportedLanguage.English)
    return stopwords_controller.stopwords_model


def test_stopwords_initialization(dutch_stopwords):
    """
    Test StopWords initialization and basic functionality.
    """
    assert "af" in dutch_stopwords
    assert "al" in dutch_stopwords
    assert "als" in dutch_stopwords
    assert len(dutch_stopwords) == 352


def test_stopwords_initialization_english(english_stopwords):
    """
    Test StopWords initialization and basic functionality.
    """
    assert "a" in english_stopwords
    assert "about" in english_stopwords
    assert "above" in english_stopwords
    assert len(english_stopwords) == 127


def test_stopwords_contains(dutch_stopwords):
    """
    Test containment check for stop words.
    """
    assert "al" in dutch_stopwords
    assert "hahahapoep" not in dutch_stopwords


def test_stopwords_contains_english(english_stopwords):
    """
    Test containment check for stop words.
    """
    assert "a" in english_stopwords
    assert "hahahapoep" not in english_stopwords


@pytest.mark.parametrize("stopwords", ["dutch_stopwords", "english_stopwords"])
def test_stopwords_iteration(stopwords, request):
    """
    Test iteration over stop words.
    """
    stopword_list = request.getfixturevalue(stopwords)
    for word in stopword_list:
        assert word in stopword_list


@pytest.mark.parametrize("stopwords", ["dutch_stopwords", "english_stopwords"])
def test_stopwords_add_single_word(stopwords, request):
    """
    Test adding a single word to stop words.
    """
    stopword_list = request.getfixturevalue(stopwords)
    n = len(stopword_list)
    stopword_list.add("hoimam")
    assert "hoimam" in stopword_list
    assert len(stopword_list) == n + 1
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)


@pytest.mark.parametrize("stopwords", ["dutch_stopwords", "english_stopwords"])
def test_stopwords_add_multiple_words(stopwords, request):
    """
    Test adding multiple words to stop words.
    """
    stopword_list = request.getfixturevalue(stopwords)
    n = len(stopword_list)
    stopword_list.add("hoimam", "hoipap", "hoibroer")
    assert "hoimam" in stopword_list
    assert "hoipap" in stopword_list
    assert "hoibroer" in stopword_list
    assert len(stopword_list) == n + 3
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)


@pytest.mark.parametrize("stopwords", ["dutch_stopwords", "english_stopwords"])
def test_stopwords_add_list(stopwords, request):
    """
    Test adding a list of words to stop words.
    """
    stopword_list = request.getfixturevalue(stopwords)
    n = len(stopword_list)
    stopword_list.add(["hoimam", "hoipap", "hoibroer"])
    assert "hoimam" in stopword_list
    assert "hoipap" in stopword_list
    assert "hoibroer" in stopword_list
    assert len(stopword_list) == n + 3
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)


@pytest.mark.parametrize("stopwords", ["dutch_stopwords", "english_stopwords"])
def test_stopwords_remove_single_word(stopwords, request):
    """
    Test removing a single word from stop words.
    """
    stopword_list = request.getfixturevalue(stopwords)
    n = len(stopword_list)
    stopword_list.add("test")
    assert "test" in stopword_list
    assert len(stopword_list) == n + 1
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)
    stopword_list.remove("test")
    assert "test" not in stopword_list
    assert len(stopword_list) == n
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)


@pytest.mark.parametrize("stopwords", ["dutch_stopwords", "english_stopwords"])
def test_stopwords_remove_multiple_words(stopwords, request):
    """
    Test removing multiple words from stop words.
    """
    stopword_list = request.getfixturevalue(stopwords)
    n = len(stopword_list)
    stopword_list.add("hoimam", "hoipap", "hoibroer")
    assert "hoimam" in stopword_list
    assert "hoipap" in stopword_list
    assert "hoibroer" in stopword_list
    assert len(stopword_list) == n + 3
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)
    stopword_list.remove("hoimam", "hoipap", "hoibroer")
    assert "hoimam" not in stopword_list
    assert "hoipap" not in stopword_list
    assert "hoibroer" not in stopword_list
    assert len(stopword_list) == n
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)


@pytest.mark.parametrize("stopwords", ["dutch_stopwords", "english_stopwords"])
def test_stopwords_remove_list(stopwords, request):
    """
    Test removing a list of words from stop words.
    """
    stopword_list = request.getfixturevalue(stopwords)
    print(type(stopword_list))
    n = len(stopword_list)
    stopword_list.add(["hoimam", "hoipap", "hoibroer"])
    assert "hoimam" in stopword_list
    assert "hoipap" in stopword_list
    assert "hoibroer" in stopword_list
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)
    stopword_list.remove(["hoimam", "hoipap", "hoibroer"])
    assert "hoimam" not in stopword_list
    assert "hoipap" not in stopword_list
    assert "hoibroer" not in stopword_list
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)
    assert len(stopword_list) == n


@pytest.mark.parametrize("stopwords", ["dutch_stopwords", "english_stopwords"])
def test_stopwords_replace(stopwords, request):
    """
    Test replacing extra stopwords with a new set.
    """
    stopword_list = request.getfixturevalue(stopwords)
    # Initial extra stopwords
    initial_extra_stopwords = ["extra1", "extra2", "extra3"]
    stopword_list.add(initial_extra_stopwords)

    # New stopwords to replace the existing ones
    new_stopwords = ["new1", "new2", "new3"]
    stopword_list.replace(set(new_stopwords), new_stopwords)

    # Check if old extra stopwords are removed
    for word in initial_extra_stopwords:
        assert word not in stopword_list

    # Check if new stopwords are added
    for word in new_stopwords:
        assert word in stopword_list

    # Check if extra words set contains same words as extra words in order list
    assert stopword_list.extra_words == set(stopword_list.extra_words_in_order)


# def test_stopwords_add_invalid_argument_type(stopwords):
#    """
#    Test adding an invalid argument type to stop words.
#    """
#    with pytest.raises(TypeError):
#        stopwords.add(123)

# def test_stopwords_remove_invalid_argument_type(stopwords):
#    """
#    Test removing an invalid argument type to stop words.
#    """
#    with pytest.raises(TypeError):
#        stopwords.remove(123)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
