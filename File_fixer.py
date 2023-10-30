import os
import codecs
from chardet.universaldetector import UniversalDetector
from other_fixer import print_file_content

def rewrite_file_content(file_path):
    # Determine the encoding of the file
    detector = UniversalDetector()
    with open(file_path, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    encoding = detector.result['encoding']

    # If the file is from the 'Windows-1252' folder, convert it to 'Shift_JIS'
    if 'Windows-1252' in file_path:
        new_encoding = 'Shift_JIS'
    else:
        new_encoding = 'utf-8'

    try:
        # Read the content of the file with the detected encoding
        with codecs.open(file_path, 'r', encoding=encoding) as f:
            content = f.read()

        # Check if there is at least one Japanese character in the content
        japanese_chars = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
        if any(char in content for char in japanese_chars):
            # Write the content back to the file with the new encoding
            with codecs.open(file_path, 'w', encoding=new_encoding, errors='ignore') as f:
                f.write(content)
            return True

        # Check if there are specific unreadable characters in the content
        specific_chars = "ѓќѓѓѓѓѓѓЏЃѓЋЌÑ†ѓЃѓЃЃЊЋЉ—ї„‹І€“Ѓ"
        unreadable_chars_in_file = [char for char in specific_chars if char in content]
        if unreadable_chars_in_file:
            print(f"Specific unreadable characters found in file: {file_path}. Characters: {' '.join(unreadable_chars_in_file)}")
            return False

        # Write the content back to the file with the new encoding
        with codecs.open(file_path, 'w', encoding=new_encoding, errors='ignore') as f:
            f.write(content)
    except UnicodeDecodeError as e:
        print(f"Cannot decode file: {file_path}. Error: {str(e)}")
        return False

    return True


def list_of_problem_files(files):
    for file_path in files:
        success = print_file_content(file_path)
        if not success:
            print(f"File {file_path} could not be processed.")

if __name__ == "__main__":
    # The path to the "Ready" folder
    ready_folder = os.path.abspath('Ready')

    # Create a list to store files that could not be decoded
    undecodable_files = []

    # Walk through all session folders in the "Ready" folder
    for session_folder in os.listdir(ready_folder):
        session_folder_path = os.path.join(ready_folder, session_folder)

        # Check if it's a directory, not a file
        if os.path.isdir(session_folder_path):
            fix_files_folder = os.path.join(session_folder_path, 'Fix_files')

            # Check if the "Fix_files" folder exists in the session folder
            if os.path.exists(fix_files_folder):
                # Walk through all files in the "Fix_files" folder of the session
                for root, dirs, files in os.walk(fix_files_folder):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)

                        # Rewrite the content of the file with utf-8 encoding
                        success = rewrite_file_content(file_path)
                        if not success:
                            undecodable_files.append(file_path)

    # If there are no undecodable files, print a success message. Otherwise, print a list of undecodable files.
    if len(undecodable_files) == 0:
        print("All files have been successfully fixed.")
    else:
        print("The following files could not be decoded:")
        for file_path in undecodable_files:
            print(file_path)

    # Call list_of_problem_files with the list of undecodable files
    list_of_problem_files(undecodable_files)
