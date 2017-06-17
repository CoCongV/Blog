from flask import Blueprint
from flask_restful import Api

from .users import UserView
from .login import LoginView

api_user = Blueprint('user', __name__, url_prefix='/user')
api = Api(api_user)

api.add_resource(UserView, '/')
api.add_resource(LoginView, '/login/')
