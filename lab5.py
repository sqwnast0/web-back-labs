from flask import Flask, Blueprint, request, render_template, redirect, session
import datetime

lab5 = Blueprint('lab5', __name__)

app = Flask(__name__)
app.secret_key = 'секретно-секретный секрет'

# Страница с основным списком ссылок
@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')