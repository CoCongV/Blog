from flask import Blueprint
from flask_restful import Api

from .token import Token
from .token_auth import EmailAuth
from .post_permission import PostPermission
from .comment_permission import CommentPermission
from .user_permission import UserPermission
from .email_auth import SendEmailAuth


api_auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(api_auth)

api.add_resource(Token, '/token/')
api.add_resource(EmailAuth, '/email_auth/<token>/', endpoint='email_auth')
api.add_resource(PostPermission, '/post_permission/', endpoint='post_permission')
api.add_resource(CommentPermission, '/comment_permission', endpoint='comment_permission')
api.add_resource(UserPermission, '/user_permission', endpoint='user_permission')
api.add_resource(SendEmailAuth, '/send_email_auth/', endpoint='send_email_auth')
