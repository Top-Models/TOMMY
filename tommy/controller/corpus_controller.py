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
    corpus_model: CorpusModel = None
    project_settings_model: ProjectSettingsModel = None
    fileParsers: GenericFileImporter = GenericFileImporter()

    @staticmethod
    def set_corpus_model(corpus_model: CorpusModel) -> None:
        """
        Sets the reference to the corpus model

        :param corpus_model: The corpus model
        :return: None
        """
        CorpusController.corpus_model = corpus_model

    @staticmethod
    def set_project_settings_model(
            project_settings_model: ProjectSettingsModel) -> None:
        """
        Sets the reference to the project settings model

        :param project_settings_model: The project settings model
        :return: None
        """
        CorpusController.project_settings_model = project_settings_model

    @staticmethod
    def _read_files(path: str) -> Generator[RawFile, None, None]:
        """
        Yields the contents of all compatible files in a given directory
        and all its subdirectories.

        :param path: The string of the path to the directory
        :return: Generator[RawFile, None, None]: A generator yielding File
        objects
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                yield from CorpusController.fileParsers.import_file(
                    os.path.join(root,
                                 file))

    @staticmethod
    def _read_files_from_input_folder() -> Generator[RawFile, None, None]:
        """
        Private method to read all files in the folder specified in the
        project settings model

        :return: Generator[RawFile]: a generator that iterates over the raw
        file contents and their metadata.
        """
        return CorpusController._read_files(
            CorpusController.project_settings_model.input_folder_path)

    @staticmethod
    def extract_and_store_metadata() -> None:
        """
        Gets the metadata from all files in the directory specified by the
        project settings and stores it in the corpus model.

        :return: None
        """
        files = CorpusController._read_files_from_input_folder()
        metadatas = [file.metadata for file in files]

        CorpusController.corpus_model.metadatas = metadatas

    @staticmethod
    def get_metadata() -> List[Metadata]:
        """
        Gets the metadata from all files in the corpus model. This method
        assumes that extract_and_store_metadata has already been called.

        :return: List[Metadata]: The metadata of the files in the corpus
        """
        return CorpusController.corpus_model.metadatas

    @staticmethod
    def get_raw_bodies() -> Generator[RawBody, None, None]:
        """
        Get a generator that reads all the raw file contents from the input
        folder

        :return: Generator[RawBody]: a generator for just the contents of
        the raw corpus, but without the metadata
        """
        files = CorpusController._read_files_from_input_folder()
        return (file.body for file in files)

    @staticmethod
    def get_processed_corpus() -> Iterable[ProcessedFile]:
        """
        Get an iterable of the processed corpus. Only works after
        pre-processing has been completed.

        :return: Iterable[ProcessedFile]: The pre-processed files and a
        reference to their metadata
        """
        return CorpusController.corpus_model.processed_corpus

    @staticmethod
    def set_processed_corpus(corpus: List[ProcessedFile]) -> None:
        """
        Set the processed corpus using a list

        :param corpus: List[ProcessedFile]: List of pre-processed files in
        a bag-of-words representation
        :return: None
        """
        CorpusController.corpus_model.processed_corpus.documents = corpus

    @staticmethod
    def get_dictionary() -> Dictionary:
        """
        Get the dictionary corresponding to the bag-of-words representation of
        the pre-processed documents. It is only set after pre-processing
        has been completed.

        :return: corpora.Dictionary: the dictionary of the pre-processed
        documents
        """
        return CorpusController.corpus_model.dictionary

    @staticmethod
    def set_dictionary(dictionary: Dictionary) -> None:
        """
        Set the dictionary corresponding to the bag-of-words representation of
        the pre-processed documents.

        :param dictionary: corpora.Dictionary: the dictionary of the pre-processed
        documents
        :return: None
        """
        CorpusController.corpus_model.dictionary = dictionary


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
