from flask import g
from flask_restful import Resource, reqparse

from app.models import User
from app.api_v1 import StateCode


class LoginView(Resource, StateCode):

    def __init__(self):
        self.expiration = 86400
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json')
        self.reqparse.add_argument('password', type=str, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password']
        user = User.query.filter_by(email=email).first()
        verify = user.verify_password(password)
        if not verify:
            return {'message': 'username or password error!'}, self.UNAUTHORIZED_ACCESS
        else:
            g.current_user = user
            token = user.generate_confirm_token(expiration=self.expiration)
            return {
                       "token": token,
                       "expiration": self.expiration,
                       "username": user.username
                   }, self.SUCCESS
