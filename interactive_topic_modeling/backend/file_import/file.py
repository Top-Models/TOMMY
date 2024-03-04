import os
from interactive_topic_modeling.backend.file_import import generic_file_importer
from typing import Generator


class File:

    def __init__(self, file_name: str, file_path: str, file_content: str, file_size: int):
        self.name = file_name
        self.format = file_name.split(".")[-1]
        self.path = file_path
        self.size = file_size
        self.content = file_content
        self.length = len(file_content.split())
