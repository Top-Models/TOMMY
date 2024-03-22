from dataclasses import dataclass
from typing import List

from tommy.controller.file_import.processed_file import ProcessedFile


@dataclass
class ProcessedCorpus:
    """
    The ProcessedCorpus class is an iterable of ProcessedFile objects
    """
    documents: List[ProcessedFile] = None

    def __iter__(self):
        """
        :return: an iterator of ProcessedFile objects
        """
        return iter(self.documents)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
