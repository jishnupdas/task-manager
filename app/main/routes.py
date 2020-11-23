from flask       import render_template, url_for, flash, redirect, request, Blueprint,jsonify
from flask_login import login_user, current_user, logout_user, login_required
from datetime    import datetime
from app         import db, bcrypt
from app.models  import User,Task

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    tasks = Task.query.all()
    return render_template('tasker/dashboard.html',tasks=tasks)

@main.route('/dashboard', methods=['GET','POST'])
def dashboard():
    tasks = Task.query.all()
    return render_template('tasker/dashboard.html',tasks=tasks)

@login_required
@main.route('/user_list')
def user_list():
    
    users = User.query.all()
    user_list = [{'id':user.id,'username':user.username} for user in users]
    
    return jsonify({'users':user_list})
