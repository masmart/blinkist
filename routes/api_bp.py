from flask import Blueprint

from controllers.APIController import search, search_author


api_bp = Blueprint('api_bp', __name__)

api_bp.route('/search', methods=['GET'])(search)
api_bp.route('/search/author', methods=['GET'])(search_author)