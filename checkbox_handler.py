
from flask import Flask, request
import subprocess

# Получаем значения чекбоксов
data = request.get_json()
fix_encoding = data.get('fixEncoding', False)
corrected_files = data.get('correctedFiles', False)
file_correction_only = data.get('fileCorrectionOnly', False)

# Вызываем file_sorter.py и передаем значения чекбоксов как аргументы
subprocess.call(['python', 'file_sorter.py', str(fix_encoding), str(corrected_files), str(file_correction_only)])
