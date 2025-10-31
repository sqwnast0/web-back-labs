from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)


@app.errorhandler(404)
def not_found(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
        <style>
            body {
                text-align: center;
                padding: 50px;
                font-family: Arial, sans-serif;
            }
            h1 {
                font-size: 80px;
                color: #ff6b6b;
                margin: 0;
            }
            h2 {
                color: #333;
                margin: 20px 0;
            }
            img {
                max-width: 500px;
                margin: 20px auto;
                border-radius: 10px;
            }
            p {
                color: #666;
                max-width: 500px;
                margin: 0 auto 20px;
            }
            a {
                color: #667eea;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>404</h1>
        <h2>Страница не найдена</h2>
        
        <img src="''' + url_for('static', filename='404.png') + '''" alt="Страница не найдена">
        
        <p>Запрашиваемая страница не существует или была перемещена.</p>
        <p>Проверьте правильность адреса или вернитесь на главную страницу.</p>
        
        <a href="/">← Вернуться на главную</a>
    </body>
</html>''', 404

@app.route("/bad_request")
def bad_request():
    return '''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за некорректного синтаксиса.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 400

@app.route("/unauthorized")
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 401

@app.route("/payment_required")
def payment_required():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Зарезервировано для будущего использования. Первоначально предназначалось для цифровых платежных систем.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 402

@app.route("/forbidden")
def forbidden():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к запрошенному ресурсу запрещен.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 403

@app.route("/method_not_allowed")
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса не поддерживается для данного ресурса.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 405

@app.route("/teapot")
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я - чайник. Не могу заварить кофе.</p>
        <a href="/">На главную</a>
    </body>
</html>''', 418


@app.route("/")

@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <main>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                </ul>
            </nav>
        </main>
        
        <footer>
            <hr>
            &copy; Чикирисова Анастасия Вячеславовна, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''

@app.route("/lab1")
def lab1():
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
        
        <ul>
            <li><a href="/lab1/author">author</a></li>
            <li><a href="/lab1/web">web</a></li>
            <li><a href="/lab1/image">image</a></li>
            <li><a href="/lab1/counter">counter</a></li>
        </ul>
    </body>
</html>'''  

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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


@app.route('/lab1/image') 
def image():
    path = url_for("static", filename="oak.jpg")
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
</html>'''

count = 0

@app.route('/lab1/counter') 
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

@app.route('/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect('/lab1/counter')

@app.route("/lab1/info")
def info():
    return redirect("/author")


@app.route("/created")
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