from dataclasses import dataclass
from typing import List

from gensim.corpora import Dictionary

from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.processed_corpus import ProcessedCorpus


class CorpusModel:
    """
    CorpusModel stores the data about the documents in the input folder. It
    is only accessible through the CorpusController class. The raw corpus
    data is not stored as it wouldn't fit in memory. The processed corpus is
    stored in the ProcessedCorpus class.
    """
    metadatas: List[Metadata] = None
    dictionary: Dictionary = None
    processed_corpus: ProcessedCorpus

    def __init__(self):
        self.processed_corpus = ProcessedCorpus()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
