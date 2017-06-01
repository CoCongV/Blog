from flask import g
from flask_restful import Api, reqparse, abort, Resource
from flask_httpauth import HTTPBasicAuth

from ..models import User
from . import api

auth = HTTPBasicAuth()


class Login(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json')
        self.reqparse.add_argument('password', type=str, required=True, location='json')
        super(Login, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password']
        user = User.query.filter_by(email=email).first()
        verify = user.verify_password(password)
        if not verify:
            return {'message': 'username or password error!'}, 403
        else:
            g.current_user = user
            token = user.generate_confirm_token()
            return {"token": token}, 200


class VerifyPassword(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, required=True, location='json')
        super(VerifyPassword, self).__init__()

    @auth.verify_password
    def post(self):
        args = self.reqparse.parse_args()
        token = args['token']
        g.current_user = User.verify_auth_token(token)
        if g.current_user:
            g.token_used = True
            return True


class GetToken(Resource):

    @staticmethod
    def get():
        if g.current_user is None or g.token_used:
            return {"message": "Invalid credentials"},
        return {
            "token": g.current_user.generate_confirm_token(),
            "expiration": 3600
        }, 200


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user and not g.current_user.confirmed:
        return {'message': 'Unconfirmed account'}, 200

api.add_resource(Login, '/login/')
api.add_resource(GetToken, '/get_token/')
