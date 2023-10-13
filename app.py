from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO
import os
import subprocess
from flask import send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Замените 'your_secret_key_here' на секретный ключ


# Указываем папку для загрузки файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Максимальный размер загружаемых файлов (в байтах)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Например, 16 MB

socketio = SocketIO(app)

# Функция для проверки разрешенных расширений файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'


@app.route('/download')
def download_file():
    return send_from_directory('Ready', 'Completed_files.zip')


@app.route('/sort_files', methods=['GET', 'POST'])
def sort_files():
    if request.method == 'POST':
        # Your current code for handling POST requests
        pass
    else:
        # Processing GET requests
        try:
            subprocess.run(['python', 'C:\\MyCode\\Python\\Ruslan-dev-Free-Fire_Site\\file_sorter.py'], check=True)
            # Return the URL of the created archive
            return 'Sorting completed successfully. Download the sorted files <a href="/download">here</a>.'
        except subprocess.CalledProcessError as e:
            return f'Error during sorting: {e}'



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/file_encoding_sorter', methods=['GET', 'POST'])
def file_encoding_sorter():
    if request.method == 'POST':
        # Проверка, был ли выбран файл
        if 'file' not in request.files:
            flash('File not selected', 'error')
            return redirect(request.url)

        file = request.files['file']

        # Если пользователь не выбрал файл, браузер отправит пустое поле без имени файла
        if file.filename == '':
            flash('File not selected', 'error')
            return redirect(request.url)

        # Проверка разрешенных расширений файла
        if not allowed_file(file.filename):
            flash('Only files with the extension .txt are allowed', 'error')
            return redirect(request.url)

        # Если файл прошел все проверки, сохраняем его
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully', 'success')
            # Здесь вы можете провести дополнительную обработку файла, если это необходимо

    return render_template('file_encoding_sorter.html')

@socketio.on('run_script')
def run_script():
    try:
        subprocess.call(['python', 'file_sorter.py'])  # Замените 'file_sorter.py' на путь к вашему скрипту
        download_link = url_for('download_file')
        result_message = 'Sorting completed successfully. Download the sorted files <a href="{}">here</a>.'.format(download_link)
        socketio.emit('script_result', result_message)
    except Exception as e:
        socketio.emit('script_result', f'Error during sorting: {e}')


if __name__ == '__main__':
    socketio.run(app, debug=True)
