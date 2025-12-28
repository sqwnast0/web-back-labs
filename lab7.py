from flask import Blueprint, render_template, request, abort

lab7 = Blueprint('lab7', __name__)

# ------------------ ДАННЫЕ ------------------

films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха и вымирание растений приводят человечество "
                       "к продовольственному кризису, группа исследователей "
                       "отправляется в путешествие сквозь червоточину."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн осуждён за убийство жены и её любовника "
                       "и отправлен в тюрьму Шоушенк."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зелёная миля",
        "year": 1999,
        "description": "История тюремного надзирателя и необычного заключённого, "
                       "обладающего сверхъестественными способностями."
    },
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Профессиональный вор проникает в сны людей, чтобы украсть идеи."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "История человека, который создаёт подпольный бойцовский клуб."
    }
]

# ------------------ СТРАНИЦА ------------------

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

# ------------------ REST API ------------------

# Получить все фильмы
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


# Получить один фильм
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]


# Удалить фильм
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    del films[id]
    return '', 204


# Редактировать фильм
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)

    film = request.get_json()
    films[id] = film
    return films[id]
