from flask import Blueprint, request, render_template, redirect

lab4 = Blueprint('lab4', __name__)

# Страница с основным списком ссылок
@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

# Страница с формой деления
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
        return render_template('lab4/result.html', result=result, operation="Деление", operation_symbol="/", x1=x1, x2=x2)
    
    except ValueError:
        return "Ошибка: введите корректные числа!", 400

# Суммирование
@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Преобразуем пустые поля в 0
    x1 = int(x1) if x1 else 0
    x2 = int(x2) if x2 else 0

    result = x1 + x2
    return render_template('lab4/result.html', result=result, operation="Суммирование", operation_symbol="+", x1=x1, x2=x2)

# Умножение
@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Преобразуем пустые поля в 1
    x1 = int(x1) if x1 else 1
    x2 = int(x2) if x2 else 1

    result = x1 * x2
    return render_template('lab4/result.html', result=result, operation="Умножение", operation_symbol="*", x1=x1, x2=x2)

# Вычитание
@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2:
        return "Ошибка: оба поля должны быть заполнены!", 400

    x1 = int(x1)
    x2 = int(x2)

    result = x1 - x2
    return render_template('lab4/result.html', result=result, operation="Вычитание", operation_symbol="-", x1=x1, x2=x2)

# Возведение в степень
@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2:
        return "Ошибка: оба поля должны быть заполнены!", 400

    x1 = int(x1)
    x2 = int(x2)

    # Ошибка если оба числа равны нулю
    if x1 == 0 and x2 == 0:
        return "Ошибка: возведение в степень с основанием и экспонентой равными нулю невозможно!", 400

    result = x1 ** x2
    return render_template('lab4/result.html', result=result, operation="Возведение в степень", operation_symbol="^", x1=x1, x2=x2)
# Начальное количество деревьев
tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    # Обработка метода GET
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    # Обработка метода POST
    if request.method == 'POST':
        operation = request.form.get('operation')
        
        if operation == 'cut' and tree_count > 0:
            tree_count -= 1
        elif operation == 'plant' and tree_count < 10:
            tree_count += 1
        
        # Перенаправление на ту же страницу, чтобы предотвратить повторную отправку данных
        return redirect('/lab4/tree')