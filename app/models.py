from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # "user" ou "admin"

    def set_password(self, password):
        self.password = generate_password_hash(password)  # Criptografa a senha

    def check_password(self, password):
        return check_password_hash(self.password, password)  # Verifica a senha criptografada