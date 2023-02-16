from flask import Blueprint

from controllers.UploadContoller import upload_view, upload_file_view, content_view


upload_bp = Blueprint('upload_bp', __name__)

upload_bp.route('/', methods=['GET'])(upload_view)
upload_bp.route('/file', methods=['GET', 'POST'])(upload_file_view)
upload_bp.route('/content/<object_name>', methods=['GET'])(content_view)