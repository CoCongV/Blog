from flask import g, url_for, current_app
from flask_restful import reqparse, Resource
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from werkzeug.exceptions import Forbidden

from blog.api_v1 import token_auth
from blog.errors import UserAlreadyExistsError
from blog.models import User, Role
from blog.utils.celery.email import send_email
from blog.utils.web import HTTPStatusCodeMixin


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
    'username', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'location', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'about_me', type=str, location='json', store_missing=False)
reqparse_patch.add_argument(
    'password', type=str, location='json', store_missing=False)


class UserView(Resource, HTTPStatusCodeMixin):
    method_decorators = {
        'get': [token_auth.login_required],
        'patch': [token_auth.login_required]
    }

    def get(self):
        # get user info
        if not g.current_user.is_anonymous:
            json_user = g.current_user.to_json()
            return json_user, self.SUCCESS
        return {'username': ''}, self.SUCCESS

    def post(self):
        # register user
        args = user_reqparse.parse_args()
        try:
            role = Role.query.filter_by(permissions=2).first()
            user = User.create(email=args['email'],
                               username=args['username'],
                               password=args['password'],
                               location=args.get('location'),
                               about_me=args.get('about'),
                               role=role)
        except (IntegrityError, InvalidRequestError):
            raise UserAlreadyExistsError()
        except DataError:
            raise UserAlreadyExistsError()
        token = user.generate_confirm_token(expiration=86400)
        email_token = user.generate_email_token()
        send_email.delay(
            to=user.email,
            subject='Confirm Your Account',
            template='mail/confirm',
            user=user.username,
            url=url_for('auth.email_auth', token=email_token, _external=True))
        current_app.logger.info(
            'New User Exist: {}, {}'.format(user.id, user.email))
        return {
            'token': token,
            'permission': user.role.permissions
        }, self.SUCCESS

    def patch(self):
        args = reqparse_patch.parse_args()
        print(args)
        g.current_user.update(**args)
        return {}, self.SUCCESS
