from flask import g, make_response, jsonify

from app.models import User
from app.api_v1 import token_auth


@token_auth.verify_token
def verify_token(token):
    print(token)
    g.current_user = User.verify_auth_token(token)
    if g.current_user:
        g.token_used = True
        return True


@token_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
