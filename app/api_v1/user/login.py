from flask import g, request
from flask_restful import reqparse

from app.models import User
from app.api_v1 import BaseResource


class LoginView(BaseResource):

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
            return {'message': 'Email error'}, self.UNAUTHORIZED_ACCESS
        verify = user.verify_password(password)
        if not verify:
            return {'message': 'Password error!'}, self.UNAUTHORIZED_ACCESS
        else:
            g.current_user = user
            token = user.generate_confirm_token(expiration=self.expiration)
            return {
                       'token': token,
                       'expiration': self.expiration,
                       'username': user.username,
                       'permission': user.role.permissions
                   }, self.SUCCESS
