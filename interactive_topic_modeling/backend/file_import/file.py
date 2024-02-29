import os
from interactive_topic_modeling.backend.file_import import generic_file_importer
from typing import Generator


class File:

    def __init__(self, file_name: str):
        self.name = file_name
        self.format = file_name.split(".")[-1]
