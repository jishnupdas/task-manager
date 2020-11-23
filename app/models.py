from app import db, login_manager
from datetime         import datetime
from flask            import Flask, current_app
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
from flask_login      import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm   import backref
from itsdangerous     import TimedJSONWebSignatureSerializer as Serializer
from flask_login      import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    'User class, this creates a table in our database with the following columns'
    id          = db.Column(db.Integer,    unique=True, primary_key=True)
    phone       = db.Column(db.Integer,    nullable=True)
    email       = db.Column(db.String(90), nullable=False, unique=True)
    username    = db.Column(db.String(20), nullable=False, unique=True)
    password    = db.Column(db.String(20), nullable=False)
    address1    = db.Column(db.String(50), nullable=True)
    address_map = db.Column(db.String(60), nullable=True)
    user_type   = db.Column(db.Integer,  nullable=False, default=1)
    join_date   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.phone}')"


class Task(db.Model):
    id            = db.Column(db.Integer,    unique=True, primary_key=True)
    task_name     = db.Column(db.String(150), nullable=False)
    task_detail   = db.Column(db.String(400), nullable=True)
    task_date     = db.Column(db.String(20))
    assigned_by   = db.Column(db.String(20))
    assigner_mail = db.Column(db.String(90))
    assigner_phone= db.Column(db.Integer)
    assigned_to   = db.Column(db.String(20), db.ForeignKey('user.username'), primary_key=True)
    assignee      = db.relationship('User',lazy=True, uselist=False)
    status        = db.Column(db.String(50), nullable=False,default='Pending')
    
    def serialize(self):
        return {
        'task_id'       :self.id       ,
        'task_name'     :self.task_name     ,
        'task_detail'   :self.task_detail   ,
        'task_date'     :self.task_date     ,
        'assigned_by'   :self.assigned_by   ,
        'assigner_mail' :self.assigner_mail ,
        'assigner_phone':self.assigner_phone,
        'assigned_to'   :self.assigned_to   ,
        'assignee'      :self.assignee.username,
        'status'        :self.status
        }

class Tasklist(db.Model):
    name        = db.Column(db.String(150), unique=True, primary_key=True)
    Category    = db.Column(db.String(100))
