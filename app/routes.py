from flask import request, redirect, url_for, render_template, session
from app import app, db
from app.models import Produtos

#@app.route('/')
#def index():
 #   items_ = Produtos.query.all()
  #  return render_template('index.html', items=items_)

@app.route('/')
def index():
    items_ = Produtos.query.all()
    
    # Se o usuário não estiver logado (não existir na sessão), redireciona para o login
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona para a página de login
    
    return render_template('index.html', items=items_)

@app.route('/create', methods=['GET', 'POST'])
def create():
    # Verifica se o usuário está logado e é um administrador
    if 'role' not in session or session['role'] != 'admin':  
        return redirect(url_for('index'))  # Usuário não tem permissão, redireciona para o índice
    
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        new_produto = Produtos(nome=nome, quantidade=quantidade)
        db.session.add(new_produto)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Verifica se o usuário está logado e é um administrador
    if 'role' not in session or session['role'] != 'admin':  
        return redirect(url_for('index'))  # Usuário não tem permissão, redireciona para o índice
    
    item = Produtos.query.get_or_404(id)
    if request.method == 'POST':
        item.nome = request.form['nome']
        item.quantidade = request.form['quantidade']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    # Verifica se o usuário está logado e é um administrador
    if 'role' not in session or session['role'] != 'admin':  
        return redirect(url_for('index'))  # Usuário não tem permissão, redireciona para o índice
    
    item = Produtos.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))
