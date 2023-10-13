import os
import shutil
from chardet.universaldetector import UniversalDetector

# Путь к папке с файлами
folder_path = "uploads"  # Путь к папке с загруженными файлами

# Маппинг кодировок на папки
# noinspection PyDictDuplicateKeys
encoding_to_folder_map = {
    "ISO-8859-1": "ISO-8859-1",
    "ascii": "ANSI",
    "Windows-1251": "ANSI",
    "Shift_JIS": "Shift_JIS",
    "SHIFT_JIS": "Shift_JIS",
    "Windows-1252": "Windows-1252",
    "utf-8": "UTF-8",
    "UTF-16": "UTF-16",
    "utf-8": "UTF8",
    None: "Unknown"  # Добавлено для файлов с неопознанной кодировкой
}

# Получение списка файлов в папке
txt_files = [file for file in os.listdir(folder_path) if file.lower().endswith(".txt")]

if txt_files:
    print(f"Number of .txt files in the folder: {len(txt_files)}")

    # Создание папок для сортировки
    for folder_name in encoding_to_folder_map.values():
        folder = os.path.join(os.getcwd(), "Ready", folder_name)
        os.makedirs(folder, exist_ok=True)
        print(f"Folder '{folder}' created successfully.")

    # Обработка файлов
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        print(f"Processing file: {file_path}")

        try:
            # Если в файле есть определенные символы, предположим, что это SHIFT_JIS.
            shift_jis_symbols = ["„q", "„y", "„x", "„~", "„u", "„ѓ", "„Ѓ", "„p",
                                 "„‚", "„Ђ", "„|", "„Ћ", "„S", "‚ ", "‚И", "‚Ѕ",
                                 "‚М", "‰п", "€х", "‚Н",  "  ‚Е",  "‚·ЃB"]
            if any(symbol in open(file_path, 'r', errors='ignore').read() for symbol in shift_jis_symbols):
                encoding = "Shift_JIS"
            else:
                # Определение кодировки с помощью chardet
                detector = UniversalDetector()
                with open(file_path, 'rb') as file:
                    for line in file:
                        detector.feed(line)
                        if detector.done:
                            break
                detector.close()
                encoding = detector.result['encoding']

                print(f"Detected encoding for file '{file_path}': {encoding}")

                # Если файл обнаружен как ANSI и не содержит не-ASCII символов,
                # предположим, что это на самом деле UTF-8.
                if encoding == 'ISO-8859-1' and all(31 < byte < 128 for byte in open(file_path, 'rb').read()):
                    encoding = 'UTF-8'

            target_folder_name = encoding_to_folder_map.get(encoding, 'Unknown')
            # Используем 'Unknown', если кодировка не найдена

            target_folder = os.path.join(os.getcwd(), "Ready", target_folder_name)  # Путь к целевой папке в корневой директории
            target_file_path = os.path.join(target_folder, txt_file)
            shutil.copy(file_path, target_file_path)
            print(f"File '{file_path}' copied to '{target_file_path}'.")
        except Exception as e:
            print(f"An error occurred while processing a file: {e}")

# Удаление пустых папок
for folder_name in encoding_to_folder_map.values():
    folder = os.path.join(os.getcwd(), "Ready", folder_name)
    try:
        os.rmdir(folder)
        print(f"Empty folder '{folder}' removed successfully.")
    except OSError as e:
        print(f"Error: {folder} : {e.strerror}")
