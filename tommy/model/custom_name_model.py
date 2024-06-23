class TopicNameModel:
    """A class to store custom topic names for each configuration."""

    def __init__(self) -> None:
        # Dictionary to store the custom topic names, indexed by configuration
        self.topic_names = {}

    def get_topic_name(self, index: int) -> str:
        """
        Function to get the custom name of a topic.
        If no custom name is set, the default name is returned.
        :param config_name: The name of the configuration
        :param index: The index of the topic
        :return: The name of the topic
        """
        return self.topic_names.get(index, f"Topic {index + 1}")

    def set_topic_name(self, index: int, name: str) -> None:
        """
        Function to set a custom name for a topic.
        :param config_name: The name of the configuration
        :param index: The index of the topic
        :param name: The custom name to set
        :return: None
        """
        self.topic_names[index] = name

    def clear_topic_names(self) -> None:
        """
        Function to clear all custom topic names in a config when rerunning
        topic modelling.
        :return: None
        """
        self.topic_names = {}


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
