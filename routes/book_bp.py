from flask import Blueprint

from controllers.BookController import book_view, bookmark, bookmark_view, player_view, original_mobile_view, original_desktop_view

book_bp = Blueprint('book_bp', __name__)

book_bp.route('/<book_slug>', methods=['GET'])(book_view)
book_bp.route('/bookmark', methods=['GET', 'POST', 'DELETE'])(bookmark)
book_bp.route('/bookmark/<book_slug>/', methods=['GET'])(bookmark_view)
book_bp.route('/player', methods=['GET'])(player_view)
book_bp.route('/original_mobile', methods=['GET'])(original_mobile_view)
book_bp.route('/original_desktop', methods=['GET'])(original_desktop_view)