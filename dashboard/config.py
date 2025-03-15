import os
from dotenv import load_dotenv
from datetime import timedelta
from flask import current_app

__all__ = ['BaseConfig', 'DevelopmentConfig', 'TestingConfig', 'ProductionConfig']

load_dotenv()


class BaseConfig(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = None
    TRAP_HTTP_EXCEPTIONS = False
    TRAP_BAD_REQUEST_ERRORS = None
    SECRET_KEY = None
    SECRET_KEY_FALLBACKS = None
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_PARTITIONED = False
    SESSION_COOKIE_SAMESITE = None
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_REFRESH_EACH_REQUEST = True
    USE_X_SENDFILE = False
    SEND_FILE_MAX_AGE_DEFAULT = None
    TRUSTED_HOSTS = None
    SERVER_NAME = None
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'
    MAX_CONTENT_LENGTH = None
    MAX_FORM_MEMORY_SIZE = 500_000
    MAX_FORM_PARTS = 1_000
    TEMPLATES_AUTO_RELOAD = None
    EXPLAIN_TEMPLATE_LOADING = False
    MAX_COOKIE_SIZE = 4093
    PROVIDE_AUTOMATIC_OPTIONS = False
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')
    ALEMBIC_PATH = os.environ.get('ALEMBIC_PATH')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')


class ProductionConfig(BaseConfig):
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')