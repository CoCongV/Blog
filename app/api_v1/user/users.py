from flask import g, url_for
from flask_restful import reqparse, Resource
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError

from app.api_v1 import token_auth, HTTPStatusCode
from app.api_v1.error import UserAlreadyExistsError
from app.utils.send_mail import send_email
from app.models import User, Role


class UserView(Resource, HTTPStatusCode):

    def __init__(self):
        super(UserView, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json')
        self.reqparse.add_argument('username', type=str, required=True, location='json')
        self.reqparse.add_argument('location', type=str, location='json')
        self.reqparse.add_argument('about_me', type=str, location='json')

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
        self.reqparse.add_argument('password', type=str, required=True, location='json')
        args = self.reqparse.parse_args()
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
        send_email.delay(to=user.email, subject='Confirm Your Account',
                         template='mail/confirm', user=user.username,
                         url=url_for('auth.email_auth', token=email_token, _external=True))
        return {'token': token, 'permission': user.role.permissions}, self.SUCCESS

    @token_auth.login_required
    def put(self):
        # update user
        args = self.reqparse.parse_args()
        username = args['username']
        email = args['email']
        user = User.query.filter(User.id != g.current_user.id).filter_by(username=username).first()
        if user:
            raise UserAlreadyExistsError('Username Exist')
        user = User.query.filter(User.id != g.current_user.id, User.email == email).first()
        if user:
            raise UserAlreadyExistsError('Email Exist')
        g.current_user.update(**args)
        return {}, self.SUCCESS
