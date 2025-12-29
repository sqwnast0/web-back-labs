from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import random

lab9 = Blueprint('lab9', __name__)

# Данные для коробок с подарками
gift_boxes = [
    {"id": i, "message": f"Поздравляем! Это коробка номер {i+1}!", "opened": False, "gift": f"gift_{i+1}.png"}
    for i in range(10)
]

# Главная страница
@lab9.route('/lab9')
def lab9_index():
    remaining_boxes = len([box for box in gift_boxes if not box['opened']])
    return render_template('lab9/index.html', boxes=gift_boxes, remaining=remaining_boxes)

# Открытие коробки
@lab9.route('/lab9/open/<int:box_id>', methods=['POST'])
def open_box(box_id):
    if session.get('opened', 0) >= 3:
        return jsonify({"error": "Вы уже открыли 3 коробки. Не больше!"})

    box = gift_boxes[box_id]
    if box['opened']:
        return jsonify({"error": "Эта коробка уже пустая!"})

    # Открываем коробку
    box['opened'] = True
    session['opened'] = session.get('opened', 0) + 1
    return jsonify({"message": box['message'], "gift": box['gift'], "remaining": len([b for b in gift_boxes if not b['opened']])})

# Сброс коробок для авторизованных пользователей
@lab9.route('/lab9/reset', methods=['POST'])
def reset_boxes():
    if 'login' not in session:
        return jsonify({"error": "Только авторизованные пользователи могут сбросить коробки!"})

    for box in gift_boxes:
        box['opened'] = False
    session['opened'] = 0
    return jsonify({"message": "Все коробки были вновь наполнены!"})

# Страница входа
@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['login'] = username
        return redirect(url_for('lab9.lab9_index'))
    return render_template('lab9/login.html')

# Страница регистрации
@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = 'Пароли не совпадают!'
        elif not username or not password:
            error = 'Заполните все поля!'
        else:
            session['login'] = username
            return redirect(url_for('lab9.lab9_index'))
    return render_template('lab9/register.html', error=error)

# Страница выхода
@lab9.route('/lab9/logout')
def logout():
    session.clear()
    return redirect(url_for('lab9.lab9_index'))
