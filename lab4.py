from flask import Blueprint, url_for, request, redirect, render_template, abort
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

# Страница с формой
@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

# Обработчик для деления
@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Проверка на пустые поля
    if not x1 or not x2:
        return "Ошибка: оба поля должны быть заполнены!", 400
    
    try:
        x1 = int(x1)
        x2 = int(x2)
        
        if x2 == 0:
            return "Ошибка: деление на ноль невозможно!", 400

        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return "Ошибка: введите корректные числа!", 400