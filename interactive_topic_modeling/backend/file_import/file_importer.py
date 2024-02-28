import os
import generic_file_importer
from typing import Generator
from interactive_topic_modeling.support import project_settings
from interactive_topic_modeling.backend.file_import.file import File


class FileImporter:
    """FileImporter is the mother class responsible for getting a path to a
     folder, and creating a generator that returns all files in the directory"""

    def __init__(self):
        self.fileParsers = generic_file_importer.GenericFileImporter()

    def test_read_file(self):
        project_settings.current_project_settings.selected_folder = os.path.pardir
        print(project_settings.current_project_settings.selected_folder)
        print(list(self.read_files()))

    # yields the contents of all compatible files in the current project
    # settings selected folder and all its subdirectories
    def read_files(self) -> Generator[File, None, None]:
        for root, dirs, files in os.walk(
                project_settings.current_project_settings.selected_folder):
            for file in files:
                yield self.fileParsers.import_file(os.path.normpath(
                    os.path.join(root, file)))


if __name__ == "__main__":
    test_file = FileImporter()
    test_file.test_read_file()
