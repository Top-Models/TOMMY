from abc import ABC, abstractmethod
from datetime import date, datetime


class FileImporterBase(ABC):

    @abstractmethod
    def load_file(self, path: str) -> str:
        pass

    @abstractmethod
    def compatible_file(self, path: str) -> bool:
        pass

    def parse_date(self, date: str) -> date:
        raise NotImplementedError
