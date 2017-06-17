from flask_httpauth import HTTPTokenAuth

from .decorators import permission_required


class StateCode(object):
    SUCCESS = 200
    CREATED = 201
    UNAUTHORIZED_ACCESS = 401
    PERMISSION_FORBIDDEN = 403


# api_comment = Blueprint('comment', __name__, url_prefix='/comment/')
token_auth = HTTPTokenAuth(scheme='token')

from .auth import authentication

