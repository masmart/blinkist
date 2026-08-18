import logging

from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, InputRequired

from services.auth import AuthService


logger = logging.getLogger(__name__)
auth_service = AuthService()


class UserForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), DataRequired()])


def login_view():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = auth_service.authenticate(form.email.data, form.password.data)
        if user:
            login_user(user, remember=True)
            return redirect(url_for('dashboard_bp.dashboard_view'))
    return render_template('views/user/login.html', form=form)


def register_view():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = auth_service.register(form.email.data, form.password.data, request.remote_addr)
        if user:
            login_user(user, remember=True)
            return redirect(url_for('dashboard_bp.dashboard_view'))
    return render_template('views/user/register.html', form=form)


@login_required
def logout_view():
    logout_user()
    return redirect('/')


# Compatibility helpers retained for existing imports.
def register(email, password):
    try:
        user = auth_service.register(email, password, request.remote_addr)
        if user:
            login_user(user, remember=True)
        return user is not None
    except Exception:
        logger.exception('Failed to register user')
        return False


def check_user(email):
    return auth_service.find_by_email(email) is not None


def login(email, password):
    user = auth_service.authenticate(email, password)
    if user:
        login_user(user, remember=True)
        return True
    return False
