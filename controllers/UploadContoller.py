from flask import abort, request, render_template
from flask_login import login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from minio import Minio
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE, MINIO_AUDIO_BUCKET, MINIO_BOOK_COVER_BUCKET, db
from models.Object import Objects

import os
import uuid
import logging


storage = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=MINIO_SECURE)
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'mp3', 'm4a', 'wav'}
logger = logging.getLogger(__name__)

@login_required
def upload_view():

    if not bucket_exists(MINIO_AUDIO_BUCKET):
        create_bucket(MINIO_AUDIO_BUCKET)

    if not bucket_exists(MINIO_BOOK_COVER_BUCKET):
        create_bucket(MINIO_BOOK_COVER_BUCKET)
        
    return render_template('views/upload/upload.html')

@login_required
def upload_file_view():

    if request.method == 'POST':
        if request.content_length and request.content_length > MAX_UPLOAD_BYTES:
            abort(413)
        uploaded_file = request.files.get('file')
        if uploaded_file:
            new_audio = upload_content(uploaded_file, MINIO_AUDIO_BUCKET)

            return render_template('views/upload/file.html', file=new_audio)

def upload_content(upload_file, bucket_name):

    if upload_file and bucket_name:
        safe_name = secure_filename(upload_file.filename or '')
        file_extension = safe_name.rsplit('.', 1)[-1].lower() if '.' in safe_name else ''
        if file_extension not in ALLOWED_EXTENSIONS:
            abort(400, description='Unsupported file type')
        type = upload_file.content_type
        file_name = f'{str(uuid.uuid4())}.{file_extension}'
        while object_exists(bucket_name, file_name):
            file_name = str(uuid.uuid4()) + file_extension
        size = os.fstat(upload_file.fileno()).st_size
        storage.put_object(bucket_name, file_name, upload_file, size)
        now = datetime.now()
        upload_object = Objects(name=upload_file.filename, object_name=file_name, bucket=bucket_name, type=type, created_at=now, updated_at=now, creator_ip=request.remote_addr, updater_ip=request.remote_addr)
        db.session.add(upload_object)
        db.session.commit()

        return storage.presigned_get_object(bucket_name, file_name)
    
    return False

@login_required
def get_object_url(object_name):

    stored_object = Objects.query.filter_by(object_name=object_name).first_or_404()
    return storage.presigned_get_object(stored_object.bucket, stored_object.object_name)

def bucket_exists(bucket_name):

    try:
        if storage.bucket_exists(bucket_name):
            return True
    except Exception:
        logger.exception('Failed to check MinIO bucket %s', bucket_name)
        return False

    return False

def create_bucket(bucket_name):
    
    if not bucket_exists(bucket_name):
        storage.make_bucket(bucket_name)
    
def object_exists(bucket_name, object_name):

    try:
        if storage.stat_object(bucket_name, object_name):
            return True
    except Exception:
        logger.exception('Failed to check MinIO object %s/%s', bucket_name, object_name)
        return False

    return False

def get_object(bucket_name, object_name):

    if object_exists(bucket_name, object_name):
        return storage.fget_object(bucket_name, object_name, f'/tmp/{object_name}')

    return None
