from sanic import Blueprint
from sanic_restful import Api

bp = Blueprint('auth', url_prefix='/auth')
api = Api(bp)

from .main import SendEmailAuth, UserExist, EmailAuth
from .password import Password
from .permission import UserPermission, PostPermission, CommentPermission
from .token import Token

api.add_resource(Token, '/token')
api.add_resource(EmailAuth, '/email_auth/<token>')
api.add_resource(PostPermission, '/post_permission')
api.add_resource(CommentPermission, '/comment_permission')
api.add_resource(UserPermission, '/user_permission')
api.add_resource(SendEmailAuth, '/send_email_auth')
api.add_resource(Password, '/password')
api.add_resource(UserExist, '/user_exist')
