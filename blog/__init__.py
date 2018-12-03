from datetime import datetime

from celery import Celery
from flask import Flask, g
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_uploads import (UploadSet,
                           IMAGES,
                           configure_uploads,
                           patch_request_class)
from flask_redis import FlaskRedis

from blog.utils import assets, FlaskCaptcha, RedisSessionInterface

mail = Mail()
pagedown = PageDown()
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

celery = Celery(__name__, broker='redis://localhost:6379')

photos = UploadSet('photos', IMAGES)
flask_captcha = FlaskCaptcha()
redis_cli = FlaskRedis()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    config.init_app(app)

    configure_uploads(app, (photos, ))
    patch_request_class(app, None)
    mail.init_app(app)
    pagedown.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    assets.init_app(app)
    redis_cli.init_app(app)
    flask_captcha.init_app(app)
    app.session_interface = RedisSessionInterface(redis_cli)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_v1 import api_v1
    app.register_blueprint(api_v1)

    return app


def make_celery(app, _celery):
    _celery.conf.update(app.config)
    TaskBase = _celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    _celery.Task = ContextTask
    return _celery
