$(document).ready(function(){
  $("#start-sorting").click(function(e){
    e.preventDefault(); // Prevent the default action of the link
    $.ajax({
        url: '/sort_files', // The route that will run the script
        type: 'POST', // The method of the request
        success: function(response){
            // Handle the response from the server
            console.log(response);
            // Insert the download link into the log panel
            $('#log').append('<div class="log-entry">ファイルが並べ替えられました。このリンクからダウンロードできます: <a href="/download">ダウンロード</a></div>');
        },
        error: function(error){
            // Handle any errors
            console.log(error);
        }
    });
});
});




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

// прочие функции

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

// прочие функции end