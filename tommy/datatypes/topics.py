from dataclasses import dataclass


@dataclass
class Topic:
    """
    A dataclass representing a topic resulting from modelling run, holding
    a number of top words per topic.
    """
    topic_id: int
    top_words: list[str]

    @property
    def n_words(self) -> int:
        """Get the number of top words saved in this topic object"""
        return len(self.top_words)


class TopicWithScores(Topic):
    """
    A more extensive class representing topic resulting from modelling run,
    holding a number of top words per topic and their scores.
    """
    word_scores: list[float]

    @property
    def top_words_with_scores(self) -> list[tuple[str, float]]:
        """Get tuples of top words with their corresponding score"""
        return zip(self.top_words, self.word_scores)

    def __init__(self, topic_id: int,
                 top_words_with_scores: list[tuple[str, float]]) -> None:
        """
        Create a topic object that holds top words and their corresponding
        scores.
        :param topic_id: The id of the topic that this object represents
        :param top_words_with_scores: the list of tuples of top words and their
            corresponding score
        :return: None
        """
        top_words, word_scores = zip(*top_words_with_scores)
        self.word_scores = word_scores
        super().__init__(topic_id, top_words)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
