const uploadBtn = document.getElementById('uploadBtn'),
      itemUpload = document.getElementById('itemUpload');

uploadBtn.addEventListener('click', () => itemUpload.click());

itemUpload.addEventListener('change', function() {
    const hasFile = this.files.length > 0;
    uploadBtn.classList.toggle('has-file', hasFile);
    if (hasFile) {
        add_file();
    }
});

document.addEventListener('dragover', e => e.preventDefault());
document.addEventListener('drop', e => {
    e.preventDefault();
    itemUpload.files = e.dataTransfer.files;
    uploadBtn.classList.add('has-file');
    add_file();
});

function add_file() {
    const file = itemUpload.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imagePreview = document.getElementById('imagePreview');
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

document.getElementById('send_button').addEventListener('click', function() {

    const data = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        characters: document.getElementById('characters').value.split(' ').filter(Boolean),
        tags: document.getElementById('tags').value.split(' ').filter(Boolean),
        meta: document.getElementById('meta').value.split(' ').filter(Boolean),
        copyright: document.getElementById('copyright').value.split(' ').filter(Boolean),
        score: document.getElementById('score').value,
        resolutionX: document.getElementById('resolutionX').value,
        resolutionY: document.getElementById('resolutionY').value,
        compressMode: document.getElementById('compressMode').value,
        file: document.getElementById('itemUpload').files[0]
    };

    // Удаляем пустые значения
    const keysToRemove = [];
    for (const key of Object.keys(data)) {
        const value = data[key];
        if (!value) {
            keysToRemove.push(key);
        }
    }
    for (const key of keysToRemove) {
        delete data[key];
    }

    // Отправка данных на сервер
    const formData = new FormData();
    for (const key in data) {
        if (['characters', 'tags', 'meta', 'copyright'].includes(key)) {
            data[key].forEach(element => {
                formData.append(key, element);
            });
        } else {
            formData.append(key, data[key]);
        }
    }

    fetch('../api/items/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});