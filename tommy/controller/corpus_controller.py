import os
from typing import Generator, Iterable, List

from tommy.controller.file_import.generic_file_importer import (
    GenericFileImporter)
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.file_import.raw_body import RawBody
from tommy.controller.file_import.raw_file import RawFile
from tommy.model.corpus_model import CorpusModel
from tommy.model.project_settings_model import ProjectSettingsModel


class CorpusController:
    corpus_model: CorpusModel = None
    project_settings_model: ProjectSettingsModel = None
    fileParsers: GenericFileImporter = GenericFileImporter()

    @staticmethod
    def set_corpus_model(corpus_model: CorpusModel):
        """
        Sets the corpus model
        :param corpus_model:
        :return:
        """
        CorpusController.corpus_model = corpus_model

    @staticmethod
    def set_project_settings_model(
            project_settings_model: ProjectSettingsModel):
        CorpusController.project_settings_model = project_settings_model

    @staticmethod
    def _read_files(path: str) -> Generator[RawFile, None, None]:
        """
        Yields the contents of all compatible files in a given directory
        and all its subdirectories.

        :param path: The string of the path to the directory
        :return: Generator[File, None, None]: A generator yielding File objects
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                yield from CorpusController.fileParsers.import_file(
                    os.path.join(root,
                                 file))

    @staticmethod
    def _read_files_from_input_folder() -> Generator[RawFile, None, None]:
        print(CorpusController.project_settings_model)
        print(CorpusController.project_settings_model.input_folder_path)
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
        return CorpusController.corpus_model.metadatas

    @staticmethod
    def get_raw_bodies() -> Generator[RawBody, None, None]:
        files = CorpusController._read_files_from_input_folder()
        return (file.body for file in files)

    @staticmethod
    def get_processed_corpus() -> Iterable[ProcessedFile]:
        return CorpusController.corpus_model.processed_corpus

    @staticmethod
    def set_processed_corpus(corpus: List[ProcessedFile]) -> None:
        CorpusController.corpus_model.processed_corpus.documents = corpus


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
