from flask import current_app
from flask_restful import reqparse, Resource
from werkzeug.exceptions import Forbidden

from blog.models import User


reqparse = reqparse.RequestParser()
reqparse.add_argument('email', required=True, location='json', type=str)
reqparse.add_argument('password', required=True, location='json', type=str)


class LoginView(Resource):

    def post(self):
        args = reqparse.parse_args()
        print(args)
        user = User.query.filter_by(email=args.email).first()

        if not user:
            raise Forbidden('Email Error')
        if not user.verify_password(args.password):
            raise Forbidden('Password Error')

        token = user.generate_confirm_token()
        return {
            'token': token,
            'username': user.username,
            'permission': user.role.permissions,
            'avatar': user.avatar,
            'expiration': current_app.config['LOGIN_TOKEN_EXPIRES']
        }
