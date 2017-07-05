from flask import g, url_for, request
from flask_restful import Resource

from app.api_v1 import HTTPStatusCode, token_auth, permission_required
from app.utils.send_mail import send_email
from app.models import Permission, User


class SendEmailAuth(Resource, HTTPStatusCode):

    decorators = [permission_required(Permission.COMMENT),
                  token_auth.login_required]

    def get(self):
        # 发送验证邮件
        user = g.current_user
        if not user.is_anonymous:
            email_token = g.current_user.generate_email_token()
            send_email.delay(to=user.email, subject='Confirm Your Account',
                             template='mail/confirm', user=user.username,
                             url=url_for('auth.email_auth', token=email_token, _external=True))
        return {}, self.SUCCESS


class EmailExist(Resource, HTTPStatusCode):

    def get(self):
        email = request.args.get('email')
        user = User.query.filter_by(email=email)
        if user:
            return {}, self.USER_EXIST
        return {}, self.SUCCESS
