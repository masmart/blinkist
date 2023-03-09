from flask import request, render_template, url_for, send_file
from datetime import datetime
from minio import Minio
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE, MINIO_AUDIO_BUCKET, MINIO_BOOK_COVER_BUCKET, db
from models.Object import Objects

import os
import uuid


storage = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=MINIO_SECURE)

def upload_view():

    if not bucket_exists(MINIO_AUDIO_BUCKET):
        create_bucket(MINIO_AUDIO_BUCKET)

    if not bucket_exists(MINIO_BOOK_COVER_BUCKET):
        create_bucket(MINIO_BOOK_COVER_BUCKET)
        
    return render_template('views/upload/upload.html')

def upload_file_view():

    if request.method == 'POST':
        uploaded_file = request.files['file']
        print(uploaded_file)
        if uploaded_file:
            new_audio = upload_content(uploaded_file, MINIO_AUDIO_BUCKET)

            return render_template('views/upload/file.html', file=new_audio)

def upload_content(upload_file, bucket_name):

    if upload_file and bucket_name:
        type = upload_file.content_type
        file_extension = upload_file.filename.split('.')[-1]
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

def get_object_url(object_name):

    return storage.presigned_get_object(bucket_name, object_name)

def bucket_exists(bucket_name):

    try:
        if storage.bucket_exists(bucket_name):
            return True
    except:
        return False

    return False

def create_bucket(bucket_name):
    
    if not bucket_exists(bucket_name):
        storage.make_bucket(bucket_name)
    
def object_exists(bucket_name, object_name):

    try:
        if storage.stat_object(bucket_name, object_name):
            return True
    except:
        return False

    return False

def get_object(bucket_name, object_name):

    if object_exists(bucket_name, object_name):
        return storage.fget_object(bucket_name, object_name, f'/tmp/{object_name}')

    return None