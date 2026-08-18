"""Flask configuration."""
from os import environ, path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from itsdangerous import URLSafeSerializer, SignatureExpired
from flask_admin import Admin

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY', 'dev-only-change-me')
APP_NAME = 'Blinkist'

db = SQLAlchemy()
login_manager = LoginManager()
serializer = URLSafeSerializer(SECRET_KEY)
basedir = path.abspath(path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'postgresql://127.0.0.1:5432/blinkist')
SQLALCHEMY_TRACK_MODIFICATIONS=False

admin = Admin()
admin.template_mode = 'bootstrap4'

MINIO_ENDPOINT = environ.get('MINIO_ENDPOINT', '127.0.0.1:9000')
MINIO_ACCESS_KEY = environ.get('MINIO_ACCESS_KEY', '')
MINIO_SECRET_KEY = environ.get('MINIO_SECRET_KEY', '')
MINIO_AUDIO_BUCKET = 'audio'
MINIO_BOOK_COVER_BUCKET = 'cover'
MINIO_SECURE = environ.get('MINIO_SECURE', 'false').lower() == 'true'
