from datetime import datetime

from flask import g, make_response, jsonify
from flask_httpauth import HTTPTokenAuth

from app.models import User, AnonymousUser
from app.utils.web import NestableBlueprint


api_v1 = NestableBlueprint('api_v1', __name__, url_prefix='/api_v1')
token_auth = HTTPTokenAuth(scheme='token')


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.verify_auth_token(token)
    if g.current_user:
        g.token_used = True
        g.current_user.update(last_seen=datetime.utcnow())
    else:
        g.current_user = AnonymousUser()
    return True


@token_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
