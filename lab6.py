from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

# ---------- ДАННЫЕ ----------
offices = []
for i in range(1, 11):
    offices.append({
        'number': i,
        'tenant': '',
        'price': 1000 + i * 500  # разная стоимость
    })

# ---------- СТРАНИЦА ----------
@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

# ---------- JSON-RPC API ----------
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')

    # ---------- INFO ----------
    if data.get('method') == 'info':
        login = session.get('login')
        total_price = 0

        if login:
            for office in offices:
                if office['tenant'] == login:
                    total_price += office['price']

        return {
            'jsonrpc': '2.0',
            'result': {
                'offices': offices,
                'total_price': total_price
            },
            'id': id
        }

    # ---------- АВТОРИЗАЦИЯ ----------
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    # ---------- BOOKING ----------
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
                        'id': id
                    }

                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    # ---------- CANCELLATION ----------
    if data.get('method') == 'cancellation':
        office_number = data.get('params')

        for office in offices:
            if office['number'] == office_number:

                if not office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 5,
                            'message': 'Office is not rented'
                        },
                        'id': id
                    }

                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Not your office'
                        },
                        'id': id
                    }

                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    # ---------- METHOD NOT FOUND ----------
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
