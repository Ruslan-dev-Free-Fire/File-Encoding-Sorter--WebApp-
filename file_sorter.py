import os
import shutil
from zipfile import ZipFile
import logging
from chardet.universaldetector import UniversalDetector
import subprocess
import argparse



def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--fix_encodings', type=str2bool, default=False,
                    help='Fix incorrect encodings')
parser.add_argument('--separate_folder', type=str2bool, default=False,
                    help='Place the corrected files in a separate folder')
parser.add_argument('--only_correction', type=str2bool, default=False,
                    help='File correction only (no sorting)')

args = parser.parse_args()
print(args)


# Set up logging
logging.basicConfig(filename='file_processing.log', level=logging.INFO)

# Path to the main folder with files
base_folder_path = "uploads"

# Mapping encodings to folders
encoding_to_folder_map = {
    "ISO-8859-1": "ISO-8859-1",
    "ascii": "ANSI",
    "Windows-1251": "Windows-1251",
    "SHIFT_JIS": "Shift_JIS",
    "Windows-1252": "Windows-1252",
    "utf-8": "UTF-8",
    "UTF-16": "UTF-16",
    None: "Unknown"
}

# Get a list of subfolders in the uploads folder
user_folders = [os.path.join(base_folder_path, folder) for folder in os.listdir(base_folder_path) if
                os.path.isdir(os.path.join(base_folder_path, folder))]


# Check for specific characters in the file




# Сортировка по умолчанию
def standard_sorting(user_folders, encoding_to_folder_map):
    print("Запуск функции сортировки по умолчанию")  # Выводим сообщение в консоль
    for user_folder_path in user_folders:
        # Создание уникальной папки внутри папки Ready для каждого пользователя
        user_ready_folder = os.path.join('Ready', os.path.basename(user_folder_path))
        os.makedirs(user_ready_folder, exist_ok=True)

        txt_files = [file for file in os.listdir(user_folder_path) if file.lower().endswith(".txt")]

        if txt_files:
            print(f"Number of .txt files in folder '{user_folder_path}': {len(txt_files)}")

            for txt_file in txt_files:
                file_path = os.path.join(user_folder_path, txt_file)
                print(f"Processing file: {file_path}")

                try:
                    # Определение кодировки файла с помощью chardet
                    detector = UniversalDetector()
                    with open(file_path, 'rb') as file:
                        for line in file:
                            detector.feed(line)
                            if detector.done:
                                break
                    detector.close()
                    encoding = detector.result['encoding']

                    print(f"Detected encoding for file '{file_path}': {encoding}")

                    target_folder_name = encoding_to_folder_map.get(encoding, 'Unknown')

                    # Создание папки для каждой кодировки внутри уникальной папки пользователя
                    target_folder = os.path.join(user_ready_folder, target_folder_name)
                    os.makedirs(target_folder, exist_ok=True)

                    target_file_path = os.path.join(target_folder, txt_file)
                    shutil.copy(file_path, target_file_path)
                    print(f"File '{file_path}' copied to '{target_file_path}'.")
                except Exception as e:
                    print(f"An error occurred while processing a file: {e}")

            # Создание архива с обработанными файлами в уникальной папке пользователя
            archive_name = f'Completed_files_{os.path.basename(user_folder_path)}.zip'
            with ZipFile(os.path.join(user_ready_folder, archive_name), 'w') as zipf:
                for encoding_folder in encoding_to_folder_map.values():
                    encoding_folder_path = os.path.join(user_ready_folder, encoding_folder)
                    if os.path.exists(encoding_folder_path):
                        for filename in os.listdir(encoding_folder_path):
                            if not filename.endswith('.zip'):  # Исключаем файлы .zip
                                full_file_path = os.path.join(encoding_folder_path, filename)
                                # Добавляем файл в архив с указанием относительного пути
                                zipf.write(full_file_path, arcname=os.path.join(encoding_folder, filename))

            print(f"Archive '{user_ready_folder}/{archive_name}' created successfully.")

            # Удаление исходных файлов из уникальной папки пользователя после создания архива
            for filename in os.listdir(user_ready_folder):
                file_path = os.path.join(user_ready_folder, filename)
                try:
                    if os.path.isfile(file_path) and file_path.endswith('.txt'):  # Удаляем только .txt файлы
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

            print("All source files deleted successfully.")


