from sanic import Blueprint
from sanic_restful import Api

bp = Blueprint('comment', url_prefix='/comments')
api = Api(bp)

from .main import CommentsApi

api.add_resource(CommentsApi, '')
