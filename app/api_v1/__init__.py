from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource

from .decorators import permission_required


class HTTPStatusCode(object):
    SUCCESS = 200
    CREATED = 201
    UNAUTHORIZED_ACCESS = 401
    PERMISSION_FORBIDDEN = 403
    USER_EXIST = 409  # 用户信息已被使用

    def __init__(self):
        super(HTTPStatusCode, self).__init__()

# api_comment = Blueprint('comment', __name__, url_prefix='/comment/')
token_auth = HTTPTokenAuth(scheme='token')

from .auth import authentication
from .error import PermissionForbiddenError, UserAlreadyExistsError, AuthorizedError