# Сортировка True True False
def sort_and_fix_folder(user_folders, encoding_to_folder_map):
    print("Запуск функции сортировки с папкой Fix")  # Выводим сообщение в консоль
    def check_for_specific_chars(file_path, chars):
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            content = f.read()
            for char in chars:
                if char in content:
                    return True
        return False

    for user_folder_path in user_folders:
        user_ready_folder = os.path.join('Ready', os.path.basename(user_folder_path))
        os.makedirs(user_ready_folder, exist_ok=True)

        txt_files = [file for file in os.listdir(user_folder_path) if file.lower().endswith(".txt")]

        if txt_files:
            print(f"Number of .txt files in folder '{user_folder_path}': {len(txt_files)}")

            for txt_file in txt_files:
                file_path = os.path.join(user_folder_path, txt_file)
                logging.info(f"Processing file: {file_path}")
                print(f"Processing file: {file_path}")

                try:
                    detector = UniversalDetector()
                    with open(file_path, 'rb') as f:
                        for line in f:
                            detector.feed(line)
                            if detector.done:
                                break
                    detector.close()
                    encoding = detector.result['encoding']

                    print(f"Detected encoding for file '{file_path}': {encoding}")

                    target_folder_name = encoding_to_folder_map.get(encoding, 'Unknown')

                    target_folder = os.path.join(user_ready_folder, target_folder_name)
                    os.makedirs(target_folder, exist_ok=True)

                    target_file_path = os.path.join(target_folder, txt_file)
                    shutil.copy(file_path, target_file_path)
                    logging.info(f"File '{file_path}' copied to '{target_file_path}'.")
                    print(f"File '{file_path}' copied to '{target_file_path}'.")

                    specific_chars = "ѓќѓѓCѓѓѓѓЏЃѓЋЌ†ѓЃѓЃЃyЊЋЉz—ї‹аМІ€Д“аЃz"
                    if target_folder_name in ["Shift_JIS", "UTF-8", "Windows-1251", "Unknown",
                                              "Windows-1252"] and check_for_specific_chars(target_file_path,
                                                                                           specific_chars):
                        fix_files_folder = os.path.join(user_ready_folder, 'Fix_files')
                        os.makedirs(fix_files_folder, exist_ok=True)

                        filename_without_extension, extension = os.path.splitext(txt_file)
                        new_target_file_path = os.path.join(fix_files_folder,
                                                            filename_without_extension + '_fix' + extension)
                        shutil.move(target_file_path, new_target_file_path)
                        print(f"File '{target_file_path}' moved to '{new_target_file_path}'.")

                        # Вызываем скрипт 'File_fixer.py'
                        subprocess.check_call(['python', 'File_fixer.py'])
                except Exception as e:
                    print(f"An error occurred while processing a file: {e}")

        # Create an archive with processed files in the user's unique folder
        archive_name = f'Completed_files_{os.path.basename(user_ready_folder)}.zip'
        with ZipFile(os.path.join(user_ready_folder, archive_name), 'w') as zipf:
            for folder_name in os.listdir(user_ready_folder):
                folder_path = os.path.join(user_ready_folder, folder_name)
                if os.path.isdir(folder_path):
                    for filename in os.listdir(folder_path):
                        if not filename.endswith('.zip'):  # Exclude .zip files
                            full_file_path = os.path.join(folder_path, filename)
                            # Add file to archive with relative path
                            zipf.write(full_file_path, arcname=os.path.join(folder_name, filename))

        print(f"Archive '{user_ready_folder}/{archive_name}' created successfully.")

        # Delete source files from the user's unique folder after creating the archive
        for filename in os.listdir(user_ready_folder):
            file_path = os.path.join(user_ready_folder, filename)
            try:
                if os.path.isfile(file_path) and not file_path.endswith('.zip'):  # Delete only non-.zip files
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


