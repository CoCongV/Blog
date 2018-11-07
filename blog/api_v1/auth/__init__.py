from flask import Blueprint
from flask_restful import Api

from .auth import (SendEmailAuth,
                   EmailExist,
                   EmailAuth,
                   UsernameExist)
from .captcha import ImageCaptcha
from .password import Password
from .permission import (PostPermission,
                         CommentPermission,
                         UserPermission)
from .token import Token


api_auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(api_auth)

api.add_resource(Token, '/token/')
api.add_resource(EmailAuth, '/email_auth/<token>/',
                 endpoint='email_auth')
api.add_resource(PostPermission, '/post_permission/',
                 endpoint='post_permission')
api.add_resource(CommentPermission, '/comment_permission',
                 endpoint='comment_permission')
api.add_resource(UserPermission, '/user_permission',
                 endpoint='user_permission')
api.add_resource(SendEmailAuth, '/send_email_auth/',
                 endpoint='send_email_auth')
api.add_resource(Password, '/password/')
api.add_resource(EmailExist, '/email_exist/',
                 endpoint='email_exist')
api.add_resource(UsernameExist, '/username_exist/',
                 endpoint='username_exist')
api.add_resource(ImageCaptcha, '/img_captcha',
                 endpoint='img_captcha')
