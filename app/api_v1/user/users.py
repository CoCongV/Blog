from flask import g
from flask_restful import reqparse

from app.models import User
from app.api_v1 import token_auth, BaseResource


class UserView(BaseResource):
    # decorators = [token_auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json')
        self.reqparse.add_argument('username', type=str, required=True, location='json')
        self.reqparse.add_argument('password', type=str, required=True, location='json')
        self.reqparse.add_argument('location', type=str, location='json')
        self.reqparse.add_argument('about', type=str, location='json')
        self.reqparse.add_argument('avatar', location='file')

    @token_auth.login_required
    def get(self):
        # get user info
        user = g.current_user.json()
        return user, self.SUCCESS

    def post(self):
        # register user
        args = self.reqparse.parse_args()
        user = User.create(email=args['email'],
                           username=args['username'],
                           password=args['password'],
                           location=args.get('location'),
                           about_me=args.get('about'))
        token = user.generate_confirm_token(expiration=86400)
        return {'token': token}, self.SUCCESS
