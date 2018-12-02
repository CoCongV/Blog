from datetime import datetime

from flask import g, make_response, jsonify, current_app
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized

from blog.models import User, AnonymousUser
from blog.utils.web import NestableBlueprint


api_v1 = NestableBlueprint('api_v1', __name__, url_prefix='/api/v1')
token_auth = HTTPTokenAuth(scheme='token')


@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user:
        g.current_user = user
        g.token_used = True
        g.current_user.update(last_seen=datetime.utcnow())
    else:
        g.current_user = AnonymousUser()
    return True


@token_auth.error_handler
def unauthorized():
    return Unauthorized()


from .post import api_post
from .user import api_user
from .comment import api_comment
from .auth import api_auth

api_v1.register_blueprint(api_post)
api_v1.register_blueprint(api_user)
api_v1.register_blueprint(api_comment)
api_v1.register_blueprint(api_auth)
