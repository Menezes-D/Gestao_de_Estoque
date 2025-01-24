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
        return redirect(url_for('login'))  # Redireciona para a página de login
    
    return render_template('index.html', items=items_)

@app.route('/create', methods=['GET', 'POST'])
@login_required  # Garante que somente usuários logados possam acessar
def create():
    # Verifica se o usuário é o admin
    if current_user.role != 'admin':  
        flash('Você não tem permissão para acessar esta página!', 'error')
        return redirect(url_for('index'))  # Usuário não tem permissão, redireciona para o início
    
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
        flash('Você não tem permissão para acessar esta págin!', 'error')
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
@login_required  # Garante que somente usuários logados possam acessar
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
@login_required  # Garante que somente usuários logados possam acessar
def logout():
    logout_user()  # Logout do usuário
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))  # Redireciona para a página de login

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
                return redirect(url_for('index'))  # Caso contrário, redireciona para a página inicial

        flash('Usuário ou senha inválidos', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required  # Garante que apenas usuários logados possam acessar
def register():
    if current_user.role != 'admin':  # Verifica se o usuário é administrador
        flash('Você não tem permissão para acessar esta página!', 'error')
        return redirect(url_for('index'))  # Caso contrário, redireciona para a página inicial
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Pode ser "admin" ou "user"
        
        # Verifica se o username já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username já existe!', 'danger')
            return render_template('register.html')  # Retorna o formulário de registro com mensagem de erro

        # Cria o novo usuário
        new_user = User(username=username, role=role)
        new_user.set_password(password)  # Criptografa a senha

        db.session.add(new_user)
        db.session.commit()
        
        flash('Novo usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))  # Redireciona para a página principal após sucesso
    
    return render_template('register.html')  # Retorna o formulário de cadastro
