import csv
import os
from typing import LiteralString, Optional, Dict, List

from striprtf.striprtf import rtf_to_text

"""
This is a standalone script for generating a csv file from a folder
with rtf files. The rtf files are exported from lexus nexus and have a 
specific layout. 
"""


def extract_data_from_rtf_file(file_path) -> Optional[Dict[str,
                                                           str |
                                                           LiteralString]]:
    """
    Extract data from an RTF file.
    :param file_path: The path to the RTF file.
    :return:  A dictionary containing the extracted data,
              or None if extraction fails
    """
    try:
        with (open(file_path, 'r', encoding='utf-8', errors='ignore')
              as rtf_file):
            rtf_content = rtf_file.read()

        # Using striprtf to extract plain text from RTF content
        body = rtf_to_text(rtf_content)

        # Extracting title from the first non-empty line
        lines = body.split('\n')
        title1_index = next(
            # Index of the first non-empty line
            index for index, line in enumerate(lines) if line.strip())

        # Get the title from the first non-empty line
        title1 = lines[title1_index].strip()

        # Check if the next index exists and has leading space,
        # then append it to title1
        title1_end_index = title1_index
        if (title1_index + 1 < len(lines) and
                lines[title1_index + 1].startswith(' ')):
            title1 += ' ' + lines[title1_index + 1].strip()
            title1_end_index = title1_index + 1

        # Check if there are enough lines
        if len(lines) < title1_end_index + 3:
            print(f"Skipping file {file_path} - "
                  f"Not enough lines to extract data")
            return None  # or return {}

        # Extracting date from the second line after the title
        date = lines[title1_end_index + 2]
        date = date.lstrip(',')  # Remove leading `",`
        date = date.strip('"')  # Remove trailing '"'

        # Remove surrounding quotations from the title
        title = title1.strip('"').strip("'")

        # Extracting body from the line 'Body' to 'Graphic'
        # (or 'Classification' if 'Graphic' is missing)
        start_index = lines.index('Body') + 1 if 'Body' in lines else 0
        end_index = len(lines)
        for section in ['Graphic', 'Classification']:
            if section in lines:
                end_index = lines.index(section)
                break

        # filter the empty lines out of the body before joining it together
        body_content = '\n'.join(filter(''.__ne__,
                                        lines[start_index:end_index]))

        # Remove newlines from body_content
        body_content = body_content.replace('\n', ' ')

        return {'title': title, 'body': body_content, 'date': date}
    except UnicodeDecodeError:
        print(f"Skipping file {file_path} - UnicodeDecodeError")
        return None  # or return {}


def process_rtf_folder(folder_path) -> List[Dict[str, str]]:
    """
    Processes a folder containing RTF files.

    :param folder_path: The path of the folder.
    :return: A list of dictionaries containing extracted data
    """
    all_data_folder = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.rtf'):
            rtf_file_path = os.path.join(folder_path, filename)
            extracted_data = extract_data_from_rtf_file(rtf_file_path)
            if extracted_data is not None:
                all_data_folder.append(extracted_data)

    # Remove duplicates based on 'title', 'body', and 'date'
    unique_data = [dict(t) for t in {tuple(d.items()) for d
                                     in all_data_folder if d is not None}]
    return unique_data


def export_to_csv(data_list, csv_file) -> None:
    """
    Exports extracted data to a CSV file.

    :param data_list: A list of dictionaries containing data.
    :param csv_file: The path to the csv file.
    :return: None
    """
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'body', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quoting=csv.QUOTE_MINIMAL)

        writer.writeheader()
        writer.writerows(data_list)


if __name__ == "__main__":
    # Get the current directory where the script is located
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Define the folder containing the RTF files
    rtf_folder_name = "Rtf_files"
    # rtf_folder_name = "test"
    rtf_folder_path = os.path.join(script_directory, rtf_folder_name)

    # Define the output CSV file
    csv_output_file = 'csv_files/Bodegravencsvdata.csv'

    all_data = process_rtf_folder(rtf_folder_path)

    if all_data:
        export_to_csv(all_data, csv_output_file)
        print(f"Data from {len(all_data)} RTF files exported to "
              f"{csv_output_file}")
    else:
        print("No RTF files found in the folder.")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
