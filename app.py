from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_sock import Sock
import os
import subprocess
from flask import send_from_directory
from flask_mail import Mail, Message
#from flask_talisman import Talisman

app = Flask(__name__)
sock = Sock(app)

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

# Указываем папку для загрузки файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Максимальный размер загружаемых файлов (в байтах)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Например, 16 MB

@sock.route('/sockjs')
def sockjs(sock):
    while True:
        msg = sock.receive()
        print(msg)
        if msg == 'run_script':
            try:
                subprocess.call(['python', 'file_sorter.py'])  # Замените 'file_sorter.py' на путь к вашему скрипту
                download_link = url_for('download_file')
                result_message = 'Sorting completed successfully. Download the sorted files <a href="{}">here</a>.'.format(download_link)
                sock.send(result_message)
            except Exception as e:
                sock.send(f'Error during sorting: {e}')

# Функция для проверки разрешенных расширений файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'

@app.route('/download')
def download_file():
    return send_from_directory('Ready', 'Completed_files.zip')


# Функция отправки запроса на кнопку для выполнения скрипта сортировки
@app.route('/sort_files', methods=['GET', 'POST'])
def sort_files():
    if request.method == 'POST':
        try:
            subprocess.run(['python', 'C:\\MyCode\\Python\\Ruslan-dev-Free-Fire_Site\\file_sorter.py'], check=True)
            # Return the URL of the created archive
            return 'Sorting completed successfully. Download the sorted files <a href="/download">here</a>.'
        except subprocess.CalledProcessError as e:
            return f'Error during sorting: {e}'
    else:
        # Processing GET requests
        try:
            subprocess.run(['python', 'C:\\MyCode\\Python\\Ruslan-dev-Free-Fire_Site\\file_sorter.py'], check=True)
            # Return the URL of the created archive
            return 'Sorting completed successfully. Download the sorted files <a href="/download">here</a>.'
        except subprocess.CalledProcessError as e:
            return f'Error during sorting: {e}'
# Функция отправки запроса на кнопку для выполнения скрипта сортировки end


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

# My page end


if __name__ == '__main__':
    app.run(debug=True)