# Сортировка True False False
def sort_and_not_fix_folder(user_folders, encoding_to_folder_map):
    print("Запуск функции сортировки и исправления без папки Fix")  # Выводим сообщение в консоль
    # Check for specific characters in the file
    def check_for_specific_chars(file_path, chars):
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            content = f.read()
            for char in chars:
                if char in content:
                    return True
        return False

    # Process files and remove duplicates
    for user_folder_path in user_folders:
        # Create a unique folder inside the Ready folder for each user
        user_ready_folder = os.path.join('Ready', os.path.basename(user_folder_path))
        os.makedirs(user_ready_folder, exist_ok=True)

        txt_files = [file for file in os.listdir(user_folder_path) if file.lower().endswith(".txt")]

        if txt_files:
            print(f"Number of .txt files in folder '{user_folder_path}': {len(txt_files)}")

            for txt_file in txt_files:
                file_path = os.path.join(user_folder_path, txt_file)
                logging.info(f"Processing file: {file_path}")
                print(f"Processing file: {file_path}")

                try:
                    # Determine the encoding of the file
                    detector = UniversalDetector()
                    with open(file_path, 'rb') as f:
                        for line in f:
                            detector.feed(line)
                            if detector.done:
                                break
                    detector.close()
                    encoding = detector.result['encoding']

                    print(f"Detected encoding for file '{file_path}': {encoding}")

                    target_folder_name = encoding_to_folder_map.get(encoding, 'Unknown')

                    # Create a folder for each encoding inside the user's unique folder
                    target_folder = os.path.join(user_ready_folder, target_folder_name)
                    os.makedirs(target_folder, exist_ok=True)

                    target_file_path = os.path.join(target_folder, txt_file)
                    shutil.copy(file_path, target_file_path)
                    logging.info(f"File '{file_path}' copied to '{target_file_path}'.")
                    print(f"File '{file_path}' copied to '{target_file_path}'.")

                    # Check for specific characters and process the file if condition is met
                    specific_chars = "ѓќѓѓCѓѓѓѓЏЃѓЋЌ†ѓЃѓЃЃyЊЋЉz—ї‹аМІ€Д“аЃz"
                    if target_folder_name in ["Shift_JIS", "UTF-8", "Windows-1251", "Unknown",
                                              "Windows-1252"] and check_for_specific_chars(target_file_path,
                                                                                           specific_chars):
                        fix_files_folder = os.path.join(user_ready_folder, 'Fix_files')
                        os.makedirs(fix_files_folder, exist_ok=True)

                        filename_without_extension, extension = os.path.splitext(txt_file)
                        new_target_file_path = os.path.join(fix_files_folder,
                                                            filename_without_extension + '_fix' + extension)
                        shutil.move(target_file_path, new_target_file_path)
                        print(f"File '{target_file_path}' moved to '{new_target_file_path}'.")

                        # Вызываем скрипт 'File_fixer.py'
                        subprocess.call(['python', 'File_fixer.py'])

                        # После исправления файлов перемещаем их обратно в исходную папку
                        shutil.move(new_target_file_path, target_file_path)
                        print(f"File '{new_target_file_path}' moved back to '{target_file_path}'.")

                        # Удаляем папку 'Fix_files' после обработки всех файлов
                        shutil.rmtree(os.path.join(user_ready_folder, 'Fix_files'))
                        print("Folder 'Fix_files' has been removed.")
                except Exception as e:
                    print(f"An error occurred while processing a file: {e}")

        # Create an archive with processed files in the user's unique folder
        archive_name = f'Completed_files_{os.path.basename(user_ready_folder)}.zip'
        with ZipFile(os.path.join(user_ready_folder, archive_name), 'w') as zipf:
            for folder_name in os.listdir(user_ready_folder):
                folder_path = os.path.join(user_ready_folder, folder_name)
                if os.path.isdir(folder_path):
                    for filename in os.listdir(folder_path):
                        if not filename.endswith('.zip'):  # Exclude .zip files
                            full_file_path = os.path.join(folder_path, filename)
                            # Add file to archive with relative path
                            zipf.write(full_file_path, arcname=os.path.join(folder_name, filename))

        print(f"Archive '{user_ready_folder}/{archive_name}' created successfully.")

        # Delete source files from the user's unique folder after creating the archive
        for filename in os.listdir(user_ready_folder):
            file_path = os.path.join(user_ready_folder, filename)
            try:
                if os.path.isfile(file_path) and not file_path.endswith('.zip'):  # Delete only non-.zip files
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


