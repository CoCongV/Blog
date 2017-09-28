from flask import g, url_for
from flask_restful import reqparse, Resource
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError

from app.api_v1 import token_auth
from app.errors import UserAlreadyExistsError
from app.models import User, Role
from app.utils.celery.email import send_email
from app.utils.web import HTTPStatusCodeMixin


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
    'email', type=str, location='json', store_missing=True)
reqparse_patch.add_argument(
    'username', type=str, location='json', store_missing=True)
reqparse_patch.add_argument(
    'location', type=str, location='json', store_missing=True)
reqparse_patch.add_argument(
    'about_me', type=str, location='json', store_missing=True)
reqparse_patch.add_argument(
    'password', type=str, location='json', store_missing=True)


class UserView(Resource, HTTPStatusCodeMixin):

    @token_auth.login_required
    def get(self):
        # get user info
        user = g.current_user
        if not user.is_anonymous:
            json_user = user.to_json()
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
        return {
            'token': token,
            'permission': user.role.permissions
        }, self.SUCCESS

    @token_auth.login_required
    def patch(self):
        args = reqparse_patch.parse_args()
        g.current_user.update(**args)
        return {}, self.SUCCESS
