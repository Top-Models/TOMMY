from typing import List

from gensim.corpora import Dictionary

from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.processed_corpus import ProcessedCorpus


class CorpusModel:
    metadatas: List[Metadata] = None
    dictionary: Dictionary = None
    processed_corpus: ProcessedCorpus = None

    def __init__(self):
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
