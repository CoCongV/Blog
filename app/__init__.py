# coding: utf-8
from celery import Celery
from flask import Flask
from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import (UploadSet,
                           IMAGES,
                           configure_uploads,
                           patch_request_class)

from config import config
from app.utils import assets

toolbar = DebugToolbarExtension()
mail = Mail()
pagedown = PageDown()
db = SQLAlchemy()
cache = Cache()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

celery = Celery(__name__, broker='redis://localhost:6379')

photos = UploadSet('photos', IMAGES)


def create_app(config_name):
    # global app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    _config = config[config_name]
    _config.init_app(app)

    configure_uploads(app, (photos, ))
    patch_request_class(app, None)
    # toolbar.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    assets.init_app(app)
    cache.init_app(app)

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
