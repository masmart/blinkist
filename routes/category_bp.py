from flask import Blueprint

from controllers.CategoryController import category_list_view, category_view

category_bp = Blueprint('category_bp', __name__)

category_bp.route('/', methods=['GET'])(category_list_view)
category_bp.route('/<category_slug>', methods=['GET'])(category_view)