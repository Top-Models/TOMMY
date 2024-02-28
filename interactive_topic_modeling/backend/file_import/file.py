import os
from interactive_topic_modeling.backend.file_import import generic_file_importer
from typing import Generator


class File:

    def __init__(self):
        # The selected directory is part of the project settings,
        # so this is a dummy implementation and the selected directory
        # should be fetched from the project settings
        self.fileParsers = generic_file_importer.GenericFileImporter()

    def test_read_file(self):
        print(list(self.read_files(os.path.pardir)))

    # yields the contents of all compatible files in a given directory and all its subdirectories
    def read_files(self, path: str) -> Generator[str, None, None]:
        for root, dirs, files in os.walk(path):
            for file in files:
                yield self.fileParsers.import_file(os.path.join(root, file))


if __name__ == "__main__":
    test_file = File()
    test_file.test_read_file()
