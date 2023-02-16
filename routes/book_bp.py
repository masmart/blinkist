from flask import Blueprint

from controllers.BookController import book_view, bookmark, bookmark_view, reader_view

book_bp = Blueprint('book_bp', __name__)

book_bp.route('/<book_slug>', methods=['GET'])(book_view)
book_bp.route('/<book_slug>/reader/<idea>', methods=['GET'])(reader_view)
book_bp.route('/bookmark', methods=['GET', 'POST', 'DELETE'])(bookmark)
book_bp.route('/bookmark/<book_slug>/', methods=['GET'])(bookmark_view)