def no_sort_and_not_fix_folder(user_folders, encoding_to_folder_map):
    print("Запуск функции без сортировки и только исправление")  # Выводим сообщение в консоль

    # Process files and remove duplicates
    def check_for_specific_chars(file_path, chars):
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            content = f.read()
            for char in chars:
                if char in content:
                    return True
        return False

    # Process files and remove duplicates
    for user_folder_path in user_folders:
        # Create a unique folder inside the Ready folder for each user
        user_ready_folder = os.path.join('Ready', os.path.basename(user_folder_path))
        os.makedirs(user_ready_folder, exist_ok=True)

        txt_files = [file for file in os.listdir(user_folder_path) if file.lower().endswith(".txt")]

        if txt_files:
            print(f"Number of .txt files in folder '{user_folder_path}': {len(txt_files)}")

            for txt_file in txt_files:
                file_path = os.path.join(user_folder_path, txt_file)
                logging.info(f"Processing file: {file_path}")
                print(f"Processing file: {file_path}")

                try:
                    # Determine the encoding of the file
                    detector = UniversalDetector()
                    with open(file_path, 'rb') as f:
                        for line in f:
                            detector.feed(line)
                            if detector.done:
                                break
                    detector.close()
                    encoding = detector.result['encoding']

                    print(f"Detected encoding for file '{file_path}': {encoding}")

                    target_folder_name = encoding_to_folder_map.get(encoding, 'Unknown')

                    # Create a folder for each encoding inside the user's unique folder
                    target_folder = os.path.join(user_ready_folder, target_folder_name)
                    os.makedirs(target_folder, exist_ok=True)

                    target_file_path = os.path.join(target_folder, txt_file)
                    shutil.copy(file_path, target_file_path)
                    logging.info(f"File '{file_path}' copied to '{target_file_path}'.")
                    print(f"File '{file_path}' copied to '{target_file_path}'.")

                    # Check for specific characters and process the file if condition is met
                    specific_chars = "ѓќѓѓCѓѓѓѓЏЃѓЋЌ†ѓЃѓЃЃyЊЋЉz—ї‹аМІ€Д“аЃz"
                    if target_folder_name in ["Shift_JIS", "UTF-8", "Windows-1251", "Unknown",
                                              "Windows-1252"] and check_for_specific_chars(target_file_path,
                                                                                           specific_chars):
                        fix_files_folder = os.path.join(user_ready_folder, 'Fix_files')
                        os.makedirs(fix_files_folder, exist_ok=True)

                        filename_without_extension, extension = os.path.splitext(txt_file)
                        new_target_file_path = os.path.join(fix_files_folder,
                                                            filename_without_extension + '_fix' + extension)
                        shutil.move(target_file_path, new_target_file_path)
                        print(f"File '{target_file_path}' moved to '{new_target_file_path}'.")

                        # Вызываем скрипт 'File_fixer.py'
                        subprocess.call(['python', 'File_fixer.py'])

                        # После исправления файлов перемещаем их обратно в исходную папку
                        shutil.move(new_target_file_path, target_file_path)
                        print(f"File '{new_target_file_path}' moved back to '{target_file_path}'.")

                        # Удаляем папку 'Fix_files' после обработки всех файлов
                        shutil.rmtree(os.path.join(user_ready_folder, 'Fix_files'))
                        print("Folder 'Fix_files' has been removed.")
                except Exception as e:
                    print(f"An error occurred while processing a file: {e}")

        # Move files from subfolders to the user's unique folder
        for folder_name in os.listdir(user_ready_folder):
            folder_path = os.path.join(user_ready_folder, folder_name)
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    new_file_path = os.path.join(user_ready_folder, filename)
                    shutil.move(file_path, new_file_path)
                    print(f"File '{file_path}' moved to '{new_file_path}'.")

        # Delete empty folders
        for folder_name in os.listdir(user_ready_folder):
            folder_path = os.path.join(user_ready_folder, folder_name)
            if os.path.isdir(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f"Empty folder '{folder_path}' deleted.")

        # Create an archive with processed files in the user's unique folder
        archive_name = f'Completed_files_{os.path.basename(user_ready_folder)}.zip'
        with ZipFile(os.path.join(user_ready_folder, archive_name), 'w') as zipf:
            for filename in os.listdir(user_ready_folder):
                file_path = os.path.join(user_ready_folder, filename)
                if os.path.isfile(file_path) and not file_path.endswith('.zip'):  # Exclude .zip files
                    # Add file to archive with relative path
                    zipf.write(file_path, arcname=filename)

        print(f"Archive '{user_ready_folder}/{archive_name}' created successfully.")

        # Delete remaining files in the current session folder
        for filename in os.listdir(user_ready_folder):
            file_path = os.path.join(user_ready_folder, filename)
            try:
                if os.path.isfile(file_path) and not file_path.endswith('.zip'):  # Delete only non-.zip files
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


