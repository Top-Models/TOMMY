import os
from typing import Generator, Iterable, List

from gensim.corpora import Dictionary

from tommy.controller.file_import.generic_file_importer import (
    GenericFileImporter)
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.file_import.raw_body import RawBody
from tommy.controller.file_import.raw_file import RawFile
from tommy.model.corpus_model import CorpusModel
from tommy.model.project_settings_model import ProjectSettingsModel


class CorpusController:
    """
    The corpus controller class is responsible for handling interactions with
    the corpus model.
    """
    _corpus_model: CorpusModel = None
    _project_settings_model: ProjectSettingsModel = None
    fileParsers: GenericFileImporter = GenericFileImporter()

    def __init__(self) -> None:
        pass

    def set_model_refs(self, corpus_model: CorpusModel,
                       project_settings_model: ProjectSettingsModel) -> None:
        """
        Sets the reference to the corpus model and the project settings model
        :param corpus_model: The corpus model
        :param project_settings_model: The project settings model
        :return: None
        """
        self._corpus_model = corpus_model
        self._project_settings_model = project_settings_model

    def _read_files(self, path: str) -> Generator[RawFile, None, None]:
        """
        Yields the contents of all compatible files in a given directory
        and all its subdirectories.

        :param path: The string of the path to the directory
        :return: Generator[RawFile, None, None]: A generator yielding File
        objects
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                yield from self.fileParsers.import_file(
                    os.path.join(root,
                                 file))

    def _read_files_from_input_folder(self) -> Generator[RawFile, None, None]:
        """
        Private method to read all files in the folder specified in the
        project settings model

        :return: Generator[RawFile]: a generator that iterates over the raw
        file contents and their metadata.
        """
        return self._read_files(
            self._project_settings_model.input_folder_path)

    def extract_and_store_metadata(self) -> None:
        """
        Gets the metadata from all files in the directory specified by the
        project settings and stores it in the corpus model.

        :return: None
        """
        files = self._read_files_from_input_folder()
        metadatas = [file.metadata for file in files]

        self._corpus_model.metadatas = metadatas

    def get_metadata(self) -> List[Metadata]:
        """
        Gets the metadata from all files in the corpus model. This method
        assumes that extract_and_store_metadata has already been called.

        :return: List[Metadata]: The metadata of the files in the corpus
        """
        return self._corpus_model.metadatas

    def get_raw_bodies(self) -> Generator[RawBody, None, None]:
        """
        Get a generator that reads all the raw file contents from the input
        folder

        :return: Generator[RawBody]: a generator for just the contents of
        the raw corpus, but without the metadata
        """
        files = self._read_files_from_input_folder()
        return (file.body for file in files)

    def get_processed_corpus(self) -> Iterable[ProcessedFile]:
        """
        Get an iterable of the processed corpus. Only works after
        pre-processing has been completed.

        :return: Iterable[ProcessedFile]: The pre-processed files and a
        reference to their metadata
        """
        return self._corpus_model.processed_corpus

    def set_processed_corpus(self, corpus: List[ProcessedFile]) -> None:
        """
        Set the processed corpus using a list

        :param corpus: List[ProcessedFile]: List of pre-processed files in
        a bag-of-words representation
        :return: None
        """
        self._corpus_model.processed_corpus.documents = corpus

    def get_dictionary(self) -> Dictionary:
        """
        Get the dictionary corresponding to the bag-of-words representation of
        the pre-processed documents. It is only set after pre-processing
        has been completed.

        :return: corpora.Dictionary: the dictionary of the pre-processed
        documents
        """
        return self._corpus_model.dictionary

    def set_dictionary(self, dictionary: Dictionary) -> None:
        """
        Set the dictionary corresponding to the bag-of-words representation of
        the pre-processed documents.

        :param dictionary: corpora.Dictionary: the dictionary of the
        pre-processed documents
        :return: None
        """
        self._corpus_model.dictionary = dictionary


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
