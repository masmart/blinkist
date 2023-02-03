
from flask import render_template, redirect, url_for, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user, current_user, login_required
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired
from datetime import datetime
from random import randrange
import sys

from config import db, login_manager, serializer
from models.User import Users
from models.Book import Books
from models.Category import Categories

class UserForm(FlaskForm):

    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), DataRequired()])

def login_view():

    form = UserForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = login(email, password)
        if user:
            print(current_user.email)
            return redirect(url_for('dashboard_bp.dashboard_view'))

    return render_template('views/user/login.html', form=form)

def register_view():

    form = UserForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if register(email, password):
            return redirect(url_for('dashboard_bp.dashboard_view'))

    return render_template('views/user/register.html', form=form)

@login_required
def logout_view():

    logout_user()
    return redirect('/')

def register(email, password):

    if check_user(email):
        return False
    
    hashed_password = generate_password_hash(password, method='SHA256')
    session_token = serializer.dumps([email, password])
    created_at = datetime.now()
    creator_ip = request.remote_addr
    updated_at = created_at
    updater_ip = creator_ip
    
    try:
        user = Users(email=email, password=hashed_password, session_token=session_token, created_at=created_at, creator_ip=creator_ip, updated_at=updated_at, updater_ip=updater_ip)
        db.session.add(user)
        db.session.commit()
        login(email, password)
        return True
    except:
        return False

def check_user(email):
    
        user = Users.query.filter(Users.email == email).first()
    
        if user:
            return True
        else:
            return False

def login(email, password):
    
        user = Users.query.filter(Users.email == email).first()
    
        if user:
            if check_password_hash(user.password, password):
                user.session_token = serializer.dumps([email, password])
                db.session.commit()
                login_user(user, remember=True)
                return True
            else:
                return 'Wrong password'
        else:
            return 'User not exist'


