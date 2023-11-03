import json
import os
import subprocess
import time
import uuid
import logging
from flask import Flask, session, make_response
from flask import Flask, request, jsonify
from flask import render_template, redirect, url_for, flash
from flask import request
from flask import send_from_directory
from flask_mail import Mail, Message
from flask_sock import Sock
from werkzeug.utils import secure_filename

#from flask_talisman import Talisman

app = Flask(__name__)
sock = Sock(app)
app.logger.setLevel(logging.INFO)


#csp = {
#    'default-src': [
#        '\'self\'',
#        'http://127.0.0.1:5000',  # Добавленный URL в белый список
#        'https://code.jquery.com',
#        'https://cdn.jsdelivr.net/npm/sockjs-client@1/dist/sockjs.min.js',
#        'https://fonts.googleapis.com/css?family=Karla:400,700&display=swap',
#        'https://kit.fontawesome.com/2a20f3910e.js',
#        'https://unpkg.com/aos@next/dist/aos.css'
#    ],
#    'upgrade-insecure-requests': []  # Добавляем директиву "upgrade-insecure-requests"
#}

#talisman = Talisman(app, content_security_policy=csp)

app.config['SECRET_KEY'] = 'your_secret_key_here'  # Замените 'your_secret_key_here' на секретный ключ

# Для уникальной сессии
app.secret_key = 'your_secret_key_here'

# Указываем папку для загрузки файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Максимальный размер загружаемых файлов (в байтах)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Например, 16 MB


@app.route('/web-app-settings', methods=['POST'])
def web_app_settings():
    # Здесь вы можете обработать данные запроса, например, изменить настройки

    # Возвращаем JSON-ответ
    return jsonify(message='Your settings have been successfully changed')


@app.route('/log', methods=['POST'])
def log_message():
    data = request.get_json()
    message = data.get('message', '')
    app.logger.info(message)

    # Разбиваем сообщение на части и извлекаем аргументы
    args = message.split(' ')

    # Запускаем скрипт с аргументами
    subprocess.run(['python', 'file_sorter.py'] + args)

    return jsonify({'message': 'Message logged successfully.'}), 200


@sock.route('/sockjs')
def sockjs(sock):
    while True:
        msg = sock.receive()
        print(msg)
        if msg == 'run_script':
            try:
                return_code = subprocess.call(['python', 'file_sorter.py'])  # Замените 'file_sorter.py' на путь к вашему скрипту

                # Получаем идентификатор сессии из session['user_folder']
                session_id = os.path.basename(session['user_folder'])

                if return_code == 0:
                    download_link = url_for('download_file', session_id=session_id)
                    result_message = 'Sorting completed successfully. Download the sorted files <a href="{}">here</a>.'.format(download_link)
                else:
                    result_message = 'No files to sort.'

                sock.send(result_message)

                # Отправляем идентификатор сессии обратно клиенту
                sock.send(json.dumps({'session_id': session_id}))
            except Exception as e:
                sock.send(f'Error during sorting: {e}')


# Функция для проверки разрешенных расширений файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'

@app.route('/download/<session_id>')
def download_file(session_id):
    return send_from_directory('Ready/' + session_id, 'Completed_files.zip')


# Функция отправки запроса на кнопку для выполнения скрипта сортировки
@app.route('/sort_files', methods=['GET', 'POST'])
def sort_files():
    if request.method == 'POST':
        if 'user_folder' in session:
            session_id = os.path.basename(session['user_folder'])
            if not os.path.exists(session['user_folder']):
                return jsonify(message='No files to sort')
            elif not os.listdir(session['user_folder']):
                return jsonify(message='No files to sort')
        else:
            return jsonify(message='No files to sort')

        try:
            if not os.listdir(UPLOAD_FOLDER):
                return jsonify(message='No files to sort')

            # Здесь был вызов subprocess.run(['python', './file_sorter.py'], check=True)

            download_link = url_for('download_file', session_id=session_id)
            return jsonify(message='Sorting completed successfully.', session_id=session_id)
        except subprocess.CalledProcessError as e:
            return jsonify(message=f'Error during sorting: {e}')
# Функция отправки запроса на кнопку для выполнения скрипта сортировки end


# Initialize the user's folder when the application starts
def initialize_user_folder():
    # Получаем идентификатор устройства из cookies
    device_id = request.cookies.get('device_id')

    # Если идентификатор устройства не установлен, создаем новый
    if not device_id:
        device_id = str(uuid.uuid4())

    # Создаем уникальную папку для каждого пользователя с использованием IP-адреса и идентификатора устройства
    user_folder = os.path.join(UPLOAD_FOLDER, f'{device_id}')
    os.makedirs(user_folder, exist_ok=True)

    # Сохраняем 'user_folder' в сессии
    session['user_folder'] = user_folder

    return device_id

@app.route('/file_encoding_sorter', methods=['GET', 'POST'])
def file_encoding_sorter():
    # Инициализируем папку пользователя при каждом запросе
    device_id = initialize_user_folder()

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

            try:
                # Сохраняем файл в уникальной папке пользователя
                file.save(os.path.join(session['user_folder'], filename))
                flash('File uploaded successfully', 'success')
                # Здесь вы можете провести дополнительную обработку файла, если это необходимо
            except FileNotFoundError:
                flash('Downloaded files not found', 'error')

    response = make_response(render_template('file_encoding_sorter.html'))
    response.set_cookie('device_id', device_id)
    return response

# My page end


# Обратная связь
mail = Mail(app)

# Настройка Flask-Mail
app.config['MAIL_SERVER']='sg1-ss106.a2hosting.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pass@mail.com'
app.config['MAIL_PASSWORD'] = 'pass@mail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message('Hello', sender='pass@mail.com', recipients=['pass@mail.com'])
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    mail.send(msg)

    # После успешной обработки, выполните перенаправление
    return redirect(url_for('thanks'))
# Обратная связь end


# My pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/My_test')
def My_test():
    return render_template('My_test.html')

if __name__ == '__main__':
    app.run(debug=True)