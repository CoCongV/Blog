from flask import g, url_for
from flask_restful import reqparse

from app.models import User
from app.lib.send_mail import send_email
from app.api_v1 import token_auth, BaseResource


class UserView(BaseResource):
    # decorators = [token_auth.login_required]

    def __init__(self):
        super(UserView, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json')
        self.reqparse.add_argument('username', type=str, required=True, location='json')
        self.reqparse.add_argument('location', type=str, location='json')
        self.reqparse.add_argument('about', type=str, location='json')
        self.reqparse.add_argument('avatar', location='file')

    @token_auth.login_required
    def get(self):
        # get user info
        user = g.current_user
        if not user.is_anonymous:
            json_user = user.json()
            return json_user, self.SUCCESS
        return {'username': ''}, self.SUCCESS

    def post(self):
        # register user
        self.reqparse.add_argument('password', type=str, required=True, location='json')
        args = self.reqparse.parse_args()
        user = User.create(email=args['email'],
                           username=args['username'],
                           password=args['password'],
                           location=args.get('location'),
                           about_me=args.get('about'),
                           role_id=1)
        token = user.generate_confirm_token(expiration=86400)
        email_token = user.generate_email_token()
        send_email.delay(to=user.email, subject='Confirm Your Account',
                         template='mail/confirm', user=user.username,
                         url=url_for('auth.email_auth', token=email_token, _external=True))
        return {'token': token}, self.SUCCESS

    @token_auth.login_required
    def put(self):
        args = self.reqparse.parse_args()
        username = args['username']
        email = args['email']
        user = User.query.filter(User.id != g.current_user.id, username=username)
        if user:
            return {'message': '用户名已被使用'}, self.USER_EXIST
        user = User.query.filter(User.id != g.current_user.id, email=email)
        if user:
            return {'message': '邮箱被占用'}, self.USER_EXIST
        return self.SUCCESS
