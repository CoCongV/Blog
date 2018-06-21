from sanic import Blueprint
from sanic_restful import Api

bp = Blueprint('user', url_prefix='/user')
api = Api(bp)

from .main import UserResouce
from .authorization import Login
from .profile import UserProfile
from .permission import PermissionAuth
from .media import Avatar

api.add_resource(UserResouce, '/')
api.add_resource(Login, '/login')
api.add_resource(UserProfile, '/profile')
api.add_resource(PermissionAuth, '/permission')
api.add_resource(Avatar, '/avatar')
