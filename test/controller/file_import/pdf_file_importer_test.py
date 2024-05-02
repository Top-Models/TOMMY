import os
import pytest
from tommy.controller.file_import.pdf_file_importer import PdfFileImporter


TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             '..',
                                             '..',
                                             'test',
                                             'test_data',
                                             'test_pdf_files'))


@pytest.fixture
def pdf_file_importer():
    return PdfFileImporter()


def test_compatible_file(pdf_file_importer):
    compatible_path = os.path.join(TEST_DATA_DIR,
                                   'correct_files',
                                   'kattenverhaaltje 1.pdf')
    assert pdf_file_importer.compatible_file(compatible_path)

    incompatible_path = os.path.join(TEST_DATA_DIR,
                                     'incorrect_files',
                                     'kattenverhaaltje 1.docx')
    assert not pdf_file_importer.compatible_file(incompatible_path)


def test_load_file(pdf_file_importer):
    files_path = os.path.join(TEST_DATA_DIR, 'correct_files')
    for testfile in pdf_file_importer.load_file(files_path):
        file_generator = pdf_file_importer.load_file(testfile)
        file = next(file_generator)
        assert file is not None


def test_generate_file(pdf_file_importer):
    filepath = os.path.join(TEST_DATA_DIR,
                            'correct_files',
                            'kattenverhaaltje 1.pdf')
    testfile_metadata = {
             '/Author': 'Test Author',
             '/Title': 'kattenverhaaltje 1',
             '/ModDate': 'D:20220101000000+00\'00\''}

    file = pdf_file_importer.generate_file("Verhaaltje over een kat",
                                                path=filepath,
                                                metadata=testfile_metadata)
    assert file is not None
    assert file.metadata is not None
    assert file.body.body == "Verhaaltje over een kat"
    assert file.metadata.author == 'Test Author'
    assert file.metadata.title == 'kattenverhaaltje 1'
    assert file.metadata.date == 'D:20220101000000+00\'00\''


