from flask import Flask, Blueprint, request, render_template, redirect, session
import datetime

lab5 = Blueprint('lab5', __name__)

app = Flask(__name__)
app.secret_key = 'секретно-секретный секрет'

# Страница с основным списком ссылок
@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

# Страница входа
@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Простейшая авторизация
        if username == "anonymous" and password == "password":
            session['username'] = username
            return redirect('/lab5/list')
        else:
            error = "Неверный логин или пароль"

    return render_template('lab5/login.html', error=error)

# Страница регистрации
@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    return render_template('lab5/register.html')

# Страница со списком статей
@lab5.route('/lab5/list')
def list_articles():
    if 'username' not in session:
        return redirect('/lab5/login')  # Перенаправление на страницу входа, если не авторизован
    return render_template('lab5/list.html')

# Страница создания статьи
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    if 'username' not in session:
        return redirect('/lab5/login')  # Перенаправление на страницу входа, если не авторизован
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        # Логика добавления статьи (пока просто выводим на экран)
        return render_template('lab5/article_created.html', title=title, content=content)
    return render_template('lab5/create.html')

# Страница выхода
@lab5.route('/lab5/logout')
def logout():
    session.pop('username', None)
    return redirect('/lab5/login')
