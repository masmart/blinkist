from flask import Blueprint

from controllers.AdminController import dashboard_view, books_view, book_view, category_view, author_view, report_view, idea_add_view, idea_edit_view


admin_bp = Blueprint('admin_bp', __name__)

admin_bp.route('/', methods=['GET'])(dashboard_view)
admin_bp.route('/books', methods=['GET'])(books_view)
admin_bp.route('/books/view', methods=['GET'])(book_view)
admin_bp.route('/books/idea/add', methods=['GET'])(idea_add_view)
admin_bp.route('/book/idea/edit', methods=['GET'])(idea_edit_view)
admin_bp.route('/category', methods=['GET'])(category_view)
admin_bp.route('/author', methods=['GET'])(author_view)
admin_bp.route('/report', methods=['GET'])(report_view)