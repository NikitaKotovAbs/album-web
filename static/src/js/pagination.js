let currentPage = 1;
const limit = 5;

async function loadPhotos(page) {
    try {
        const response = await fetch(`/photos?page=${page}&limit=${limit}`);
        const data = await response.json();

        const galleryDiv = document.getElementById('gallery');
        galleryDiv.innerHTML = '';

        if (data.message) {
            galleryDiv.innerHTML = '<p>No photos available</p>';
        } else {
            data.photos.forEach(photo => {
                const photoContainer = document.createElement('div');
                photoContainer.style.marginBottom = '20px';

                const img = document.createElement('img');
                img.src = photo.url;
                img.alt = photo.caption;
                img.style.width = '200px';
                img.style.height = 'auto';

                const caption = document.createElement('p');
                caption.textContent = photo.caption;

                photoContainer.appendChild(img);
                photoContainer.appendChild(caption);
                galleryDiv.appendChild(photoContainer);
            });

            // Обновление состояния кнопок
            document.getElementById('prev').disabled = data.page <= 1;
            document.getElementById('next').disabled = data.page >= data.total_pages;
        }
    } catch (error) {
        console.error('Error loading photos:', error);
    }
}

function nextPage() {
    currentPage += 1;
    loadPhotos(currentPage);
}

function prevPage() {
    currentPage -= 1;
    loadPhotos(currentPage);
}

// Загрузка первой страницы при открытии
loadPhotos(currentPage);
