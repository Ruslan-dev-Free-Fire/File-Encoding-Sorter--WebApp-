import os
import codecs
import sys

def convert_lines_from_ansi(lines):
    converted_lines = []
    for line in lines:
        try:
            # Convert the line from ANSI to Shift-JIS
            shift_jis_bytes = codecs.encode(line, 'Windows-1251')
            shift_jis_line = shift_jis_bytes.decode('shift_jis')
            converted_lines.append(shift_jis_line)
        except UnicodeEncodeError as e:
            print(f"Cannot encode line: {line.strip()}. Error: {str(e)}")
            # Handle the error here, for example, you could skip this line
            continue
    return converted_lines

def overwrite_file_with_content(file_path, content):
    try:
        # Write the content to the file, overwriting the existing data
        with codecs.open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(content)
        print(f"File '{file_path}' overwritten with converted content.")
    except Exception as e:
        print(f"Error while overwriting file: {file_path}. Error: {str(e)}")

def Krakozyabry_in_Japanese(file_path):
    try:
        # Read the content of the file with Shift_JIS encoding
        with codecs.open(file_path, 'r', encoding='Shift_JIS') as f:
            lines = f.readlines()

        # Display all the lines
        for line in lines:
            print(line)

        # Prompt for user confirmation
        user_input = input("Are the lines displayed correctly? (y/n): ")
        if user_input.lower() == 'n':
            print(f"File '{file_path}' not overwritten due to user confirmation.")
        else:
            # If confirmed, overwrite the original file with the converted lines
            overwrite_file_with_content(file_path, lines)

    except UnicodeDecodeError as e:
        print(f"Cannot decode file: {file_path}. Error: {str(e)}")
        print("You need another function to open this file")

def print_file_content(file_path):
    try:
        # Read the content of the file with utf-8 encoding
        with codecs.open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        converted_lines = convert_lines_from_ansi(lines)

        # Display all the converted lines
        for line in converted_lines:
            print(line)

        # Prompt for user confirmation
        user_input = input("Are the lines displayed correctly? (y/n): ")
        if user_input.lower() == 'n':
            # Log the cause of the problem and the original and decoded lines
            for i, line in enumerate(lines):
                print(f"Original line {i+1}: {line.strip()} → Decoded line: {converted_lines[i].strip()}")

        else:
            # If confirmed, overwrite the original file with the converted lines
            overwrite_file_with_content(file_path, converted_lines)

    except UnicodeDecodeError as e:
        Krakozyabry_in_Japanese(file_path)

if __name__ == "__main__":
    # The path to the "Fix_files" folder
    fix_files_folder = 'Ready'

    # Check if a file name was provided as a command line argument
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

        # Walk through all subfolders of the "Fix_files" folder
        for root, dirs, files in os.walk(fix_files_folder):
            if file_name in files:
                file_path = os.path.join(root, file_name)

                # Print the content of the file
                print_file_content(file_path)
                break
        else:
            print(f"File '{file_name}' does not exist.")
    else:
        print("Please provide a file name as a command line argument.")
