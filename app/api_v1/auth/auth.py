from flask import g, url_for, request, redirect
from flask_restful import Resource, reqparse

from app.api_v1 import token_auth
from app.api_v1.decorators import permission_required
from app.errors import UserAlreadyExistsError, AuthorizedError
from app.utils.celery.email import send_email
from app.utils.web import HTTPStatusCodeMixin
from app.models import Permission, User


class SendEmailAuth(Resource, HTTPStatusCodeMixin):

    decorators = [permission_required(Permission.COMMENT),
                  token_auth.login_required]

    def get(self):
        # 发送验证邮件
        user = g.current_user
        if not user.is_anonymous:
            email_token = g.current_user.generate_email_token()
            send_email.delay(
                to=user.email,
                subject='Confirm Your Account',
                template='mail/confirm',
                user=user.username,
                url=url_for(
                    'auth.email_auth', token=email_token, _external=True))
        return {}, self.SUCCESS


class EmailExist(Resource, HTTPStatusCodeMixin):

    def get(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument('email', type=str, location='args')
        email = _reqparse.parse_args()['email']
        user = User.query.filter_by(email=email).first()
        if user:
            raise UserAlreadyExistsError()
        return {}, self.SUCCESS


class EmailAuth(Resource, HTTPStatusCodeMixin):

    def get(self, token):
        result = User.verify_email_token(token)
        if result:
            return redirect('/')
        raise AuthorizedError()


class UsernameExist(Resource, HTTPStatusCodeMixin):

    def get(self):
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            raise UserAlreadyExistsError()
        return {}, self.SUCCESS
