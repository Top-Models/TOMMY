from interactive_topic_modeling.backend.file_import import file_importer_interface


class CsvFileImporter(file_importer_interface.FileImporterInterface):

    def __init__(self):
        pass

    # this is a dummy implementation of the csv importer
    def compatible_file(self, path: str) -> bool:
        return True

    def load_file(self, path: str) -> str:
        return path
