from flask       import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from datetime    import datetime
from app         import db, bcrypt
from app.models  import User,Task

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    #tasks = Task.query.all()
    return render_template('home.html')
