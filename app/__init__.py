from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = 'random_secret_key'
app.config.from_object('config.Config')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes, models