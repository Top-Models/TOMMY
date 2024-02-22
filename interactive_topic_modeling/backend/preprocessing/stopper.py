from pipeline import Component


class Stopper(Component):

    def __init__(self, name):
        super().__init__(name)
        # Open the file
        with open('stopwords.txt', 'r') as file:
            # Read the content of the file into a string
            file_content = file.read()

        # Parse the stopwords
        stopword_list = file_content.split()
        self.stopwords = StopWords(stopword_list)

    def process(self, tokens):
        # Remove the stopwords from the tokens
        return [token for token in tokens if token not in self.stopwords]


class StopWords:

    def __init__(self, words):
        self.words = set(words)

    def __str__(self):
        return f"{list(self)}"

    def __len__(self):
        return len(self.words)

    def __contains__(self, word):
        return word in self.words

    def __iter__(self):
        return iter(self.words)

    def add(self, *args):
        # Only 1 argument and it's a list or tuple
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            words = args[0]
        # Otherwise the arguments should be the words themselves
        else:
            words = args
        # Add the words to the set
        for word in words:
            self.words.add(word)

    def remove(self, *args):
        # Only 1 argument and it's a list or tuple
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            words = args[0]
        # Otherwise the arguments should be the words themselves
        else:
            words = args
        # Remove the words from the set
        for word in words:
            self.words.discard(word)
