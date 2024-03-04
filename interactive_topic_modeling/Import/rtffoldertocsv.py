import csv
import os
from striprtf.striprtf import rtf_to_text


# this is a standalone script for generating  a csv file from a folder with rtf files
# those rtf files are exported from lexus nexus and have a specific layout
# so this won't work with other files


def extract_data_from_rtf_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as rtf_file:
            rtf_content = rtf_file.read()

        # Using striprtf to extract plain text from RTF content
        body = rtf_to_text(rtf_content)

        # Extracting title from the first non-empty line
        lines = body.split('\n')
        title1_index = next(
            index for index, line in enumerate(lines) if line.strip())  # Index of the first non-empty line

        title1 = lines[title1_index].strip()  # Get the title from the first non-empty line

        # Check if the next index exists and has leading space, then append it to title1
        title1_end_index = title1_index
        if title1_index + 1 < len(lines) and lines[title1_index + 1].startswith(' '):
            title1 += ' ' + lines[title1_index + 1].strip()
            title1_end_index = title1_index + 1

        # Check if there are enough lines
        if len(lines) < title1_end_index + 3:
            print(f"Skipping file {file_path} - Not enough lines to extract data")
            return None  # or return {}

        # Extracting date from the second line after the title
        date = lines[title1_end_index+2]
        date = date.lstrip(',')  # Remove leading `",`
        date = date.strip('"')  # Remove trailing '"'

        # Remove surrounding quotations from the title
        title = title1.strip('"').strip("'")

        # Extracting body from the line 'Body' to 'Graphic' (or 'Classification' if 'Graphic' is missing)
        start_index = lines.index('Body') + 1 if 'Body' in lines else 0
        end_index = len(lines)
        for section in ['Graphic', 'Classification']:
            if section in lines:
                end_index = lines.index(section)
                break

        # filter the empty lines out of the body before joining it together
        body_content = '\n'.join(filter(''.__ne__, lines[start_index:end_index]))

        # Remove newlines from body_content
        body_content = body_content.replace('\n', ' ')

        return {'title': title, 'body': body_content, 'date': date}
    except UnicodeDecodeError:
        print(f"Skipping file {file_path} - UnicodeDecodeError")
        return None  # or return {}


def process_rtf_folder(folder_path):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.rtf'):
            rtf_file_path = os.path.join(folder_path, filename)
            extracted_data = extract_data_from_rtf_file(rtf_file_path)
            if extracted_data is not None:
                all_data.append(extracted_data)

    # Remove duplicates based on 'title', 'body', and 'date'
    unique_data = [dict(t) for t in {tuple(d.items()) for d in all_data if d is not None}]
    return unique_data


def export_to_csv(data_list, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'body', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)

        writer.writeheader()
        writer.writerows(data_list)


if __name__ == "__main__":
    # Get the current directory where the script is located
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Define the folder containing the RTF files
    rtf_folder_name = "Rtf_files"
    #rtf_folder_name = "test"
    rtf_folder_path = os.path.join(script_directory, rtf_folder_name)

    # Define the output CSV file
    csv_output_file = 'Bodegravencsvdata.csv'
    #csv_output_file = 'test.csv'

    all_data = process_rtf_folder(rtf_folder_path)

    if all_data:
        export_to_csv(all_data, csv_output_file)
        print(f"Data from {len(all_data)} RTF files exported to {csv_output_file}")
    else:
        print("No RTF files found in the folder.")