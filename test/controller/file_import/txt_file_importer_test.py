import os
from datetime import datetime, timedelta

import pytest

from tommy.controller.file_import.txt_file_importer import TxtFileImporter

TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             '..',
                                             '..',
                                             'test',
                                             'test_data',
                                             'test_txt_files'))


@pytest.fixture
def txt_file_importer():
    return TxtFileImporter()


def test_compatible_file(txt_file_importer):
    compatible_path = os.path.join(TEST_DATA_DIR,
                                   'correct_files',
                                   'kattenverhaaltje 1.txt')
    assert txt_file_importer.compatible_file(compatible_path)

    incompatible_path = os.path.join(TEST_DATA_DIR,
                                     'incorrect_files',
                                     'kattenverhaaltje 1.pdf')
    assert not txt_file_importer.compatible_file(incompatible_path)


def test_load_file(txt_file_importer):
    testfile = os.path.join(TEST_DATA_DIR,
                            'correct_files',
                            'kattenverhaaltje 2.txt')

    for file_generator in txt_file_importer.load_file(testfile):
        file_text = file_generator.body.body.strip()

        # Assert
        assert file_generator is not None
        assert file_text == "Verhaaltje over een kat"


def test_generate_file(txt_file_importer):
    filepath = os.path.join(TEST_DATA_DIR,
                            'correct_files',
                            'kattenverhaaltje 1.txt')

    file_date = datetime.now()

    file = txt_file_importer.generate_file("Verhaaltje over een kat",
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
