from flask import g, url_for, current_app
from flask_restful import reqparse, Resource
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from werkzeug.exceptions import Forbidden, Unauthorized

from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.exceptions import AlreadyExists
from blog.models import User, Role, Permission
from blog.utils.celery.email import send_email


user_reqparse = reqparse.RequestParser()
user_reqparse.add_argument('email', type=str, required=True, location='json')
user_reqparse.add_argument(
    'username', type=str, required=True, location='json')
user_reqparse.add_argument('location', type=str, location='json')
user_reqparse.add_argument('about_me', type=str, location='json')
user_reqparse.add_argument(
    'password', type=str, required=True, location='json')


reqparse_patch = reqparse.RequestParser()
reqparse_patch.add_argument(
    'email', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'kindle_email', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'username', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'location', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'about_me', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'password', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'old_password', type=str, location='json', store_missing=False)


class UserView(Resource):
    method_decorators = {
        'get': [permission_required(Permission.COMMENT), token_auth.login_required],
        'patch': [permission_required(Permission.COMMENT), token_auth.login_required]
    }

    def get(self):
        return g.current_user.to_json()

    def post(self):
        # register user
        args = user_reqparse.parse_args()
        try:
            role = Role.query.filter_by(name='User').first()
            permission = role.permissions
            user = User.create(email=args['email'],
                               username=args['username'],
                               password=args['password'],
                               location=args.get('location'),
                               about_me=args.get('about'),
                               role=role)
        except (IntegrityError, InvalidRequestError, DataError):
            raise AlreadyExists()

        token = user.generate_confirm_token(
            expiration=current_app.config['LOGIN_TOKEN_EXPIRES'])
        email_token = user.generate_email_token()
        send_email(
            to=user.email,
            subject='Confirm Your Account',
            template='mail/confirm',
            user=user.username,
            url=url_for('auth.email_auth', token=email_token, _external=True))
        current_app.logger.info(
            'New User Exist: {}, {}'.format(user.id, user.email))
        return {
            'token': token,
            'username': user.username,
            'permission': permission,
            'expiration': current_app.config['LOGIN_TOKEN_EXPIRES'],
            'avatar': user.avatar,
        }

    def patch(self):
        args = reqparse_patch.parse_args()
        if args.get('password'):
            if args.get('old_password') and g.current_user.verify_password(args.get('old_password')):
                pass
            else:
                raise Forbidden('Password error')
        g.current_user.update(**args)
        return g.current_user.to_json(), 200
