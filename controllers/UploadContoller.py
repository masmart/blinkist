from flask import abort, current_app, render_template, request
from flask_login import login_required

from services.storage import StorageService


storage_service = StorageService()


@login_required
def upload_view():
    storage_service.ensure_bucket(current_app.config['MINIO_AUDIO_BUCKET'])
    storage_service.ensure_bucket(current_app.config['MINIO_BOOK_COVER_BUCKET'])
    return render_template('views/upload/upload.html')


@login_required
def upload_file_view():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            try:
                new_audio = upload_content(uploaded_file, current_app.config['MINIO_AUDIO_BUCKET'])
            except ValueError as error:
                abort(400, description=str(error))
            return render_template('views/upload/file.html', file=new_audio)
    return render_template('views/upload/file.html', file=None)


def upload_content(upload_file, bucket_name):
    return storage_service.upload(upload_file, bucket_name, request.remote_addr)


@login_required
def get_object_url(object_name):
    url = storage_service.get_url(object_name)
    if url is None:
        abort(404)
    return url
