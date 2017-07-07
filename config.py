# coding: utf-8
import os
import logging

from whoosh.analysis import StemmingAnalyzer

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '272c635e-a0b2-49b1-9a8b-afc671f850ee'
    SSL_DISABLE = False

    FLASK_MAIL_SUBJECT_PREFIX = '[Cong\' Blog]'
    FLASK_MAIL_SENDER = 'cong.lv.blog@gmail.com'
    FLASK_ADMIN = os.environ.get('BLOG_ADMIN')
    UPLOADED_PHOTOS_DEST = './media/photos'
    UPLOADED_FILES_DEST = './media/files'
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'webp']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # sqlalchemy config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BLOG_POST_PER_PAGE = 10
    BLOG_COMMENT_PAGE = 10
    BLOG_SLOW_DB_QUERY_TIME = 0.1
    FLASKY_DB_QUERY_TIMEOUT = 0.5
    # mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # whoosh config
    WHOOSH_BASE = '/tmp/whoosh/base'
    WHOOSH_ANALYZER = StemmingAnalyzer()
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # celery config
    BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    _LOG_FILE = './log/'
    _MAX_LOG_SIZE = 10 * 1024 * 1024
    _FORMAT = '[%(time)r][%(level)r][%(filename)r:%(line)d][%(threadName)r]: %(message)r'
    _LOG_LEVEL = logging.DEBUG
    _formatter = logging.Formatter(_FORMAT)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://lvcong:password@localhost/flask_blog'


class TestingConfig(Config):
    WTF_CSRF_ENABLE = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://lvcong:password@localhost/flask_test'


class ProductionConfig(Config):
    SERVER_NAME = os.environ.get('ADDRESS')
    SQLALCHEMY_DATABASE_URI = 'postgresql://lvcong:password@localhost/flask_blog'
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        import logging
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
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
        }
