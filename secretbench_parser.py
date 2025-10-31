import os
import re
import csv

# Define the input and output CSV file paths
input_file_path = "dataset/shuffled_secretbench.csv"
directory_path = "Files"
start_row = 0  # Adjust for starting row (0-indexed)
end_row = 97478  # Adjust for ending row (exclusive)
max_file_size = 30 * 1024 * 1024 * 1024  # 10 GB in bytes
file_count = 1  # Counter for output files
paths_stored = 0

def read_file_content(file_path, encodings=["utf-8"], handle_unclosed_strings=True):
    """Reads file content while handling encoding errors, skipping non-printable characters, and optionally fixing unclosed strings."""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return None

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                if handle_unclosed_strings:
                    content = re.sub(r'"(?=$)', r'""', content, flags=re.MULTILINE)
                content = re.sub(r'[^\x00-\x7F]+', '', content)
                return content
        except UnicodeDecodeError:
            pass  # Continue trying other encodings

    print(f"Error: Unable to decode file '{file_path}' using any of the tried encodings. The file might be corrupt or use a custom encoding.")
    return None

def preprocess(text):
    # Preprocessing code here
    return text  # Return the processed text

def get_output_file_writer():
    global file_count, output_file_path, output_file, writer
    output_file_path = f"dataset/secretbench_merged_filecontents_{file_count}.csv"
    output_file = open(output_file_path, 'w', newline='', encoding="utf-8")
    writer = csv.writer(output_file, escapechar='\\')
    writer.writerow(["FileID", "Replink", "Filelink", "Contents", "Secret", "Label","Category"])  # Write header for output file
    file_count += 1

# Open the input CSV file in read mode
with open(input_file_path, 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)

    # Initialize the first output file writer
    get_output_file_writer()

    # Skip rows before the start
    for _ in range(start_row):
        next(reader, None)

    for row_num, row in enumerate(reader):
        print(f"Row Number: {start_row + row_num}")
        if row_num >= (end_row - start_row):
            break

        # Extract and concatenate field 23 and 24 as a file
        file_path = "/".join([directory_path, row[22]])
        print(file_path)

        try:
            # Read file content
            file_content = read_file_content(file_path)
            if file_content:
                # Optionally preprocess file content
                file_content = preprocess(file_content)

                file_id = paths_stored
                paths_stored += 1
                label = 1 if row[13] == "Y" else 0
                secret = row[1][1:-1]  # Remove surrounding quotes
                category = row[21]  # Extract the category column

                # Write to output file
                try:
                    writer.writerow([file_id, paths_stored, row[23], row[22], str(file_content), str(secret), label,category])
                    print(file_id)
                except Exception as write_error:
                    print(f"Skipping write error on row {row_num + start_row}: {write_error}")

                # Check if current file size exceeds the 10GB limit
                if output_file.tell() >= max_file_size:
                    output_file.close()  # Close current file
                    get_output_file_writer()  # Create a new output file

            else:
                print(f"Skipping: Unable to read content from {file_path}")

        except Exception as read_error:
            print(f"Skipping file {file_path} due to error: {read_error}")

    # Close the final output file after processing
    output_file.close()

print(f"Total files written: {file_count - 1}, Total contents processed: {paths_stored}")
