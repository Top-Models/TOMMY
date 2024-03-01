from collections.abc import Iterable


class StopWords:

    def __init__(self, words: Iterable[str]):
        self.words = set(words)

    def __str__(self) -> str:
        return f"{list(self.words)}"

    def __len__(self) -> int:
        return len(self.words)

    def __contains__(self, word: str) -> bool:
        return word in self.words

    def __iter__(self) -> Iterable[str]:
        return iter(self.words)

    def add(self, *args: str):
        # Only 1 argument and it's a list or tuple
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            words = args[0]
        # Otherwise the arguments should be the words themselves
        else:
            words = args
        # Add the words to the set
        for word in words:
            self.words.add(word)

    def remove(self, *args: str):
        # Only 1 argument and it's a list or tuple
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            words = args[0]
        # Otherwise the arguments should be the words themselves
        else:
            words = args
        # Remove the words from the set
        for word in words:
            self.words.discard(word)
