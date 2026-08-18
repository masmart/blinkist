"""Application configuration and extension instances."""
from os import environ

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin()
admin.template_mode = 'bootstrap4'


def _as_bool(name, default=False):
    return environ.get(name, str(default)).lower() == 'true'


class BaseConfig:
    APP_NAME = 'Blinkist'
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get(
        'DATABASE_URL', 'postgresql://127.0.0.1:5432/blinkist'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    MINIO_ENDPOINT = environ.get('MINIO_ENDPOINT', '127.0.0.1:9000')
    MINIO_ACCESS_KEY = environ.get('MINIO_ACCESS_KEY', '')
    MINIO_SECRET_KEY = environ.get('MINIO_SECRET_KEY', '')
    MINIO_AUDIO_BUCKET = environ.get('MINIO_AUDIO_BUCKET', 'audio')
    MINIO_BOOK_COVER_BUCKET = environ.get('MINIO_BOOK_COVER_BUCKET', 'cover')
    MINIO_SECURE = _as_bool('MINIO_SECURE')


class DevelopmentConfig(BaseConfig):
    DEBUG = _as_bool('DEBUG')
    SECRET_KEY = BaseConfig.SECRET_KEY or 'dev-only-change-me'


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = BaseConfig.SECRET_KEY or 'test-only-secret'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


CONFIG_BY_NAME = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}


def get_config(name=None):
    """Return the selected config class and validate production secrets."""
    environment = (name or environ.get('FLASK_ENV', 'production')).lower()
    config_class = CONFIG_BY_NAME.get(environment, ProductionConfig)
    if config_class is ProductionConfig and not config_class.SECRET_KEY:
        raise RuntimeError('SECRET_KEY must be set in production')
    return config_class


# Backwards-compatible aliases for modules that will move to injected services.
MINIO_ENDPOINT = BaseConfig.MINIO_ENDPOINT
MINIO_ACCESS_KEY = BaseConfig.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = BaseConfig.MINIO_SECRET_KEY
MINIO_AUDIO_BUCKET = BaseConfig.MINIO_AUDIO_BUCKET
MINIO_BOOK_COVER_BUCKET = BaseConfig.MINIO_BOOK_COVER_BUCKET
MINIO_SECURE = BaseConfig.MINIO_SECURE
