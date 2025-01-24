from flask_login import logout_user, login_required, current_user, login_user
from flask import request, redirect, url_for, render_template, session, flash
from app import app, db
from app.models import Produtos, User

@app.route('/')
def index():
    items_ = Produtos.query.all()
    
    # Se o usuário não estiver logado, redireciona para o login
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Redireciona para a página de login
    
    return render_template('index.html', items=items_)

@app.route('/create', methods=['GET', 'POST'])
@login_required  # Garante que somente usuários logados possam acessar
def create():
    # Verifica se o usuário é o admin
    if current_user.role != 'admin':  
        flash('Você não tem permissão para acessar esta página', 'danger')
        return redirect(url_for('index'))  # Usuário não tem permissão, redireciona para o início
    
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        new_produto = Produtos(nome=nome, quantidade=quantidade)
        db.session.add(new_produto)
        db.session.commit()
        flash('Produto criado com sucesso!', 'sucess')
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required  
def update(id):
    if current_user.role != 'admin':  
        flash('Você não tem permissão para acessar esta página', 'danger')
        return redirect(url_for('index')) 
    
    item = Produtos.query.get_or_404(id)
    if request.method == 'POST':
        item.nome = request.form['nome']
        item.quantidade = request.form['quantidade']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
@login_required  # Garante que somente usuários logados possam acessar
def delete(id):
    if current_user.role != 'admin':  
        flash('Você não tem permissão para acessar esta página', 'danger')
        return redirect(url_for('index')) 
    
    item = Produtos.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout')
@login_required  # Garante que somente usuários logados possam acessar
def logout():
    logout_user()  # Logout do usuário
    return redirect(url_for('login'))  # Redireciona para a página de login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Caso o usuário já esteja logado, redireciona para a página inicial
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)

            # Redireciona o usuário para a página que ele tentou acessar (se disponível)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))  # Caso contrário, redireciona para a página inicial

        flash('Usuário ou senha inválidos', 'danger')
    
    return render_template('login.html')