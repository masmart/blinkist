from flask import Blueprint

from controllers.CollectionController import collection_view
collection_bp = Blueprint('collection_bp', __name__)

collection_bp.route('/<slug>', methods=['GET'])(collection_view)