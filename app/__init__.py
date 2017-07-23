# coding: utf-8
from celery import Celery
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache

from config import config
from app.utils import assets
# from app.lib.celery import FlaskCelery

toolbar = DebugToolbarExtension()
mail = Mail()
moment = Moment()
pagedown = PageDown()
db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

celery = Celery(__name__, broker='redis://localhost:6379')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    toolbar.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    assets.init_app(app)
    cache.init_app(app)
    # celery.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_v1.post import api_post
    app.register_blueprint(api_post)

    from .api_v1.auth import api_auth
    app.register_blueprint(api_auth)

    from .api_v1.user import api_user
    app.register_blueprint(api_user)

    from .api_v1.comment import api_comment
    app.register_blueprint(api_comment)

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
