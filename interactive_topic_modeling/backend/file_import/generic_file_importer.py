from interactive_topic_modeling.backend.file_import import file_importer_base
from interactive_topic_modeling.backend.file_import import csv_file_importer
from typing import List, Generator
from interactive_topic_modeling.backend.file_import.file import File


class GenericFileImporter:
    def __init__(self):
        self.importers: List[file_importer_base.FileImporterBase] = [csv_file_importer.CsvFileImporter()]

    def import_file(self, path: str) -> Generator[File, None, None]:
        for importer in self.importers:
            if importer.compatible_file(path):
                return importer.load_file(path)
        raise NotImplementedError("File does not have a compatible file importer implementation. Path:", path)
