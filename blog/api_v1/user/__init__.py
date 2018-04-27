from sanic import Blueprint
from sanic_restful import Api

bp = Blueprint('user', url_prefix='/user')
api = Api(bp)


