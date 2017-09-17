from flask_httpauth import HTTPTokenAuth
from app.utils.web import NestableBlueprint


api_v1 = NestableBlueprint('api_v1', __name__, url_prefix='/api_v1')
token_auth = HTTPTokenAuth(scheme='token')

from .auth import authentication
