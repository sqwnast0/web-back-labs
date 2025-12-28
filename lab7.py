from flask import Blueprint, render_template, request, jsonify, abort

lab7 = Blueprint('lab7', __name__)

# ------------------ Данные ------------------

films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Фантастический фильм о космосе и выживании человечества."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "История о надежде, дружбе и свободе."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зелёная миля",
        "year": 1999,
        "description": "Драма о человечности и сострадании."
    },
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Фильм о проникновении в сны и сознание."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Психологический триллер о двойственной личности."
    }
]

# ------------------ Страница ------------------

@lab7.route('/lab7/')
def index():
    return render_template('lab7/index.html')

# ------------------ REST API ------------------

# Получить все фильмы
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

# Получить один фильм
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return jsonify(films[id])

# Добавить фильм
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    if not film or not film.get('description'):
        return jsonify({
            "description": "Описание не может быть пустым"
        }), 400

    films.append(film)
    return jsonify({"id": len(films) - 1})

# Редактировать фильм
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def edit_film(id):
    if id < 0 or id >= len(films):
        abort(404)

    film = request.get_json()

    if not film or not film.get('description'):
        return jsonify({
            "description": "Описание не может быть пустым"
        }), 400

    films[id] = film
    return jsonify(films[id])

# Удалить фильм
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    if id < 0 or id >= len(films):
        abort(404)

    del films[id]
    return '', 204
