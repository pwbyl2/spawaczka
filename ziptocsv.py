import zipfile
import os

# Specify the current working directory
current_directory = os.getcwd()

# Iterate through all files in the current directory
for file_name in os.listdir(current_directory):
    # Check if the file is a ZIP file
    if file_name.endswith('.zip'):
        # Create a full path to the ZIP file
        zip_file_path = os.path.join(current_directory, file_name)

        # Extract the name of the ZIP file without the extension
        base_name = os.path.splitext(file_name)[0]

        # Specify the destination directory where you want to save the extracted CSV file
        destination_directory = current_directory

        # Open the ZIP file in read mode
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            # Iterate through the files in the ZIP archive
            for file_info in zip_file.infolist():
                # Extract and rename each file to match the ZIP file's base name
                zip_file.extract(file_info, path=destination_directory)
                extracted_file_name = os.path.join(destination_directory, file_info.filename)
                new_file_name = os.path.join(destination_directory, f'{base_name}.csv')
                os.rename(extracted_file_name, new_file_name)
                print(f"Extracted {file_info.filename} as {base_name}.csv")

print("Extraction and renaming completed.")
