class TopicNameModel:
    """A class to store custom topic names for each configuration."""
    def __init__(self, config_name: str = None) -> None:
        # Dictionary to store the custom topic names, indexed by configuration
        self.topic_names = {config_name: {}} if config_name else {}

    def get_topic_name(self, config_name: str, index: int) -> str:
        """Function to get the custom name of a topic.
        If no custom name is set, the default name is returned."""
        return self.topic_names.get(config_name, {}).get(index,
                                                         f"Topic {index + 1}")

    def set_topic_name(self, config_name: str, index: int, name: str) -> None:
        """Function to set a custom name for a topic."""
        if config_name not in self.topic_names:
            self.topic_names[config_name] = {}
        self.topic_names[config_name][index] = name
        print(self.topic_names)

    def remove_config(self, config_name: str) -> None:
        """Function to remove a configuration from the model."""
        if config_name in self.topic_names:
            del self.topic_names[config_name]