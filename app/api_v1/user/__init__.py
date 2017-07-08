from flask import Blueprint
from flask_restful import Api

from .users import UserView
from .login import LoginView
from .user_profile import UserProfile
from .permission import PermissionAuth

api_user = Blueprint('user', __name__, url_prefix='/user')
api = Api(api_user)

api.add_resource(UserView, '/')
api.add_resource(LoginView, '/login/')
api.add_resource(UserProfile, '/profile/<int:uid>/', endpoint='user_profile')
api.add_resource(PermissionAuth, '/permission/', endpoint='permission_auth')
