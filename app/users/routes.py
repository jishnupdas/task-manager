from flask       import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from datetime    import datetime
from app         import db, bcrypt
from app.models  import User,Task
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from email.message import EmailMessage
from app.users.forms import RegistrationForm, LoginForm
import smtplib

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # use this for email confirmation
        #token = generate_confirmation_token(user.email)
        #confirm_url = url_for('confirm_email', token=token, _external=True)
        #html = render_template('users/activate.html', confirm_url=confirm_url)
        #subject = "Please confirm your email"
        #send_email(user.email,subject, html)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for('main.home'))
    return render_template('users/register.html', form=form, title='Register now',
                           description='Registration form for new users')

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def send_email(to,subject, template):
    message = EmailMessage()
    message['To']      = to
    message['From']    = MAIL_DEFAULT_SENDER
    message['Subject'] = subject
    message.set_content(template, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(message)

@users.route('/confirm/<token>')
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
    return redirect(url_for('main.home'))

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('users/login.html', form=form, title='Login',
                           description="Login page for existing users")

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


