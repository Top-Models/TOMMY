from nltk.tokenize import RegexpTokenizer
from spacy.tokens import Doc
from spacy import Language


class NLTKTokenizer:
    def __init__(self, nlp: Language) -> None:
        self._vocab = nlp.vocab
        self._tokenizer = RegexpTokenizer(r'\w+')

    def __call__(self, doc: str) -> Doc:
        doc = doc.lower()
        words = self._tokenizer.tokenize(doc)
        words = [word for word in words if (not word.isnumeric()) and (len(word) > 1)]
        spaces = [True] * len(words)

        return Doc(self._vocab, words=words, spaces=spaces)
