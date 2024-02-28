from abc import ABC, abstractmethod


class FileImporterInterface(ABC):

    @abstractmethod
    def load_file(self, path: str) -> str:
        pass

    @abstractmethod
    def compatible_file(self, path: str) -> bool:
        pass
