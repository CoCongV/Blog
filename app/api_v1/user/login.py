from flask import g
from flask_restful import reqparse, Resource

from app.models import User
from app.api_v1 import HTTPStatusCodeMixin
from app.api_v1.error import AuthorizedError


class LoginView(Resource, HTTPStatusCodeMixin):

    def __init__(self):
        super(LoginView, self).__init__()
        self.expiration = 86400
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', required=True, location='json', type=str)
        self.reqparse.add_argument('password', required=True, location='json', type=str)

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            return AuthorizedError('Email Error')
        verify = user.verify_password(password)
        if not verify:
            return AuthorizedError('Password Error')
        else:
            g.current_user = user
            token = user.generate_confirm_token(expiration=self.expiration)
            return {
                       'token': token,
                       'expiration': self.expiration,
                       'username': user.username,
                       'permission': user.role.permissions
                   }, self.SUCCESS
