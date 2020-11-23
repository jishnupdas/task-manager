from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login  import LoginManager
from flask_login  import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    'User class, this creates a table in our database with the following columns'
    id          = db.Column(db.Integer, unique=True, primary_key=True)
    phone       = db.Column(db.Integer, nullable=True)
    email       = db.Column(db.String(90), unique=True, nullable=False)
    username    = db.Column(db.String(20), unique=True, nullable=False)
    password    = db.Column(db.String(20), nullable=False)
    address1    = db.Column(db.String(50), nullable=True)
    address_map = db.Column(db.String(60), nullable=True)
    join_date   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_type   = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username,self.email,self.phone)


class Task(db.Model):
    task_id     = db.Column(db.Integer, unique=True, primary_key=True)
    task_name   = db.Column(db.String(50), nullable=False)
    task_date   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    assigned_by = db.Column(db.Integer)
    assigner_ml = db.Column(db.String(90))
    assigner_ph = db.Column(db.Integer)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    assignee    = db.relationship('User',lazy=True, uselist=False)
    status      = db.Column(db.String(50), nullable=False,default='Incomplete')
