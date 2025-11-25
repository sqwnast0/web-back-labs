from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name = name if name else "Аноним"
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    age = age if age else "Неизвестно"
    return render_template('/lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if user == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    drink_name = ''

    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    additions = []
    if request.args.get('milk') == 'on':
        price += 30
        additions.append('молоко')
    if request.args.get('sugar') == 'on':
        price += 10
        additions.append('сахар')
    
    return render_template('lab3/pay.html', price=price, drink_name=drink_name, additions=additions)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    current_color = request.cookies.get('color', '#000000')
    current_bg_color = request.cookies.get('bg_color', '#ffffff')
    current_font_size = request.cookies.get('font_size', '16')
    current_font_family = request.cookies.get('font_family', 'Arial, sans-serif')

    new_color = request.args.get('color')
    new_bg_color = request.args.get('bg_color')
    new_font_size = request.args.get('font_size')
    new_font_family = request.args.get('font_family')

    if new_color or new_bg_color or new_font_size or new_font_family:
        color_to_use = new_color if new_color is not None else current_color
        bg_color_to_use = new_bg_color if new_bg_color is not None else current_bg_color
        font_size_to_use = new_font_size if new_font_size is not None else current_font_size
        font_family_to_use = new_font_family if new_font_family is not None else current_font_family
        
        resp = make_response(render_template('lab3/settings.html', 
                                            color=color_to_use,
                                            bg_color=bg_color_to_use,
                                            font_size=font_size_to_use,
                                            font_family=font_family_to_use))

        if new_color:
            resp.set_cookie('color', new_color, max_age=60*60*24*365)
        if new_bg_color:
            resp.set_cookie('bg_color', new_bg_color, max_age=60*60*24*365)
        if new_font_size:
            resp.set_cookie('font_size', new_font_size, max_age=60*60*24*365)
        if new_font_family:
            resp.set_cookie('font_family', new_font_family, max_age=60*60*24*365)
        
        return resp
    
    return render_template('lab3/settings.html', 
                          color=current_color, 
                          bg_color=current_bg_color, 
                          font_size=current_font_size,
                          font_family=current_font_family)