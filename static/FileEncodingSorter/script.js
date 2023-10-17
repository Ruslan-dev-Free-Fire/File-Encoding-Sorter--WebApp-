function initializeSockJS() {
    var sock = new SockJS('http://' + document.domain + ':' + location.port + '/sockjs');

    $('#start-sorting').on('click', function (event) {
        event.preventDefault();  // Предотвращает переход по ссылке
        sock.send('run_script');
    });

    sock.onmessage = function(e) {
        document.getElementById('log').innerHTML += '<div class="log-entry">' + e.data + '</div>';
    };
}

function startSorting() {
    // Создаем новый объект XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Определяем функцию, которая будет вызвана при изменении состояния запроса
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Запрос успешно выполнен и ответ получен
            console.log(this.responseText);
        }
    };

    // Отправляем GET-запрос на URL /sort_files
    xhttp.open("GET", "/sort_files", true);
    xhttp.send();
}

// Загрузка лога сообщений при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const log = localStorage.getItem('log');
    if (log) {
        document.querySelector('.mytextlogfile').innerHTML = log;
    }
});

// Добавление сообщения в лог и сохранение его в localStorage
function addToLog(message) {
    const logContainer = document.querySelector('.mytextlogfile');
    const logEntry = document.createElement('div');
    logEntry.textContent = message;
    logContainer.appendChild(logEntry);

    // Сохраняем обновленный лог в localStorage
    localStorage.setItem('log', logContainer.innerHTML);
}

document.addEventListener('DOMContentLoaded', function() {
// Clear the log when the page is loaded
localStorage.removeItem('log');

// Clear the displayed log messages
document.querySelector('.mytextlogfile').innerHTML = '';
});

window.onload = function() {
    const fileDropArea = document.getElementById('file-drop-area');
    const fileInput = document.querySelector('.sc-16z3mvs-0.kbLfHX');

    if (fileDropArea) {
        fileDropArea.addEventListener('dragover', function (e) {
            e.preventDefault(); // Предотвращаем браузерное действие по умолчанию
            fileDropArea.style.border = '2px dashed green';
        });
    }
};

const fileDropArea = document.getElementById('file-drop-area');

if (fileDropArea) {
    // Обработчик события dragleave (когда файл перетаскивают из области)
    fileDropArea.addEventListener('dragleave', function (e) {
        e.preventDefault();
        fileDropArea.style.border = 'none';
    });

    // Обработчик события drop (когда файл отпускают в область)
    fileDropArea.addEventListener('drop', function (e) {
        e.preventDefault(); // Предотвращаем браузерное действие по умолчанию
        fileDropArea.style.border = 'none';

        const files = e.dataTransfer.files;
        handleFiles(files);
    });
}

function handleFiles(files) {
for (const file of files) {
    if (file) {
        const allowedExtensions = ['txt'];
        const fileExtension = file.name.split('.').pop().toLowerCase();

        if (allowedExtensions.indexOf(fileExtension) === -1) {
            alert('Only files with the extension .txt are allowed');
        } else {
            fileInput.files = files;
            fileInput.form.submit();  // Automatically submit the form
        }
    }
}
}
