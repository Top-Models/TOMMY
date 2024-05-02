import os
import pytest
from tommy.controller.file_import.docx_file_importer import DocxFileImporter


TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             '..',
                                             '..',
                                             'test',
                                             'test_data',
                                             'test_docx_files'))


@pytest.fixture
def docx_file_importer():
    return DocxFileImporter()


def test_compatible_file(docx_file_importer):
    compatible_path = os.path.join(TEST_DATA_DIR,
                                   'correct_files',
                                   'kattenverhaaltje 1.docx')
    assert docx_file_importer.compatible_file(compatible_path)

    incompatible_path = os.path.join(TEST_DATA_DIR,
                                     'incorrect_files',
                                     'kattenverhaaltje 1.pdf')
    assert not docx_file_importer.compatible_file(incompatible_path)


def test_load_file(docx_file_importer):
    testfile = os.path.join(TEST_DATA_DIR,
                            'correct_files',
                            'kattenverhaaltje 1.docx')
    file_generator = docx_file_importer.load_file(testfile)
    assert file_generator is not None


def test_generate_file(docx_file_importer):
    filepath = os.path.join(TEST_DATA_DIR,
                            'correct_files',
                            'kattenverhaaltje 1.docx')
    testfile_metadata = {
             '/Author': 'Test Author',
             '/Title': 'kattenverhaaltje 1',
             '/ModDate': 'D:20220101000000+00\'00\''}

    file = docx_file_importer.generate_file("Verhaaltje over een kat",
                                                path=filepath,
                                                metadata=testfile_metadata)
    assert file is not None
    assert file.metadata is not None
    assert file.body.body == "Verhaaltje over een kat"
    assert file.metadata.author == 'Test Author'
    assert file.metadata.title == 'kattenverhaaltje 1'
    assert file.metadata.date == 'D:20220101000000+00\'00\''