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
