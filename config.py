"""Flask configuration."""
from os import environ, path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from itsdangerous import URLSafeSerializer, SignatureExpired
from flask_admin import Admin

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
APP_NAME = 'Blinkist'

db = SQLAlchemy()
login_manager = LoginManager()
serializer = URLSafeSerializer(SECRET_KEY)
basedir = path.abspath(path.dirname(__file__))

SQLALCHEMY_DATABASE_URI='postgresql://mehrdad:1322@127.0.0.1:5432/blinkist'
SQLALCHEMY_TRACK_MODIFICATIONS=False

admin = Admin()
admin.template_mode = 'bootstrap4'

MINIO_ENDPOINT = 'cdn.vicruite.com:9000'
MINIO_ACCESS_KEY = '14ANWkj7dciMuISr'
MINIO_SECRET_KEY = 'lMVQqAIysyJgL4MUfAPTMpYpAyRJEIM3'
MINIO_AUDIO_BUCKET = 'audio'
MINIO_BOOK_COVER_BUCKET = 'cover'
MINIO_SECURE = True