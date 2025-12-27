from flask import Blueprint, render_template, request, session, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

lab5 = Blueprint('lab5', __name__)

# Подключение к базе данных
def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='webprogramm',
        user='Nastya',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/')
def lab5_index():
    return render_template('lab5/lab5.html', login=session.get('login'))

# Страница входа
@lab5.route('/lab5/login', methods=['GET', 'POST'])
def logindfg():
    error = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            error = 'Заполните все поля'
            return render_template('lab5/login.html', error=error)

        try:
            conn, cur = db_connect()

            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
            user = cur.fetchone()

            if not user or not check_password_hash(user['password'], password):
                error = 'Логин или пароль неверны'
                return render_template('lab5/login.html', error=error)

            session['login'] = login
            db_close(conn, cur)

            return redirect('/lab5/success_login')
        except Exception as e:
            error = f"Ошибка при входе: {str(e)}"
            return render_template('lab5/login.html', error=error)

    return render_template('lab5/login.html')

# Страница регистрации
@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not login or not password:
            error = 'Заполните все поля'
            return render_template('lab5/register.html', error=error)

        if password != confirm_password:
            error = 'Пароли не совпадают'
            return render_template('lab5/register.html', error=error)

        try:
            conn, cur = db_connect()

            # Проверка, есть ли уже такой пользователь
            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
            user = cur.fetchone()

            if user:
                error = 'Пользователь с таким логином уже существует'
                db_close(conn, cur)
                return render_template('lab5/register.html', error=error)

            # Генерация хеша пароля перед сохранением в БД
            password_hash = generate_password_hash(password)

            # Вставка логина и хеша пароля в базу данных
            cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
            db_close(conn, cur)

            return redirect('/lab5/success_registration')
        except Exception as e:
            error = f"Ошибка при регистрации: {str(e)}"
            return render_template('lab5/register.html', error=error)

    return render_template('lab5/register.html')

# Страница с успешным входом
@lab5.route('/lab5/success_login')
def success_login():
    return render_template('lab5/success_login.html', login=session['login'])

# Страница с успешной регистрацией
@lab5.route('/lab5/success_registration')
def success_registration():
    return render_template('lab5/success_registration.html', login=session['login'])

# Страница выхода
@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('lab5.lab5_index'))

# Страница для создания статьи
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    # Проверяем, авторизован ли пользователь
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')  # Если нет, перенаправляем на страницу логина

    if request.method == 'GET':
        # Если метод GET, показываем форму для создания статьи
        return render_template('lab5/create_article.html')

    # Если метод POST, обрабатываем отправку данных
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        error = 'Заполните все поля!'
        return render_template('lab5/create_article.html', error=error)

    try:
        # Подключаемся к базе данных
        conn, cur = db_connect()

        # Получаем id пользователя по логину
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()
        login_id = user['id']

        # Вставляем статью в таблицу articles
        cur.execute(f"INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s);",
                    (login_id, title, article_text))
        db_close(conn, cur)

        # После успешного добавления статьи перенаправляем на главную страницу
        return redirect('/lab5')

    except Exception as e:
        error = f"Ошибка при добавлении статьи: {str(e)}"
        return render_template('lab5/create_article.html', error=error)
    
# Страница со списком статей пользователя
@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')

    # Если не авторизован — на логин
    if not login:
        return redirect('/lab5/login')

    try:
        conn, cur = db_connect()

        # Получаем id пользователя
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        login_id = user['id']

        # Получаем статьи пользователя sdf
        cur.execute("""
            SELECT title, article_text, created_at
            FROM articles
            WHERE login_id = %s
            ORDER BY created_at DESC;
        """, (login_id,))

        articles = cur.fetchall()
        db_close(conn, cur)

        return render_template(
            'lab5/articles.html',
            articles=articles
        )

    except Exception as e:
        return f"Ошибка при выводе статей: {e}"
