import os
import shutil
from zipfile import ZipFile
from chardet.universaldetector import UniversalDetector

# Путь к основной папке с файлами
base_folder_path = "uploads"  # Путь к папке с загруженными файлами

# Маппинг кодировок на папки
encoding_to_folder_map = {
    "ISO-8859-1": "ISO-8859-1",
    "ascii": "ANSI",
    "Windows-1251": "ANSI",
    "Shift_JIS": "Shift_JIS",
    "SHIFT_JIS": "Shift_JIS",
    "Windows-1252": "Windows-1252",
    "utf-8": "UTF-8",
    "UTF-16": "UTF-16",
    None: "Unknown"
}

# Получение списка подпапок в папке uploads
user_folders = [os.path.join(base_folder_path, folder) for folder in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, folder))]

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

