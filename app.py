import firebase_admin
from firebase_admin import credentials, storage, db
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Инициализация Firebase с вашими учетными данными
cred = credentials.Certificate("album-98093-firebase-adminsdk-mpve7-5309e8b107.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'album-98093.appspot.com',
    'databaseURL': 'https://album-98093-default-rtdb.firebaseio.com/'
})


@app.route('/')
def index():
    return render_template('app.html')


@app.route('/photos', methods=['GET'])
def get_photos():
    # Получаем значения страницы и лимита из параметров запроса
    page = int(request.args.get('page', 1))  # По умолчанию первая страница
    limit = int(request.args.get('limit', 5))  # По умолчанию 5 фото на страницу

    # Получаем все фотографии из Firebase Realtime Database
    photos_ref = db.reference('photos')
    photos = photos_ref.get()

    # Преобразуем фотографии в список и делаем срез
    if photos:
        photos_list = list(photos.values())
        start = (page - 1) * limit
        end = start + limit
        paginated_photos = photos_list[start:end]

        return jsonify({
            "photos": paginated_photos,
            "page": page,
            "limit": limit,
            "total_photos": len(photos_list),
            "total_pages": (len(photos_list) + limit - 1) // limit
        }), 200
    else:
        return jsonify({"message": "No photos available"}), 404


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'caption' not in request.form:
        return jsonify({"error": "No file or caption provided"}), 400

    file = request.files['file']
    caption = request.form['caption']

    # Путь для хранения файла
    file_path = os.path.join("photos", file.filename)
    bucket = storage.bucket()
    blob = bucket.blob(file_path)

    # Загрузка файла в Firebase Storage
    blob.upload_from_file(file)
    blob.make_public()

    # Сохранение метаданных (подписи и URL) в Realtime Database
    data = {
        "caption": caption,
        "url": blob.public_url
    }
    db.reference('photos').push(data)

    return jsonify({"message": "File uploaded", "url": blob.public_url}), 200
