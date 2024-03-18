import os
from typing import Generator

from interactive_topic_modeling.backend.file_import.file import File
from interactive_topic_modeling.model.corpus_model import CorpusModel

from interactive_topic_modeling.backend.file_import.generic_file_importer import GenericFileImporter

"""
this controller is responsible for:
 - extracting text from different file types
 - extracting metadata from files if possible
 - storing metadata in the corpus model
"""


class FileReadingController:
    def __init__(self):
        self.corpus_model: CorpusModel = None

        # The selected directory is part of the project settings,
        # so this is a dummy implementation and the selected directory
        # should be fetched from the project settings
        self.fileParsers = GenericFileImporter()

    def set_corpus_model(self, corpus_model: CorpusModel):
        self.corpus_model = corpus_model

    def load_files_from_selected_folder(self):
        pass

    def read_files(self, path: str) -> Generator[File, None, None]:
        """
        Yields the contents of all compatible files in a given directory
        and all its subdirectories.

        :param path: The string of the path to the directory
        :return Generator[File, None, None]: A generator yielding File objects.
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                yield from self.fileParsers.import_file(os.path.join(root,
                                                                     file))

    """
    This program has been developed by students from the bachelor Computer Science
    at Utrecht University within the Software Project course.
    © Copyright Utrecht University 
    (Department of Information and Computing Sciences)
    """
