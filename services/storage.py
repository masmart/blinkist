from datetime import datetime
import os
import uuid
from flask import current_app
from minio import Minio
from werkzeug.utils import secure_filename
from config import db
from models.Object import Objects
from services.unit_of_work import transaction


class StorageService:
    allowed_extensions = {'jpg', 'jpeg', 'png', 'webp', 'mp3', 'm4a', 'wav'}

    def __init__(self, client=None):
        self._client = client

    @property
    def client(self):
        if self._client is None:
            self._client = Minio(current_app.config['MINIO_ENDPOINT'], access_key=current_app.config['MINIO_ACCESS_KEY'], secret_key=current_app.config['MINIO_SECRET_KEY'], secure=current_app.config['MINIO_SECURE'])
        return self._client

    def ensure_bucket(self, bucket):
        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

    def upload(self, uploaded_file, bucket, client_ip):
        safe_name = secure_filename(uploaded_file.filename or '')
        extension = safe_name.rsplit('.', 1)[-1].lower() if '.' in safe_name else ''
        if extension not in self.allowed_extensions:
            raise ValueError('Unsupported file type')
        object_name = f'{uuid.uuid4()}.{extension}'
        size = os.fstat(uploaded_file.fileno()).st_size
        self.ensure_bucket(bucket)
        self.client.put_object(bucket, object_name, uploaded_file, size)
        now = datetime.now()
        stored = Objects(name=safe_name, object_name=object_name, bucket=bucket, type=uploaded_file.content_type, created_at=now, updated_at=now, creator_ip=client_ip, updater_ip=client_ip)
        try:
            with transaction() as session:
                session.add(stored)
        except Exception:
            self.client.remove_object(bucket, object_name)
            raise
        return self.client.presigned_get_object(bucket, object_name)

    def get_url(self, object_name):
        stored = Objects.query.filter_by(object_name=object_name).first()
        if stored is None:
            return None
        return self.client.presigned_get_object(stored.bucket, stored.object_name)
