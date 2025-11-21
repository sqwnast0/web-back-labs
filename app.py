from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

access_log = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now()
    requested_url = request.url
    
    log_entry = {
        'time': access_time,
        'ip': client_ip,
        'url': requested_url
    }
    access_log.append(log_entry)
    
    journal_html = ''
    for entry in reversed(access_log):  
        journal_html += f'''
        <div class="log-entry">
            [{entry["time"].strftime("%Y-%m-%d %H:%M:%S.%f")}, пользователь {entry["ip"]}] зашёл на адрес: {entry["url"]}
        </div>'''
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="{url_for('static', filename='lab1.css')}">
        <style>
            body {{
                text-align: center;
                padding: 50px;
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                background-color: #f8f9fa;
            }}
            .error-container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }}
            h1 {{

                font-size: 80px;
                color: #ff6b6b;
                margin: 0;
                text-align: center;
            }}
            h2 {{
                color: #333;
                margin: 20px 0;
                text-align: center;
            }}
            .info-box {{
                background: #e9ecef;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .info-box p {{
                margin: 5px 0;
                color: #495057;
            }}
            .journal {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .journal h3 {{
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            .log-entry {{
                padding: 10px;
                border-bottom: 1px solid #dee2e6;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }}
            .log-entry:last-child {{
                border-bottom: none;
            }}
            .log-time {{
                color: #6c757d;
            }}
            .log-user {{
                color: #007bff;
                font-weight: bold;
            }}
            .log-action {{
                color: #28a745;
            }}
            .home-link {{
                display: inline-block;
                padding: 12px 24px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;                
                font-weight: bold;
                margin: 20px 0;
            }}
            .home-link:hover {{
                background: #5a67d8;
                text-decoration: none;
            }}
            img {{
                max-width: 500px;
                margin: 20px auto;
                display: block;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>404</h1>
            <h2>Страница не найдена</h2>
            
            <img src="{url_for('static', filename='404.png')}" alt="Страница не найдена">
            
            <div class="info-box">
                <p><strong>Ваш IP-адрес:</strong> {client_ip}</p>
                <p><strong>Дата и время доступа:</strong> {access_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Запрошенный адрес:</strong> {requested_url}</p>
            </div>
            
            <p style="text-align: center; color: #666;">
                Запрашиваемая страница не существует или была перемещена.<br>
                Проверьте правильность адреса или вернитесь на главную страницу.
            </p>
            
            <div style="text-align: center;">
                <a href="/" class="home-link">← Вернуться на главную</a>
            </div>
        </div>
        
        <div class="journal">
            <h3>Журнал:</h3>
            {journal_html if journal_html else '<p>Пока нет записей в журнале</p>'}
        </div>
    </body>
</html>''', 404

@app.before_request
def log_all_requests():
    if not request.path.startswith('/static/'):
        log_entry = {
            'time': datetime.datetime.now(),
            'ip': request.remote_addr,
            'url': request.url
        }
        access_log.append(log_entry)

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

@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
        <style>
            body {
                text-align: center;
                padding: 50px;
                font-family: Arial, sans-serif;
                background-color: #fff5f5;
            }
            h1 {
                font-size: 80px;
                color: #e53e3e;
                margin: 0;
            }
            h2 {
                color: #333;
                margin: 20px 0;
            }
            .error-box {
                background: white;
                padding: 20px;
                border-radius: 10px;
                max-width: 600px;
                margin: 20px auto;
                border-left: 4px solid #e53e3e;
            }
            a {
                display: inline-block;
                padding: 10px 20px;
                background: grey;
                color: black;
                text-decoration: none;
                border-radius: 5px;
                margin: 10px;
            }
            a:hover {
                background: black;
            }
        </style>
    </head>
    <body>
        <h1>500</h1>
        <h2>Внутренняя ошибка сервера</h2>
        
        <div class="error-box">
            <p>На сервере произошла непредвиденная ошибка.</p>
            <p>Мы уже знаем о проблеме и работаем над её решением.</p>
            <p>Попробуйте обновить страницу через несколько минут.</p>
        </div>
        
        <div>
            <a href="/">На главную</a>
            <a href="javascript:location.reload()">Обновить страницу</a>
        </div>
        
        <p style="margin-top: 30px; color: #999; font-size: 14px;">
            Если ошибка повторяется, свяжитесь с администратором: 
            <a href="mailto:acikirisova@gmail.com" style="color: #333;">acikirisova@gmail.com</a>
        </p>
    </body>
</html>''', 500

@app.route("/server_error")
def cause_server_error():
    # Вызываем ошибку делением на ноль
    result = 1 / 0
    return "Эта строка никогда не будет выполнена"


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

@app.route("/http_codes")
def http_codes():
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
        <title>Коды ответов HTTP</title>
    </head>
    <body>
        <h1>Коды ответов HTTP</h1>
        <ul>
            <li><a href="/bad_request">400 - Bad Request</a></li>
            <li><a href="/unauthorized">401 - Unauthorized</a></li>
            <li><a href="/payment_required">402 - Payment Required</a></li>
            <li><a href="/forbidden">403 - Forbidden</a></li>
            <li><a href="/method_not_allowed">405 - Method Not Allowed</a></li>
            <li><a href="/teapot">418 - I'm a teapot</a></li>
            <li><a href="/server_error">500 - Internal Server Error</a></li>
        </ul>
        <a href="/">На главную</a>
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
</html>''', 200, {
        'Content-Language': 'ru-RU',  
        'X-Image-Type': 'Nature',     
        'X-Server-Location': 'Novosibirsk',  
        'X-Student-Name': 'Chikirisova Anastasia' 
    }

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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['астра', 'незабудка', 'альстромерия', 'тюльпан']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
    <body>
        <h1>Информация о цветке</h1>
        <p>ID: {flower_id}</p>
        <p>Название: {flower_list[flower_id]}</p>
        <a href='/lab2/flowers/>Вернуться к списку всех цветов</a>
    </body>
</html>
'''

@app.route('/lab2/add_flower/')
def add_flower_empty():
    abort(400, description="вы не задали имя цветка")

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка:  {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/flowers/all')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Все цветы</h1>
        <p>Количество цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <a href="/lab2/flowers/clear">Очистить список</a>
    </body>
</html>
'''

@app.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/flowers/all">Посмотреть все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Анастасия Чикирисова'
    group = 'ФБИ-33'
    course = '3 курс'
    number = '2'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
    ]
    return render_template('example.html', 
                           name=name, number=number, group=group, 
                           course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
<!doctype html>
<html>
<body>
    <h1>Расчёт с параметрами:</h1>
    <div class="result">
        {a} + {b} = {a + b}<br>
        {a} - {b} = {a - b}<br>
        {a} × {b} = {a * b}<br>
        {a} / {b} = {a / b if b != 0 else 'на ноль делить нельзя'}<br>
        {a}<sup>{b}</sup> = {a ** b}
    </div>
    <p><a href="/lab2/calc/">Попробовать с другими числами</a></p>
</body>
</html>
'''

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1300},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Фантастика', 'pages': 480},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Классическая проза', 'pages': 350},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Солженицын', 'title': 'Архипелаг ГУЛАГ', 'genre': 'Историческая проза', 'pages': 1424},
    {'author': 'Владимир Набоков', 'title': 'Лолита', 'genre': 'Роман', 'pages': 336},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
]

@app.route('/lab2/books/')
def books_list():
    return render_template('books.html', books=books)

@app.route('/lab2/cars/')
def cars():
    cars_list = [
        {
            'name': 'Ford Mustang',
            'year': '1964',
            'description': 'Легендарный американский маслкар, символ свободы и скорости.',
            'image': 'ford_mustang.jpg',
            'country': 'США',
            'type': 'Спортивный автомобиль'
        },
        {
            'name': 'Volkswagen Beetle',
            'year': '1938',
            'description': 'Народный автомобиль, один из самых узнаваемых в мире.',
            'image': 'Volkswagen_Beetle.jpg',
            'country': 'Германия',
            'type': 'Компактный автомобиль'
        },
        {
            'name': 'Toyota Corolla',
            'year': '1966',
            'description': 'Самый продаваемый автомобиль в истории - надежность и практичность.',
            'image': 'Toyota_Corolla.jpg',
            'country': 'Япония',
            'type': 'Седан'
        },
        {
            'name': 'Ferrari F40',
            'year': '1987',
            'description': 'Легендарный суперкар, последний автомобиль, одобренный Энцо Феррари.',
            'image': 'Ferrari_F40.jpg',
            'country': 'Италия',
            'type': 'Суперкар'
        },
        {
            'name': 'Jeep Wrangler',
            'year': '1986',
            'description': 'Внедорожник с культовым дизайном, наследник военного Willys MB.',
            'image': 'Jeep_Wrangler.jpg',
            'country': 'США',
            'type': 'Внедорожник'
        },
        {
            'name': 'BMW 3 Series',
            'year': '1975',
            'description': 'Икона спортивных седанов, сочетание комфорта и динамики.',
            'image': 'BMW3_Series.jpg',
            'country': 'Германия',
            'type': 'Спортивный седан'
        },
        {
            'name': 'Lada Niva',
            'year': '1977',
            'description': 'Первый в мире моноприводный внедорожник, легенда российского автопрома.',
            'image': 'Lada_Niva.jpg',
            'country': 'Россия',
            'type': 'Внедорожник'
        },
        {
            'name': 'Porsche 911',
            'year': '1963',
            'description': 'Культовый спортивный автомобиль с задним расположением двигателя.',
            'image': 'Porsche_911.jpg',
            'country': 'Германия',
            'type': 'Спортивный автомобиль'
        },
        {
            'name': 'Honda Civic',
            'year': '1972',
            'description': 'Компактный автомобиль, ставший иконой тюнинговой культуры.',
            'image': 'Honda_Civic.jpg',
            'country': 'Япония',
            'type': 'Компактный автомобиль'
        },
        {
            'name': 'Mercedes-Benz S-Class',
            'year': '1972',
            'description': 'Флагманский седан, эталон роскоши и технологий.',
            'image': 'Mercedes-Benz_S-Class.jpg',
            'country': 'Германия',
            'type': 'Представительский класс'
        },
        {
            'name': 'Chevrolet Corvette',
            'year': '1953',
            'description': 'Американский спортивный автомобиль, символ автоиндустрии США.',
            'image': 'Chevrolet_Corvette.jpg',
            'country': 'США',
            'type': 'Спортивный автомобиль'
        },
        {
            'name': 'Volvo XC90',
            'year': '2002',
            'description': 'Премиальный внедорожник, известный своей безопасностью.',
            'image': 'Volvo_XC90.jpg',
            'country': 'Швеция',
            'type': 'Внедорожник'
        },
        {
            'name': 'Mazda MX-5 Miata',
            'year': '1989',
            'description': 'Легкий родстер, возродивший класс доступных спортивных автомобилей.',
            'image': 'Mazda_MX-5_Miata.jpg',
            'country': 'Япония',
            'type': 'Родстер'
        },
        {
            'name': 'Range Rover',
            'year': '1970',
            'description': 'Роскошный внедорожник, создавший новый класс автомобилей.',
            'image': 'Range_Rover.jpg',
            'country': 'Великобритания',
            'type': 'Премиальный внедорожник'
        },
        {
            'name': 'Tesla Model S',
            'year': '2012',
            'description': 'Электрический седан, изменивший представление об электромобилях.',
            'image': 'Tesla_Model_S.jpg',
            'country': 'США',
            'type': 'Электромобиль'
        },
        {
            'name': 'Audi Quattro',
            'year': '1980',
            'description': 'Легенда ралли, популяризировавший полный привод в гражданских авто.',
            'image': 'Audi_Quattro.jpg',
            'country': 'Германия',
            'type': 'Спортивный автомобиль'
        },
        {
            'name': 'Nissan GT-R',
            'year': '2007',
            'description': 'Японский суперкар, известный как "Богzilla" за свою производительность.',
            'image': 'Nissan_GT-R.jpg',
            'country': 'Япония',
            'type': 'Суперкар'
        },
        {
            'name': 'Fiat 500',
            'year': '1957',
            'description': 'Культовый городской автомобиль, символ итальянского стиля.',
            'image': 'Fiat_500.jpg',
            'country': 'Италия',
            'type': 'Городской автомобиль'
        },
        {
            'name': 'Lamborghini Countach',
            'year': '1974',
            'description': 'Суперкар с клиновидным дизайном, икона 1980-х годов.',
            'image': 'Lamborghini_Countach.jpg',
            'country': 'Италия',
            'type': 'Суперкар'
        },
        {
            'name': 'Subaru Impreza WRX',
            'year': '1992',
            'description': 'Легенда раллийных соревнований с оппозитным двигателем и полным приводом.',
            'image': 'Subaru_Impreza_WRX.jpg',
            'country': 'Япония',
            'type': 'Спортивный седан'
        }
    ]
    
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
        <title>Коллекция автомобилей</title>
    </head>
    <body>
        <h1>Коллекция легендарных автомобилей</h1>
        <a href="/">На главную</a>
        <div class="cars-container">
            ''' + ''.join([f'''
            <div class="car-card">
                <h2>{car["name"]}</h2>
                <img src="{url_for('static', filename=car['image'])}" alt="{car['name']}" width="300">
                <div class="car-info">
                    <p><strong>Год выпуска:</strong> {car["year"]}</p>
                    <p><strong>Страна:</strong> {car["country"]}</p>
                    <p><strong>Тип:</strong> {car["type"]}</p>
                    <p><strong>Описание:</strong> {car["description"]}</p>
                </div>
            </div>
            ''' for car in cars_list]) + '''
        </div>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
