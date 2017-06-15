from flask import g, make_response, jsonify
from flask_restful import Resource

from ..models import User
from . import api, token_auth, StateCode


@token_auth.verify_token
def verify_token(token):
    print(token)
    g.current_user = User.verify_auth_token(token)
    if g.current_user:
        g.token_used = True
        return True


class GetToken(Resource, StateCode):

    def get(self):
        if g.current_user is None or g.token_used:
            return {"message": "Invalid credentials"},
        return {
            "token": g.current_user.generate_confirm_token(),
            "expiration": 86400
        }, self.SUCCESS


@token_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

api.add_resource(GetToken, '/get_token/')
