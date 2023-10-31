var messages = [];
$(document).ready(function(){
  $("#start-sorting").click(function(e){
    e.preventDefault(); // Prevent the default action of the link
    $.ajax({
        url: '/sort_files', // The route that will run the script
        type: 'POST', // The method of the request
        success: function(response){
            // Check if the response is a JSON object
            if (typeof response === 'object') {
                // Check if the 'message' property exists in the response
                if ('message' in response) {
                    var message = response.message;
                    // Check if the message is 'No files to sort'
                    if (message === 'No files to sort') {
                        // If no files to sort, add an error message to the messages array
                        messages.push('Файлы для сортировки не найдены.<br>');
                    } else {
                        // If sorting was successful, add a success message to the messages array
                        var sessionId = response.session_id;
                        messages.push('Файлы были отсортированы. Вы можете скачать их <a href="/download/' + sessionId + '">здесь</a>.<br>');
                    }
                }
            } else {
                console.error('Response is not a JSON object');
            }
        },
        error: function(error){
            // Обработка ошибок
            console.log(error);
        }
    });
  });
});


setInterval(function() {
    var messageBox = document.getElementById('log');
    if (messageBox && messages.length > 0) {
        // Очищаем messageBox
        messageBox.innerHTML = '';

        // Добавляем новые сообщения в messageBox и удаляем их из массива
        messageBox.innerHTML += messages.join('');
        messages = [];
    }
}, 500);


// Проверяем наличие новых flash-сообщений каждые 500 миллисекунд
setInterval(function() {
    var flashMessages = document.querySelectorAll('.flash-message');
    for (var i = 0; i < flashMessages.length; i++) {
        var message = flashMessages[i].textContent;

        // Если сообщение об успешной загрузке, активируем ваш код
        if (message === 'File uploaded successfully') {
            var messageBox = document.getElementById('log');
            if (messageBox) {
                messageBox.textContent = message;
            }

            // Удаляем flash-сообщение после обработки
            flashMessages[i].parentNode.removeChild(flashMessages[i]);
        }
    }
}, 500);
// Проверяем наличие новых flash-сообщений каждые 500 миллисекунд конец



// Создаем новый объект XMLHttpRequest
var samuraiYoshinaga = new XMLHttpRequest();

// Определяем функцию, которая будет вызвана при изменении состояния запроса
samuraiYoshinaga.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        // Запрос успешно выполнен и ответ получен
        console.log(this.responseText);

        // Обновляем пользовательский интерфейс для отображения сообщения об успешной загрузке
        var messageBox = document.getElementById('log');
        if (messageBox) {
            // Создаем новый элемент div для сообщения
            var messageDiv = document.createElement('div');
            messageDiv.textContent = this.responseText; // используем текст ответа сервера

            // Добавляем новый элемент div в конец messageBox
            messageBox.appendChild(messageDiv);
        }
    }
};

// раскрываемое меню
function expandMenu() {
    var menu = document.querySelector('.advanced-options');
    menu.classList.toggle('expanded');
  }
// раскрываемое меню конец


// обработка чекбоксов
function handleAdvancedOptions() {
    var fixEncodingCheckbox = document.getElementById('fix-encoding');
    var correctedFilesCheckbox = document.getElementById('corrected-files-in-a-separate-folder');
    var fileCorrectionOnlyCheckbox = document.getElementById('file-correction-only');

    // Устанавливаем зависимость между чекбоксами
    var isFixEncodingChecked = fixEncodingCheckbox.checked;
    correctedFilesCheckbox.disabled = !isFixEncodingChecked;
    fileCorrectionOnlyCheckbox.disabled = !isFixEncodingChecked;

    // Если fixEncodingCheckbox не выбран, сбрасываем correctedFilesCheckbox и fileCorrectionOnlyCheckbox
    if (!isFixEncodingChecked) {
        correctedFilesCheckbox.checked = false;
        fileCorrectionOnlyCheckbox.checked = false;
    }

    // Получаем значения чекбоксов
    var fixEncodingValue = isFixEncodingChecked;
    var correctedFilesValue = correctedFilesCheckbox.checked;
    var fileCorrectionOnlyValue = fileCorrectionOnlyCheckbox.checked;

    // Отправляем значения на сервер с помощью fetch API или XMLHttpRequest
    fetch('/web-app-settings', {
        method: 'POST',
        body: JSON.stringify({
            fixEncoding: fixEncodingValue,
            correctedFiles: correctedFilesValue,
            fileCorrectionOnly: fileCorrectionOnlyValue
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
      .then(data => console.log(data));
}

document.addEventListener('DOMContentLoaded', (event) => {
    // Вызываем handleAdvancedOptions при загрузке страницы
    handleAdvancedOptions();

    document.getElementById('start-sorting').addEventListener('click', function() {
        handleAdvancedOptions();
    });

    document.getElementById('fix-encoding').addEventListener('change', function() {
        handleAdvancedOptions();
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('start-sorting').addEventListener('click', function() {
        handleAdvancedOptions();
    });

    document.getElementById('fix-encoding').addEventListener('change', function() {
        handleAdvancedOptions();
    });
});

   // кнопка
function serverLog(message) {
    // Выводим сообщение в консоль
    console.log(message);

    // Отправляем сообщение на сервер
    $.ajax({
        url: '/log',
        method: 'POST',
        data: JSON.stringify({ message: message }),
        contentType: 'application/json',
        success: function(response) {
            console.log('Сообщение успешно отправлено на сервер.');
        },
        error: function(error) {
            console.log('Произошла ошибка при отправке сообщения на сервер:', error);
        }
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('start-sorting').addEventListener('click', function() {
        var fixEncodingCheckbox = document.getElementById('fix-encoding');
        var correctedFilesCheckbox = document.getElementById('corrected-files-in-a-separate-folder');
        var fileCorrectionOnlyCheckbox = document.getElementById('file-correction-only');

        var message = '--fix_encodings ' + fixEncodingCheckbox.checked +
                      ' --separate_folder ' + correctedFilesCheckbox.checked +
                      ' --only_correction ' + fileCorrectionOnlyCheckbox.checked;

        // Используем serverLog для отправки сообщения на сервер
        serverLog(message);
    });
});


// прочие функции

// Функция для запуска сортировки файлов
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

    // Отправляем GET-запрос на URL /sort_files для запуска сортировки
    xhttp.open("GET", "/sort_files", true);
    xhttp.send();
}

// Функция для открытия вкладок сообщений
// Дожидаемся загрузки DOM
document.addEventListener("DOMContentLoaded", function () {
  // Получаем все элементы с классом 'question'
  var questionElements = document.getElementsByClassName("question");

  // Проверяем, существуют ли элементы
  if (questionElements) {
    // Если элементы существуют, добавляем обработчик события клика каждому из них
    for (var i = 0; i < questionElements.length; i++) {
      questionElements[i].addEventListener("click", function () {
        // Переключаем класс 'active' родительского элемента при клике
        this.parentNode.classList.toggle("active");
      });
    }
  }
});

// прочие функции end