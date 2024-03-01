import spacy
from spacy.tokens import Doc

from stopwords import StopWords
from tokenizer import NLTKTokenizer


#    Entire pipeline:
#    ----------------
# 1. Build-in tokenization (generates metadata)
# 2. Remove certain entity types
# 3. Remove certain POS tags
# 4. Take the lemmas of the tokens
# 5. Convert to lowercase, remove interpunction, remove numbers, remove 1-letter words, remove diacritical marks
#    (i.e. additional tokenization)
# 6. TODO: Implement n-grams (up to some n)                        (Gensim)
# 7. TODO: Implement word-frequency filtering (w/ some threshold)  (Gensim)
# 8. Remove lemmatized stopwords
class Pipeline:  # Temporary class to contain the entire pipeline without design patterns
    def __init__(self):
        # Load pre-trained natural language pipeline (python3 -m spacy download nl_core_news_sm)
        # Used pipeline components: tok2vec, lemmatizer, tagger, attribute-ruler, ner
        nlp = spacy.load("nl_core_news_sm", exclude=["morphologizer", "parser", "senter"])
        self._nlp = nlp

        self._entities = {"ORDINAL", "QUANTITY", "PERSON", "MONEY", "CARDINAL", "DATE", "TIME"}
        self._tags = {"PUNCT", "NUM", "SYM", "X"}

        with open('stopwords.txt', 'r') as file:
            file_content = file.read()
        stopword_list = file_content.split()
        self._stopwords = StopWords(stopword_list)

    def __call__(self, text: str) -> list[str]:
        # 1
        tokens = self._nlp(text)
        tokens = self.process_tokens(tokens)
        return tokens

        # for doc in self._nlp.pipe(texts):
        # tokenized_docs.append(self.process_tokens(doc))
        # return tokenized_docs

    def process_tokens(self, doc: Doc) -> list[str]:
        # 2, 3, 4 - all steps that require token-level information
        lemmas = [token.lemma_ for token in doc if
                  token.ent_type_ not in self._entities and token.tag_ not in self._tags]

        # 5 - transforming the tokens (lemmas) themselves
        lemmas = [lemma.lower() for lemma in lemmas if lemma.isalpha() and len(lemma) > 1]
        # TODO: fix isalpha() for "-"words and remove diacrticial marks (and other character 'normalization')
        # words = [word for word in words if (not word.isnumeric()) and (len(word) > 1)]

        # TODO: 6,7

        # 8 - stopword removal, which can should be detached from the rest of the pipeline
        lemmas = [lemma for lemma in lemmas if lemma not in self._stopwords]

        return lemmas

    def add_stopwords(self, words: str) -> None:
        self._stopwords.add(words)

    def remove_stopwords(self, words: str) -> None:
        self._stopwords.remove(words)
