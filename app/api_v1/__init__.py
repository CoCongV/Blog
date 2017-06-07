from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


from .authentication import auth
from .decorators import permission_required


class StateCode(object):
    SUCCESS = 200
    FORBIDDEN = 403


