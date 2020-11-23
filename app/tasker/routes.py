from flask import render_template, url_for, flash, redirect, request, Blueprint,jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User,Task
from app.tasker.forms import AddTaskForm
from datetime import datetime


tasker = Blueprint('tasker', __name__)

@tasker.route('/create_task', methods=['GET','POST'])
def create_task():
    
    form = AddTaskForm()
    
    users = User.query.all()
    tasks = Task.query.all()
    
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        task_name   = form.task_name.data
        task_detail = form.task_detail.data
        task_date   = form.task_date.data
        assigned_to = form.assigned_to.data
        
        task = Task(id=len(tasks)+1,task_name=task_name,task_detail=task_detail,task_date=task_date,
                    assigned_to=assigned_to,assigned_by=user.username,assigner_mail = user.email,
                    assigner_phone=user.phone)
        
        db.session.add(task)
        db.session.commit()
        flash('Task has been succesfully created','success')
        
        return redirect(request.referrer)
        
    
    return render_template('tasker/create_task.html', form=form,users=users)


@login_required
@tasker.route("/update_task/<task_id>/<status>")
def update_task(task_id,status):
    task = Task.query.filter_by(task_id=task_id).first()
    
    task.status = status
    db.session.merge(task)
    db.session.flush()
    db.session.commit()
    
    flash(f"Task {task.task_name} has been updated","success")
    return redirect(request.referrer)

status_list = ['Success','Extended','Complete','Incomplete','Reassigned']

@login_required
@tasker.route("/task_status_list")
def list_status():
    stats = [{'id':i,'status':status} for i,status in enumerate(status_list)]
    return jsonify(stats)

@login_required
@tasker.route("/list_tasks")
def list_task():
    tasks = Task.query.filter_by(assigned_by=current_user.id).all()
    task_list = [task.serialize for task in tasks]
    return jsonify(tasks)
