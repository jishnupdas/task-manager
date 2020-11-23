from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User,Task
from app.tasker.forms import AddTaskForm
from datetime import datetime


tasker = Blueprint('tasker', __name__)

@tasker.route('/create_task')
def create_task():
    
    form = AddTaskForm()
    
    if form.validate_on_submit():
        pass
    
    return render_template('tasker/create_task.html', form=form)
