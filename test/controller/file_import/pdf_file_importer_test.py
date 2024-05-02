import pytest
from tommy.controller.file_import.pdf_file_importer import PdfFileImporter

class TestPdfFileImporter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.pdf_importer = PdfFileImporter()

    def test_compatible_file(self):
        assert self.pdf_importer.compatible_file('test_pdf/'
                                                 'correct_files/'
                                                 'kattenverhaaltje 1.pdf')
        assert not self.pdf_importer.compatible_file('test_pdf/'
                                                     'incorrect_files/'
                                                     'kattenverhaaltje 1.docx')

    def test_load_file(self):
        for testfile in self.pdf_importer.load_file('test_pdf/correct_files'):
            file_generator = self.pdf_importer.load_file(testfile)
            file = next(file_generator)
            assert file is not None

    def test_generate_file(self):
        file = self.pdf_importer.generate_file('test',
                                               'test_pdf/correct_files/kattenverhaaltje 1.pdf',
                                               'metadata')
        assert file is not None
        assert file.body == 'test'
        assert file.path == 'test_pdf/correct_files/kattenverhaaltje 1.pdf'
        assert file.metadata == 'metadata'
