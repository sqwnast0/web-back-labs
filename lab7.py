from flask import Blueprint, render_template, request, jsonify, abort

lab7 = Blueprint('lab7', __name__)

# ---------- ДАННЫЕ ----------
films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Научно-фантастический фильм о путешествиях сквозь пространство и время."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "История надежды и свободы."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зелёная миля",
        "year": 1999,
        "description": "Драма о чуде и человечности."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Психологический триллер."
    },
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Фантастика о снах внутри снов."
    }
]

# ---------- СТРАНИЦА ----------
@lab7.route('/lab7/')
def index():
    return render_template('lab7/index.html')

# ---------- REST API ----------
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    films.append(film)
    return jsonify({"id": len(films) - 1})

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def edit_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    films[id] = request.get_json()
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    del films[id]
    return '', 204
