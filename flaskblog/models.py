from flask_login import UserMixin
from flaskblog import db
import datetime

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email
from wtforms import validators

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1520350094754-f0fdcac35c1c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1650&q=80"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    posts = db.relationship("BlogPost", backref='owner')
    email_confirm = db.Column(db.Boolean())

    def __repr__(self):
        return f'{str(self.name)} - {str(self.id)}'


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(500), nullable=True, default=DEFAULT_IMAGE)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'id - {str(self.id)}, user_id - {str(self.user_id)}, title - {str(self.title)},content - {str(self.content)}  .'


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[Email(), DataRequired()],
                        render_kw={'placeholder': 'Email Address',
                                   'class': "form-control form-group floating-label-form-group controls"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"class": "form-label", "class": "form-control", "placeholder": "Password"})
    submit = SubmitField("Login")


class SingUpForm(FlaskForm):
    name = StringField('Name', validators=[validators.Length(min=3, max=50)], render_kw={'placeholder': 'Name',
                                                                                         'class': "form-control "
                                                                                                  "form-group "
                                                                                                  "floating-label"
                                                                                                  "-form-group "
                                                                                                  "controls"})
    email = StringField('Email address', validators=[Email(), DataRequired()],
                        render_kw={'placeholder': 'Email Address',
                                   'class': "form-control form-group floating-label-form-group controls"})
    password = PasswordField('Password', validators=[DataRequired(), validators.Length(min=8, max=20),
                                                     validators.EqualTo("confirm", message="Passwords do not match.")
                                                     ],
                             render_kw={"class": "form-label", "class": "form-control", "placeholder": "Password"})
    confirm = PasswordField('Confirm password', validators=[DataRequired()],
                            render_kw={"class": "form-label", "class": "form-control",
                                       "placeholder": "Confirm password"})


class ProfileForm(FlaskForm):
    name = StringField('Name',
                       validators=[validators.Length(min=3, max=50)],
                       render_kw={'placeholder': 'Name',
                                  'class': "form-control form-group floating-label-form-group controls"})
    email = StringField('Email address',
                        validators=[Email(), DataRequired()],

                        render_kw={'placeholder': 'Email Address',
                                   'class': "form-control form-group floating-label-form-group controls"})


class ProfileFormPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), validators.Length(min=8, max=20),
                                                     validators.EqualTo("confirm", message="Passwords do not match.")
                                                     ],
                             render_kw={"class": "form-label", "class": "form-control", "placeholder": "Password"})
    confirm = PasswordField('Confirm password', validators=[DataRequired()],
                            render_kw={"class": "form-label", "class": "form-control",
                                       "placeholder": "Confirm password"})
