class FileImporterInterface:
    def load_file(self, path: str) -> str:
        raise NotImplementedError

    def compatible_file(self, path: str) -> bool:
        raise NotImplementedError
