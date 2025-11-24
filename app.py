from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from lab1 import lab1
app = Flask(__name__)
app.register_blueprint(lab1)

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
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                </ul>
            </nav>
        </main>
        
        <footer>
            <hr>
            &copy; Чикирисова Анастасия Вячеславовна, ФБИ-33, 3 курс, 2025
        </footer>
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

if __name__ == '__main__':
    app.run(debug=True)
