from flask import Blueprint

from controllers.AdminController import dashboard_view, books_view, book_add_view, book_edit_view, category_view, author_view, report_view, idea_add_view, idea_edit_view, audio_add_view


admin_bp = Blueprint('admin_bp', __name__)

admin_bp.route('/', methods=['GET'])(dashboard_view)
admin_bp.route('/books', methods=['GET'])(books_view)
admin_bp.route('/books/edit', methods=['GET', 'POST'])(book_edit_view)
admin_bp.route('/books/add', methods=['GET', 'POST'])(book_add_view)
admin_bp.route('/books/idea/add', methods=['GET', 'POST'])(idea_add_view)
admin_bp.route('/book/idea/edit', methods=['GET', 'POST'])(idea_edit_view)
admin_bp.route('/books/audio/add', methods=['GET'])(audio_add_view)
admin_bp.route('/category', methods=['GET'])(category_view)
admin_bp.route('/author', methods=['GET'])(author_view)
admin_bp.route('/report', methods=['GET'])(report_view)