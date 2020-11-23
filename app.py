import smtplib
from datetime import datetime 
from flask import (Flask,render_template, url_for, flash, redirect,
                   request, abort,jsonify)
from config import Config
from flask_bcrypt import Bcrypt
from flask_login  import (LoginManager, UserMixin, 
                          login_user, current_user, 
                          logout_user, login_required)
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Optional

#initialising the app

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    return app

app = create_app()

#defining models

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


# creating routes
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    #tasks = Task.query.all()
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email,subject, html)

        flash('A confirmation email has been sent via email.', 'success')
    return render_template('register.html', form=form, title='Register now',
                           description='Registration form for new users')

def send_email(to,subject, template):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From']    = MAIL_DEFAULT_SENDER
    msg['To']      = to
    msg.set_content(template, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.join_date:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.user_type = 1
        user.join_date = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
        flash('Go to account page to update your details', 'info')
    return redirect(url_for('home'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Login',
                           description="Login page for existing users")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


class RegistrationForm(FlaskForm):
    '''Creating user registration forms'''

    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email    = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email    = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit   = SubmitField('Login')

# setting up some random tasks
task_names = [f'task-{i}' for i in range(10)]

@app.route("/task_list")
def task_list():
    tasks = [{'id':i,'task':task} for i,task in enumerate(task_names)]
    return jsonify({'tasks':tasks})

status_list = ['Success','Extended','Complete','Incomplete','Reassigned']

@app.route("/task_status_list")
def list_status():
    stats = [{'id':i,'status':status} for i,status in enumerate(status_list)]
    return jsonify(stats)

@login_required
@app.route("/list_tasks")
def list_task():
    tasks = Task.query.filter_by(assigned_by=current_user.id).all()
    return jsonify(tasks)

@login_required
@app.route("/create_task", methods=['GET', 'POST'])
def create_task():
    form = CreateTaskForm()
    
    if form.validate_on_submit():
        task_name   = form.task_name.data
        task_date   = datetime.now()
        assigned_by = current_user.id
        assigner_ml = current_user.email
        assigner_ph = current_user.phone
        assigned_to = form.assigned_to.data
        status      = 'Incomplete'
        
        task = Task(task_name=task_name,task_date=task_date,
                    assigned_by=assigned_by,assigner_ml=assigner_ml,
                    assigner_ph=assigner_ph,assigned_to=assigned_to,
                    status=status)
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task has been succesfully created')
        return redirect(request.referrer)
    
    return render_template('create_task.html',form=form)

@login_required
@app.route("/update_task/<task_id>/<status>")
def update_task(task_id,status):
    task = Task.query.filter_by(task_id=task_id).first()
    
    task.status = status
    db.session.merge(task)
    db.session.flush()
    db.session.commit()
    
    flash(f"Task {task.task_name} has been updated","success")
    return redirect(request.referrer)





if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
