from nltk.tokenize import RegexpTokenizer


class Tokenizer:
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')

    def process(self, docs):
        return [self.tokenizer.tokenize(doc.lower()) for doc in docs]


tokenizer = Tokenizer().process