def no_sort_and_fix_folder(user_folders, encoding_to_folder_map):
    print("Запуск функции без сортировки и только папка Fix Folder")  # Выводим сообщение в консоль

    # Process files and remove duplicates
    def check_for_specific_chars(file_path, chars):
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            content = f.read()
            for char in chars:
                if char in content:
                    return True
        return False

    # Process files and remove duplicates
    for user_folder_path in user_folders:
        # Create a unique folder inside the Ready folder for each user
        user_ready_folder = os.path.join('Ready', os.path.basename(user_folder_path))
        os.makedirs(user_ready_folder, exist_ok=True)

        txt_files = [file for file in os.listdir(user_folder_path) if file.lower().endswith(".txt")]

        if txt_files:
            print(f"Number of .txt files in folder '{user_folder_path}': {len(txt_files)}")

            for txt_file in txt_files:
                file_path = os.path.join(user_folder_path, txt_file)
                logging.info(f"Processing file: {file_path}")
                print(f"Processing file: {file_path}")

                try:
                    # Determine the encoding of the file
                    detector = UniversalDetector()
                    with open(file_path, 'rb') as f:
                        for line in f:
                            detector.feed(line)
                            if detector.done:
                                break
                    detector.close()
                    encoding = detector.result['encoding']

                    print(f"Detected encoding for file '{file_path}': {encoding}")

                    target_folder_name = encoding_to_folder_map.get(encoding, 'Unknown')

                    # Create a folder for each encoding inside the user's unique folder
                    target_folder = os.path.join(user_ready_folder, target_folder_name)
                    os.makedirs(target_folder, exist_ok=True)

                    target_file_path = os.path.join(target_folder, txt_file)
                    shutil.copy(file_path, target_file_path)
                    logging.info(f"File '{file_path}' copied to '{target_file_path}'.")
                    print(f"File '{file_path}' copied to '{target_file_path}'.")

                    # Check for specific characters and process the file if condition is met
                    specific_chars = "ѓќѓѓCѓѓѓѓЏЃѓЋЌ†ѓЃѓЃЃyЊЋЉz—ї‹аМІ€Д“аЃz"
                    if target_folder_name in ["Shift_JIS", "UTF-8", "Windows-1251", "Unknown",
                                              "Windows-1252"] and check_for_specific_chars(target_file_path,
                                                                                           specific_chars):
                        fix_files_folder = os.path.join(user_ready_folder, 'Fix_files')
                        os.makedirs(fix_files_folder, exist_ok=True)

                        filename_without_extension, extension = os.path.splitext(txt_file)
                        new_target_file_path = os.path.join(fix_files_folder,
                                                            filename_without_extension + '_fix' + extension)
                        shutil.move(target_file_path, new_target_file_path)
                        print(f"File '{target_file_path}' moved to '{new_target_file_path}'.")

                        # Вызываем скрипт 'File_fixer.py'
                        subprocess.run(['python', 'File_fixer.py'])
                except Exception as e:
                    print(f"An error occurred while calling the script: {e}")

    # Move files from subfolders to the user's unique folder
    for folder_name in os.listdir(user_ready_folder):
        folder_path = os.path.join(user_ready_folder, folder_name)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"Empty folder '{folder_path}' deleted.")  # Deletion of empty folders

        # Create an archive with processed files in the user's unique folder
        archive_name = f'Completed_files_{os.path.basename(user_ready_folder)}.zip'
        with ZipFile(os.path.join(user_ready_folder, archive_name), 'w') as zipf:
            for root, dirs, files in os.walk(user_ready_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not file_path.endswith('.zip'):  # Exclude .zip files
                        # Add file to archive with relative path
                        zipf.write(file_path, arcname=os.path.relpath(file_path, user_ready_folder))

        print(f"Archive '{user_ready_folder}/{archive_name}' created successfully.")

        # Delete remaining files in the current session folder
        for filename in os.listdir(user_ready_folder):
            file_path = os.path.join(user_ready_folder, filename)
            try:
                if os.path.isfile(file_path) and not file_path.endswith('.zip'):  # Delete only non-.zip files
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')  # Deletion of remaining files and folders


# Разберите аргументы
args = parser.parse_args()

# Теперь вы можете использовать эти аргументы в вашем коде
if not args.fix_encodings and not args.separate_folder and not args.only_correction:
    # Запустите функцию standard_sorting, если все аргументы равны False
    standard_sorting(user_folders, encoding_to_folder_map)
if args.fix_encodings and args.separate_folder and not args.only_correction:
    sort_and_fix_folder(user_folders, encoding_to_folder_map)
if args.fix_encodings and not args.separate_folder and not args.only_correction:
    sort_and_not_fix_folder(user_folders, encoding_to_folder_map)
if args.fix_encodings and not args.separate_folder and args.only_correction:
    no_sort_and_not_fix_folder(user_folders, encoding_to_folder_map)
if args.fix_encodings and args.separate_folder and args.only_correction:
    no_sort_and_fix_folder(user_folders, encoding_to_folder_map)