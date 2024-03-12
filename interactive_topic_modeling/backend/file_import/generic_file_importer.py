from typing import List, Generator

from interactive_topic_modeling.backend.file_import.file import File
from interactive_topic_modeling.backend.file_import import file_importer_base
from interactive_topic_modeling.backend.file_import import csv_file_importer


class GenericFileImporter:
    """
    The class GenericFileImporter is responsible for importing files using FileImporterBase objects
    """
    def __init__(self):
        """
        Initialization of a new GenericFileImporter object.
        """
        self.importers: List[file_importer_base.FileImporterBase] = [csv_file_importer.CsvFileImporter()]

    def import_file(self, path: str) -> Generator[File, None, None]:
        """
        Imports a file from the specified path using compatible importers.

        :param path: The string path of the file to import.
        :return Generator[File, None, None]: A generator yielding File objects.
        """
        for importer in self.importers:
            if importer.compatible_file(path):
                return importer.load_file(path)
        raise NotImplementedError("File does not have a compatible file importer implementation. Path:", path)
