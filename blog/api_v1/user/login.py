from flask import g
from flask_restful import reqparse, Resource

from blog.models import User
from blog.utils.web import HTTPStatusCodeMixin
from blog.errors import AuthorizedError


class LoginView(Resource, HTTPStatusCodeMixin):

    def __init__(self):
        super(LoginView, self).__init__()
        self.expiration = 86400
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email', required=True, location='json', type=str)
        self.reqparse.add_argument(
            'password', required=True, location='json', type=str)

    def post(self):
        args = self.reqparse.parse_args()
        email = args['email']
        password = args['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            raise AuthorizedError('Email Error')
        verify = user.verify_password(password)
        if not verify:
            raise AuthorizedError('Password Error')
        else:
            g.current_user = user
            token = user.generate_confirm_token(expiration=self.expiration)
            return {
                'token': token,
                'expiration': self.expiration,
                'username': user.username,
                'permission': user.role.permissions
            }, self.SUCCESS
