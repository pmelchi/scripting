#!/bin/bash

# Function to create a folder if it doesn't exist
create_folder() {
    local folder="$1"
    if [ ! -d "$folder" ]; then
        mkdir -p "$folder"
        echo "Created folder: $folder"
    else
        echo "Folder already exists: $folder"
    fi
}

input_folder="$1"

# Verify if input_folder is provided
if [ -z "$1" ]; then
    echo "Please provide the input folder as an argument."
    echo "Usage: ./multi-cap2hccapx.sh <input_folder>"
    exit 1
fi

archive_folder="$input_folder/output"
hccapx_folder="$input_folder/hccapx"
hashcat_utils="/home/pablo/Downloads/hashcat-utils-1.9"  # Update the path accordingly

# Check if folders exists
create_folder "$archive_folder"
create_folder "$hccapx_folder"

# Loop through files in the folder
for file in $(find "$input_folder" -type f); do
    # Process each file here
    echo "Processing file: $file"
    # Add your code to process the file
    filename=$(basename "$file")
    filename_without_extension="${filename%.*}"
    output_file="$hccapx_folder/$filename_without_extension.hccapx"

    # Use the hashcat-utils variable to execute the command
    "$hashcat_utils/bin/cap2hccapx.bin" "$file" "$output_file"
done