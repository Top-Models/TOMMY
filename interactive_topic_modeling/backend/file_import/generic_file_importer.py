from interactive_topic_modeling.backend.file_import import file_importer_interface
from interactive_topic_modeling.backend.file_import import csv_file_importer
from typing import List


class GenericFileImporter:
    def __init__(self):
        self.importers: List[file_importer_interface.FileImporterInterface] = [csv_file_importer.CsvFileImporter()]

    def import_file(self, path: str) -> str:
        for importer in self.importers:
            if importer.compatible_file(path):
                return importer.load_file(path)
        raise NotImplementedError("File does not have a compatible file importer implementation. Path:", path)
