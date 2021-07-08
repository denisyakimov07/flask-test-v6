import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from environment import get_env

app = Flask(__name__)
app.config['SECRET_KEY'] = get_env().FLASK_SECRET_KEY

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'{get_env().DB_DATABASE_TYPE}://{get_env().DB_USER}' \
                                 f':{get_env().DB_PASSWORD}@{get_env().DB_HOST}' \
                                 f':{get_env().DB_PORT}/{get_env().DB_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page'
login_manager.login_message_category = 'success'

from flaskblog import routes
from flaskblog.models import BlogPost, User

admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(User, db.session))

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

from flask_mail import Mail

mail = Mail(app)
