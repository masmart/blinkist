from flask import Blueprint

from controllers.APIController import search


api_bp = Blueprint('api_bp', __name__)

api_bp.route('/search', methods=['GET'])(search)