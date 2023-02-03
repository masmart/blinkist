from flask import Blueprint

from controllers.AuthorController import index, store, show, update, delete

author_bp = Blueprint('author_bp', __name__)

author_bp.route('/', methods=['GET'])(index)
author_bp.route('/create', methods=['GET', 'POST'])(store)
author_bp.route('/<int:author_id>', methods=['GET'])(show)
author_bp.route('/<int:author_id>/edit', methods=['POST'])(update)
author_bp.route('/<int:author_id>', methods=['DELETE'])(delete)