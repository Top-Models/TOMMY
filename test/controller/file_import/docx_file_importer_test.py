import os
import pytest
from datetime import datetime, timedelta

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


def test_corrupted_file(docx_file_importer):
    corrupted_path = os.path.join(TEST_DATA_DIR,
                                  'corrupt_files',
                                  'hondenverhaaltje 1.docx')
    assert not docx_file_importer.compatible_file(corrupted_path)


def test_load_file(docx_file_importer):
    testfile = os.path.join(TEST_DATA_DIR,
                            'correct_files',
                            'kattenverhaaltje 2.docx')

    for file_generator in docx_file_importer.load_file(testfile):
        file_text = file_generator.body.body.strip()

        # Assert
        assert file_generator is not None
        assert file_text == "Verhaaltje over een kat"


def test_generate_file(docx_file_importer):
    filepath = os.path.join(TEST_DATA_DIR,
                            'correct_files',
                            'kattenverhaaltje 1.docx')

    file_date = datetime.now()

    file = docx_file_importer.generate_file("Verhaaltje over een kat",
                                                path=filepath)

    # Set date as current date for testing purposes
    file.metadata.date = file_date

    assert file is not None
    assert file.metadata is not None
    assert file.body.body == "Verhaaltje over een kat"
    assert file.metadata.title == 'kattenverhaaltje 1'

    # Get the current date
    current_date = datetime.now()

    # Check if the date in the metadata is validly set (within 1 day)
    # We are interested in days only, so we usually ignore time
    assert abs(file.metadata.date - current_date) < timedelta(minutes=10)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
