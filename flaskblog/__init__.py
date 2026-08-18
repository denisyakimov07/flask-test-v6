import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from environment import get_env

app = Flask(__name__)
app.config['SECRET_KEY'] = get_env().FLASK_SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = get_env().DB_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = get_env().MAIL_SERVER
app.config['MAIL_PORT'] = get_env().MAIL_PORT
app.config['MAIL_USE_SSL'] = get_env().MAIL_USE_SSL
app.config['MAIL_USE_TLS'] = get_env().MAIL_USE_TLS
app.config['MAIL_USERNAME'] = get_env().MAIL_USERNAME
app.config['MAIL_PASSWORD'] = get_env().MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = get_env().MAIL_DEFAULT_SENDER

db = SQLAlchemy(app)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page'
login_manager.login_message_category = 'success'

from flask_mail import Mail

mail = Mail(app)

from flask_migrate import Migrate

migrate = Migrate(app, db)

from flaskblog import routes
from flaskblog.models import BlogPost, User

admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(User, db.session))
