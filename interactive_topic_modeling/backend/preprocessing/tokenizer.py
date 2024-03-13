from nltk.tokenize import RegexpTokenizer
from spacy.tokens import Doc
from spacy import Language


class NLTKTokenizer:
    """
    class for tokenizing text using NLTk;s RegexpTokenizer.

    It uses:
    _vocab (spacy.vocab.Vocab): The vocabulary object from a spaCy
                                language pipeline.
    _tokenizer (nltk.tokenize.RegexpTokenizer): The tokenizer object
                                                from NLTK.
    """
    def __init__(self, nlp: Language) -> None:
        """
        Initialize the NLTKTokenizer object.

        :param nlp: The spaCy language object.
        :return: None.
        """
        self._vocab = nlp.vocab
        self._tokenizer = RegexpTokenizer(r'\w+')

    def __call__(self, doc: str) -> Doc:
        """
        Tokenize a document.
        :param doc: The input document to be tokenized.
        :return Doc: The tokenized document as a spaCy Doc object.
        """
        doc = doc.lower()
        words = self._tokenizer.tokenize(doc)
        words = [word for word in words if (not word.isnumeric())
                 and (len(word) > 1)]
        spaces = [True] * len(words)

        return Doc(self._vocab, words=words, spaces=spaces)
