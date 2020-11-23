from flask   import current_app
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, IntegerField, SelectField, DateField
from app.models  import User, Task
from flask_wtf   import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, Optional, ValidationError

class AddTaskForm(FlaskForm):
    'adding tasks'
    task_name   = StringField('Task', validators=[DataRequired()])
    task_detail = TextAreaField('Task description', validators=[Optional()])
    task_date   = DateField('Due date', validators=[DataRequired()])
    assigned_to = SelectField('Assigned to', validators=[DataRequired()])
    submit      = SubmitField('Add task')
    
    
