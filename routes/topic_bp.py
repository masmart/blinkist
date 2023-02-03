from flask import Blueprint

from controllers.TopicController import index, store, show, update, delete

topic_bp = Blueprint('topic_bp', __name__)

topic_bp.route('/', methods=['GET'])(index)
topic_bp.route('/create', methods=['GET', 'POST'])(store)
topic_bp.route('/<int:topic_id>', methods=['GET'])(show)
topic_bp.route('/<int:topic_id>/edit', methods=['POST'])(update)
topic_bp.route('/<int:topic_id>', methods=['DELETE'])(delete)