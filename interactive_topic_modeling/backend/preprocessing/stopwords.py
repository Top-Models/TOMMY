from collections.abc import Iterable


class StopWords:
    """A class representing the sets of stopwords."""

    def __init__(self, words: Iterable[str]) -> None:
        """Initialize the Stopwords object."""
        self.words = set(words)

    def __str__(self) -> str:
        """Get a sting representation of the stop words"""
        return f"{list(self.words)}"

    def __len__(self) -> int:
        """Get the number of stop words"""
        return len(self.words)

    def __contains__(self, word: str) -> bool:
        """Check if the stop words list contains a word"""
        return word in self.words

    def __iter__(self) -> Iterable[str]:
        """Return an iterable stopword list"""
        return iter(self.words)

    def add(self, *args: str | Iterable[str]) -> None:
        """
        Add one or more stop words
        :param args: The word(s) to add to the iterable.
        :return: None.
        """
        # Only 1 argument and it's a list or tuple
        if len(args) == 1 and isinstance(args[0], Iterable):
            words = args[0]
        # Otherwise the arguments should be the words themselves
        else:
            words = args
        # Add the words to the set
        for word in words:
            self.words.add(word)

    def remove(self, *args: str | Iterable[str]) -> None:
        """
        Remove one or more stop words
        :param args: The word(s) to remove from the iterable.
        :return: None.
        """
        # Only 1 argument and it's a list or tuple
        if len(args) == 1 and isinstance(args[0], Iterable):
            words = args[0]
        # Otherwise the arguments should be the words themselves
        else:
            words = args
        # Remove the words from the set
        for word in words:
            self.words.discard(word)
