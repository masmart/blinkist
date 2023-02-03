from flask import Blueprint

from controllers.UserController import login_view, register_view, logout_view

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/login', methods=['GET', 'POST'])(login_view)
user_bp.route('/register', methods=['GET', 'POST'])(register_view)
user_bp.route('/logout', methods=['GET'])(logout_view)