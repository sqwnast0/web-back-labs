from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

# 10 офисов: number — номер, tenant — арендатор (пусто => свободен)
offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": ""})


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    req_id = data.get('id')

    # info — вернуть список офисов
    if data.get('method') == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': req_id
        }

    # для booking / cancellation нужна авторизация
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': req_id
        }

    # booking — забронировать офис
    if data.get('method') == 'booking':
        office_number = data.get('params')

        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Office already booked'
                        },
                        'id': req_id
                    }

                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': req_id
                }

        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': req_id
        }

    # cancellation — снять бронь (только если бронировал ты)
    if data.get('method') == 'cancellation':
        office_number = data.get('params')

        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Not your booking'
                        },
                        'id': req_id
                    }

                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': req_id
                }

        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': req_id
        }

    # неизвестный метод (JSON-RPC стандарт: -32601)
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': req_id
    }
