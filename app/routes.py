from flask_login import logout_user, login_required, current_user, login_user
from flask import request, redirect, url_for, render_template, session, flash
from app import app, db
from app.models import Produtos, User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

# Definição do formulário de login com Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])

@app.route('/')
def index():
    items_ = Produtos.query.all()
    
    # Se o usuário não estiver logado, redireciona para o login
    if not current_user.is_authenticated:
        return redirect(url_for('login')) 
    
    return render_template('index.html', items=items_)

@app.route('/create', methods=['GET', 'POST'])
@login_required  # Garante que somente usuários logados possam acessar essa rota
def create():
    
    if current_user.role != 'admin':  
        flash('Você não tem permissão para acessar esta página!', 'error')
        return redirect(url_for('index'))  # Se o usuário não tiver permissão, redireciona para o início
    
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        new_produto = Produtos(nome=nome, quantidade=quantidade)
        db.session.add(new_produto)
        db.session.commit()
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required  
def update(id):
    if current_user.role != 'admin':  
        flash('Você não tem permissão para acessar esta página!', 'error')
        return redirect(url_for('index')) 
    
    item = Produtos.query.get_or_404(id)
    if request.method == 'POST':
        item.nome = request.form['nome']
        item.quantidade = request.form['quantidade']
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
@login_required  
def delete(id):
    if current_user.role != 'admin':  
        flash('Você não tem permissão para acessar esta página!', 'error')
        return redirect(url_for('index')) 
    
    item = Produtos.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required  
def logout():
    logout_user()  
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Caso o usuário já esteja logado, redireciona para a página inicial
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)

            # Redireciona o usuário para a página que ele tentou acessar (se disponível)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))  

        flash('Usuário ou senha inválidos', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required  
def register():
    if current_user.role != 'admin':  
        flash('Você não tem permissão para acessar esta página!', 'error')
        return redirect(url_for('index'))  
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  
        
        # Verifica se o nome de usuário já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Usuário ja cadastrado!', 'error')
            return render_template('register.html')  

        # Cria o novo usuário
        new_user = User(username=username, role=role)
        new_user.set_password(password)  

        db.session.add(new_user)
        db.session.commit()
        
        flash('Novo usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))  
    
    return render_template('register.html')  
