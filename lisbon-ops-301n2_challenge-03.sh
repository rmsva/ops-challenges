#!/bin/bash

# Script: Ops Challenge: Class 03
# Goal: Create a script that requires user input, to input a directory path and the desired chmod value, so it can change all file permissions in the target directory.
# Why: Further bash scripting practice combined with what I learned about chmod and automatization.

# Fetch script directory
script_directory=$(dirname "$0")

# Define log file path, so the output log file will always appear where the script is, instead of target directory
log_file="$script_directory/output_log.txt"

# Prompt the user to input a directory relative to the script location
echo "Enter target path:"
read directory_path

# Check if the entered path is a valid directory. If input is not (!) a valid directory (-d STRING), then it aborts the script with an error message
if [ ! -d "$directory_path" ]; then
    echo "Error: The directory '$directory_path' does not exist or is not a valid directory. Quitting..." | tee -a "$log_file"
    exit 1
fi

# Prompt the user to input chmod value
echo "Enter chmod value:"
read chmod_value

# Check if the entered chmod value is valid. If input is not a valid chmod value between 0 and 777, aborts the script with an error message
if ! [[ "$chmod_value" =~ ^[0-7]+$ ]]; then
    echo "Error: '$chmod_value' is not a valid chmod value. Enter a number between 0 and 777. Quitting..." | tee -a "$log_file"
    exit 1
fi

# Navigate to the input directory
cd "$directory_path" || exit

# Change the permission of all files in target directory to target chmod value
echo "Changing permissions of files in '$directory_path'..." | tee -a "$log_file"
for file in *; do
    if [ -f "$file" ]; then
        echo "Changing permission of file '$file'..." | tee -a "$log_file"
        sleep 1
        chmod "$chmod_value" "$file" | tee -a "$log_file"
    fi
done

echo "Permissions of all files in '$directory_path' have been changed to '$chmod_value'." | tee -a "$log_file"