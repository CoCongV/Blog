# coding: utf-8
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from raven.contrib.flask import Sentry
from whoosh.analysis import StemmingAnalyzer

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '272c635e-a0b2-49b1-9a8b-afc671f850ee'
    SSL_DISABLE = False

    # CACHE CONFIG
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'blog:'
    CACHE_REDIS_DB = 1

    # FLASK EMAIL
    FLASK_MAIL_SUBJECT_PREFIX = '[Cong\' Blog]'
    FLASK_MAIL_SENDER = os.environ.get('FLASK_MAIL_SENDER')
    FLASK_ADMIN = os.environ.get('BLOG_ADMIN')

    # mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # FILE UPLOAD
    # UPLOADED_PHOTOS_DEST = './app/media/photos'
    UPLOADED_DEFAULT_DEST = '/tmp/blog'
    UPLOADED_DEFAULT_URL = '/media/'
    UPLOADED_PHOTOS_DEST = os.path.join(UPLOADED_DEFAULT_DEST, 'photos/')
    UPLOADED_PHOTOS_URL = os.path.join(UPLOADED_DEFAULT_URL, 'images/')
    UPLOADED_FILES_DEST = os.path.join(UPLOADED_DEFAULT_DEST, 'files/')
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'webp']
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # sqlalchemy config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BLOG_POST_PER_PAGE = 10
    BLOG_COMMENT_PAGE = 10
    BLOG_SLOW_DB_QUERY_TIME = 0.1
    FLASKY_DB_QUERY_TIMEOUT = 0.5

    # LOGIN
    LOGIN_TOKEN = 60 * 60 * 24

    # whoosh config
    WHOOSH_BASE = '/tmp/whoosh/base'
    WHOOSH_ANALYZER = StemmingAnalyzer()
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # celery config
    BROKER_URL = 'redis://172.17.0.2:6379'
    CELERY_RESULT_BACKEND = 'redis://172.17.0.2:6379/0'

    # Redis
    REDIS_URL = 'redis://172.17.0.2:6379'

    # logger
    LOG_NAME = 'blog.log'
    LOG_PATH = '/logs/blog/'
    LOG_TIME = 'D'
    LOG_BACK_COUNT = 10

    CAPTCHA_FONTS_PATH = [os.path.join(basedir, 'fonts/NotoSans-Regular.ttf')]

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://lvcong:password@/blog_dev'
    BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    REDIS_URL = 'redis://localhost:6379'


class TestingConfig(Config):
    WTF_CSRF_ENABLE = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://docker:docker@172.17.0.2/blog_test'


class DockerConfig(TestingConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://docker:docker@/blog_test'


class ProductionConfig(Config):
    SERVER_NAME = os.environ.get('ADDRESS')
    SQLALCHEMY_DATABASE_URI = 'postgresql://lvcong:password@/flask_blog'
    DEBUG = False

    # SENTRY CONFIGURE
    SENTRY_DSN = os.environ.get('SENTRY_DSN')

    @classmethod
    def init_app(cls, app):
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()

        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASK_MAIL_SENDER,
            toaddrs=[cls.FLASK_ADMIN],
            subject=cls.FLASK_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        logfile = os.path.join(cls.LOG_PATH, cls.LOG_NAME)
        file_handler = TimedRotatingFileHandler(
            logfile, when=cls.LOG_TIME, backupCount=cls.LOG_BACK_COUNT)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        sentry = Sentry()
        sentry.init_app(
            app, dsn=cls.SENTRY_DSN, logging=True, level=logging.ERROR)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
