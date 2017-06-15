from flask import Blueprint
from flask_restful import Api
from flask_httpauth import HTTPTokenAuth

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
token_auth = HTTPTokenAuth()


from .decorators import permission_required


class StateCode(object):
    SUCCESS = 200
    PERMISSION_FORBIDDEN = 403
    UNAUTHORIZED_ACCESS = 401

