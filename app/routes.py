from flask import request, redirect, url_for, render_template
from app import app,db
from app.models import Produtos

@app.route('/')
def index():
    items_ = Produtos.quer.all()
    return render_template('index.html', items=items_)