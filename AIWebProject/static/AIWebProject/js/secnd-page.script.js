document.getElementById('upload-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) return;

//    const previewImage = document.getElementById('preview-image');
//    previewImage.src = URL.createObjectURL(file);
//    previewImage.style.display = 'block';

    const formData = new FormData();
    formData.append('image', file); // 'image' — имя поля, как в Django view

    const imageURL = URL.createObjectURL(file);

    // Получаем CSRF токен из куки
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    fetch('http://51.250.51.104:8000/predict-image/', {
        method: 'POST',
        headers: {
        'X-CSRFToken': csrftoken
        },
        body: formData,
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Prediction result:', data);

        const existingRightSection = document.querySelector('.right-setion');
        if (existingRightSection) {
            const previewImage = document.getElementById('preview-image');
            previewImage.src = imageURL;
            const titleElement = document.querySelector('.info-container-title');
            if (titleElement && data.prediction) {
                titleElement.textContent = data.prediction;
            }
        }
        else{
            const rightSectionHTML = `
                <section class="right-setion">
                    <div class="filter-card">
                        <div>
                            <img id="preview-image" src="${imageURL}" alt="Загруженное изображение" style="display: block; max-width: 300px; margin-bottom: 10px;">
                        </div>
                        <div class="info-container2">
                            <h3 class="info-container-title">${data.prediction}</h3>
                        </div>
                    </div>
                </section>
            `;

            const main = document.querySelector('main');
            const leftSection = main.querySelector('.left-setion');
            leftSection.insertAdjacentHTML('afterend', rightSectionHTML);
        }
//        const titleElement = document.querySelector('.info-container-title');
//        if (titleElement && data.prediction) {
//            titleElement.textContent = data.prediction;
//        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при отправке изображения');
    });
});