from os import environ

from flask import Blueprint, abort
from flask_login import current_user

from controllers.AdminController import dashboard_view, books_view, book_add_view, book_edit_view, categories_view, authors_view, report_view, idea_add_view, idea_edit_view, audio_add_view, audio_edit_view, category_add_view, category_edit_view, author_add_view, author_edit_view


admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.before_request
def require_admin():
    admin_emails = {
        email.strip().lower()
        for email in environ.get('ADMIN_EMAILS', '').split(',')
        if email.strip()
    }
    if not current_user.is_authenticated:
        abort(401)
    if current_user.email.lower() not in admin_emails:
        abort(403)

admin_bp.route('/', methods=['GET'])(dashboard_view)
admin_bp.route('/books', methods=['GET'])(books_view)
admin_bp.route('/books/edit', methods=['GET', 'POST'])(book_edit_view)
admin_bp.route('/books/add', methods=['GET', 'POST'])(book_add_view)
admin_bp.route('/books/idea/add', methods=['GET', 'POST'])(idea_add_view)
admin_bp.route('/book/idea/edit', methods=['GET', 'POST'])(idea_edit_view)
admin_bp.route('/books/audio/add', methods=['GET', 'POST'])(audio_add_view)
admin_bp.route('/books/audio/edit', methods=['GET', 'POST'])(audio_edit_view)
admin_bp.route('/categories', methods=['GET'])(categories_view)
admin_bp.route('/categories/add', methods=['GET', 'POST'])(category_add_view)
admin_bp.route('/categories/edit', methods=['GET', 'POST'])(category_edit_view)
admin_bp.route('/authors', methods=['GET'])(authors_view)
admin_bp.route('/authors/add', methods=['GET', 'POST'])(author_add_view)
admin_bp.route('/authors/edit', methods=['GET', 'POST'])(author_edit_view)
admin_bp.route('/report', methods=['GET'])(report_view)
