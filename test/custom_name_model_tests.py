import pytest

from tommy.model.custom_name_model import TopicNameModel


def test_initialization_with_config_name():
    model = TopicNameModel(config_name="new config")
    assert model.topic_names == {"new config": {}}


def test_initialization_without_config_name():
    model = TopicNameModel()
    assert model.topic_names == {}


def test_get_topic_name_with_existing_config_and_index():
    model = TopicNameModel()
    model.set_topic_name("test config",
                         0,
                         "test topic")
    assert (model.get_topic_name("test config", 0) ==
            "test topic")


# Returns default topic
def test_get_topic_name_with_non_existing_config():
    model = TopicNameModel()
    assert (model.get_topic_name("new test config", 0) ==
            "Topic 1")


def test_get_topic_name_with_non_existing_index():
    model = TopicNameModel()
    model.set_topic_name("config", 0, "custom topic")
    assert model.get_topic_name("config", 1) == "Topic 2"


def test_set_topic_name():
    model = TopicNameModel()
    model.set_topic_name("config", 0, "custom topic")
    assert model.topic_names["config"][0] == "custom topic"


def test_remove_config():
    model = TopicNameModel()
    model.set_topic_name("config", 0, "topic")
    model.remove_config("config")
    assert "config" not in model.topic_names


def test_remove_non_existing_config():
    model = TopicNameModel()
    model.set_topic_name("config1", 0, "topic")
    model.remove_config("config2")
    assert "config1" in model.topic_names


# Running the tests
if __name__ == "__main__":
    pytest.main()

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
