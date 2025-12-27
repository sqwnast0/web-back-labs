from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from os import path

lab5 = Blueprint('lab5', __name__)

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------

def exec_query(cur, db_type, query, params=()):
    if db_type == 'postgres':
        cur.execute(query.replace('?', '%s'), params)
    else:
        cur.execute(query, params)


def db_connect():
    db_type = current_app.config.get('DB_TYPE', 'sqlite')

    if db_type == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='webprogramm',
            user='Nastya',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        db_path = path.join(path.dirname(__file__), 'database.db')
        conn = sqlite3.connect(db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur, db_type


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# ---------- ГЛАВНАЯ ----------

@lab5.route('/lab5')
@lab5.route('/lab5/')
def lab5_index():
    return render_template('lab5/lab5.html', login=session.get('login'))


# ---------- РЕГИСТРАЦИЯ ----------

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    if password != confirm:
        return render_template('lab5/register.html', error='Пароли не совпадают')

    conn, cur, db_type = db_connect()

    exec_query(cur, db_type, "SELECT id FROM users WHERE login=?;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Пользователь уже существует')

    password_hash = generate_password_hash(password)

    exec_query(
        cur, db_type,
        "INSERT INTO users (login, password) VALUES (?, ?);",
        (login, password_hash)
    )

    db_close(conn, cur)
    return render_template('lab5/success_registration.html', login=login)


# ---------- ЛОГИН ----------

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur, db_type = db_connect()

    exec_query(cur, db_type, "SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return redirect('/lab5/list')


# ---------- ЛОГАУТ ----------

@lab5.route('/lab5/logout')
def logout():
    session.clear()
    return redirect('/lab5/login')


# ---------- СОЗДАНИЕ СТАТЬИ ----------

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    text = request.form.get('article_text')

    if not title or not text:
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur, db_type = db_connect()

    exec_query(cur, db_type, "SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()['id']

    exec_query(
        cur, db_type,
        "INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?);",
        (user_id, title, text)
    )

    db_close(conn, cur)
    return redirect('/lab5/list')


# ---------- СПИСОК СТАТЕЙ ----------

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur, db_type = db_connect()

    exec_query(cur, db_type, "SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()['id']

    exec_query(
        cur, db_type,
        "SELECT id, title, article_text, created_at FROM articles WHERE login_id=? ORDER BY created_at DESC;",
        (user_id,)
    )
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)


# ---------- РЕДАКТИРОВАНИЕ ----------

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur, db_type = db_connect()

    exec_query(cur, db_type, "SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()['id']

    if request.method == 'GET':
        exec_query(
            cur, db_type,
            "SELECT * FROM articles WHERE id=? AND login_id=?;",
            (article_id, user_id)
        )
        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return redirect('/lab5/list')

        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    text = request.form.get('article_text')

    exec_query(
        cur, db_type,
        "UPDATE articles SET title=?, article_text=? WHERE id=? AND login_id=?;",
        (title, text, article_id, user_id)
    )

    db_close(conn, cur)
    return redirect('/lab5/list')


# ---------- УДАЛЕНИЕ ----------

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur, db_type = db_connect()

    exec_query(cur, db_type, "SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()['id']

    exec_query(
        cur, db_type,
        "DELETE FROM articles WHERE id=? AND login_id=?;",
        (article_id, user_id)
    )

    db_close(conn, cur)
    return redirect('/lab5/list')
