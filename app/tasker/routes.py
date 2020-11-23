from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User,Task
from app.users.forms import (RegistrationForm, LoginForm)
from datetime import datetime


tasker = Blueprint('tasker', __name__)
