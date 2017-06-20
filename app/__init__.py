# coding: utf-8
import os
from flask import Flask

# from flask_assets import Environment
# from flask_dashed.admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

from config import config
from app.utils import assets

toolbar = DebugToolbarExtension()
mail = Mail()
moment = Moment()
pagedown = PageDown()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


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

    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)

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
