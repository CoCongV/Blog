from flask import Blueprint
from flask_restful import Api

from .token import Token


api_auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(api_auth)

api.add_resource(Token, '/get_token/')
