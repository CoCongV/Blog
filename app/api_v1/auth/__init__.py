from flask import Blueprint
from flask_restful import Api

from .token import Token
from .token_auth import EmailAuth


api_auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(api_auth)

api.add_resource(Token, '/token/')
api.add_resource(EmailAuth, '/email_auth/<token>/', endpoint='email_auth')
