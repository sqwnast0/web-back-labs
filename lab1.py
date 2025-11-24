from flask import Blueprint, url_for, request, redirect
import datetime
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1")
def lab():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная работа 1</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        
        <a href="/">На главную</a>
        
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/author">Автор</a></li>
            <li><a href="/lab1/web">WEB</a></li>
            <li><a href="/lab1/image">Дуб</a></li>
            <li><a href="/lab1/counter">Счетчик</a></li>
            <li><a href="/bad_request">400 - Bad Request</a></li>
            <li><a href="/unauthorized">401 - Unauthorized</a></li>
            <li><a href="/payment_required">402 - Payment Required</a></li>
            <li><a href="/forbidden">403 - Forbidden</a></li>
            <li><a href="/nonexistent_page">404 - Not Found</a></li>
            <li><a href="/method_not_allowed">405 - Method Not Allowed</a></li>
            <li><a href="/teapot">418 - I'm a teapot</a></li>
            <li><a href="/server_error">500 - Internal Server Error</a></li>
        </ul>
    </body>
</html>'''   


@lab1.route("/lab1/web")
def web():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') +'''">
    </head>
    <body>
        <h1>web-сервер на flask</h1>
        <a href="/lab1/author">author</a>
    </body>
</html>''', 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
}


@lab1.route("/lab1/author")
def author():
    name = "Чикирисова Анастасия Вячеславовна"
    group = "ФБИ-33"
    faculty = "ФБ"
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>           
    <body>
        <p>Студент: ''' + name + '''</p>
        <p>Группа: ''' + group + '''</p>
        <p>Факультет: ''' + faculty + '''</p>
        <a href="/web">web</a>
    </body>
</html>'''


@lab1.route('/lab1/image') 
def image():
    path = url_for("static", filename="oak.jpeg")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') +'''">
    </head>
    <body>
        <h1>Дyб</h1>
        <img src="''' + path + '''">
    </body>
</html>''', 200, {
        'Content-Language': 'ru-RU',  
        'X-Image-Type': 'Nature',     
        'X-Server-Location': 'Novosibirsk',  
        'X-Student-Name': 'Gevorkyan Alina' 
    }
count = 0


@lab1.route('/lab1/counter') 
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') +'''">
    </head>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <br>
        <a href="/reset_counter">Очистить счётчик</a>
    </body>
</html>
'''


@lab1.route('/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@lab1.route("/lab1/info")
def info():
    return redirect("/author")


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201