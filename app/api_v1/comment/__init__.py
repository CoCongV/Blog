from flask import Blueprint
from flask_restful import Api

api_comment = Blueprint('comment', __name__, url_prefix='/comment')
api = Api(api_comment)


from .comment import CommentApi

api.add_resource(CommentApi, '/list')
