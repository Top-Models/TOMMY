import os
from collections.abc import Generator, Iterable

from gensim.corpora import Dictionary

from tommy.controller.file_import.generic_file_importer import (
    GenericFileImporter)
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.file_import.raw_body import RawBody
from tommy.controller.file_import.raw_file import RawFile
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
from tommy.support.event_handler import EventHandler
from tommy.model.corpus_model import CorpusModel


class CorpusController:
    """
    The corpus controller class is responsible for handling interactions with
    the corpus model.
    """

    _corpus_model: CorpusModel = None
    _project_settings_controller: ProjectSettingsController = None
    fileParsers: GenericFileImporter = GenericFileImporter()
    _metadata_changed_event: EventHandler[[Metadata]] = None

    @property
    def metadata_changed_event(self) -> EventHandler[[Metadata]]:
        """
        This event gets triggered every time the metadata of the corpus is
        changed, so the UI can update itself to show the metadata
        :return:
        """
        return self._metadata_changed_event

    def __init__(self) -> None:
        """Initialize corpus controller and eventhandler for metadata"""
        super().__init__()
        self._metadata_changed_event = EventHandler[[Metadata]]()

    def set_controller_refs(self,
                            project_settings_controller:
                            ProjectSettingsController) -> None:
        """
        Sets the reference to the project settings controller, 
        and subscribes to the publisher of project settings
        :param project_settings_controller: the project settings controller
        :return: None
        """
        self._project_settings_controller = project_settings_controller
        project_settings_controller.input_folder_path_changed_event.subscribe(
            self.on_input_folder_path_changed)

    def set_model_refs(self, corpus_model: CorpusModel) -> None:
        """
        Sets the reference to the corpus model
        :param corpus_model: The corpus model
        :return: None
        """
        self._corpus_model = corpus_model

    def change_config_model_refs(self, corpus_model: CorpusModel) -> None:
        """
        Sets the reference to the corpus model
        :param corpus_model: The corpus model
        :return: None
        """
        self._corpus_model = corpus_model

    def _read_files(self, path: str) -> Generator[RawFile, None, None]:
        """
        Yields the contents of all compatible files in a given directory
        and all its subdirectories.

        :param path: The string of the path to the directory
        :return: A generator yielding File
        objects
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.startswith('.'):
                    continue

                yield from self.fileParsers.import_file(
                    os.path.join(root,
                                 file))

    def _read_files_from_input_folder(self) -> Generator[RawFile, None, None]:
        """
        Private method to read all files in the folder specified in the
        project settings model

        :return: A generator that iterates over the raw
        file contents and their metadata.
        """
        path = self._project_settings_controller.get_input_folder_path()
        return self._read_files(path)

    def on_input_folder_path_changed(self, input_folder_path: str) -> None:
        """
        Gets the metadata from all files in the directory specified by the
        project settings and stores it in the corpus model and triggers the
        metadata-changed-event

        :param input_folder_path: The new path to the input folder
        :return: None
        """
        files = self._read_files(input_folder_path)
        metadata = [file.metadata for file in files]

        self._corpus_model.metadata = metadata
        self._metadata_changed_event.publish(metadata)

    def get_metadata(self) -> list[Metadata]:
        """
        Gets the metadata from all files in the corpus model. This method
        assumes that extract_and_store_metadata has already been called.

        :return: The metadata of the files in the corpus
        """
        return self._corpus_model.metadata

    def get_raw_bodies(self) -> Generator[RawBody, None, None]:
        """
        Get a generator that reads all the raw file contents from the input
        folder

        :return: A generator for just the contents of the raw corpus,
        but without the metadata
        """
        files = self._read_files_from_input_folder()
        return (file.body for file in files)

    def get_raw_files(self) -> Generator[RawFile, None, None]:
        """
        Get a generator that reads all the raw file contents and their metadata
        from the input folder

        :return: A generator of the raw corpus
        """
        return self._read_files_from_input_folder()

    def get_processed_corpus(self) -> Iterable[ProcessedFile]:
        """
        Get an iterable of the processed corpus. Only works after
        pre-processing has been completed.

        :return: The pre-processed files and a reference to their metadata
        """
        return self._corpus_model.processed_corpus

    def set_processed_corpus(self, corpus: list[ProcessedFile]) -> None:
        """
        Set the processed corpus using a list

        :param corpus: List of pre-processed files in a bag-of-words
        representation
        :return: None
        """
        self._corpus_model.processed_corpus.documents = corpus

    def get_dictionary(self) -> Dictionary:
        """
        Get the dictionary corresponding to the bag-of-words representation of
        the pre-processed documents. It is only set after pre-processing
        has been completed.

        :return: the dictionary of the pre-processed documents
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
