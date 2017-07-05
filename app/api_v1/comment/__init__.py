from flask import Blueprint
from flask_restful import Api, reqparse

api_comment = Blueprint('comment', __name__, url_prefix='/comment')
api = Api(api_comment)

comment_parse = reqparse.RequestParser()
comment_parse.add_argument(
    'body',
    location='json',
    required=True
)
comment_parse.add_argument(
    'reply',
    location='json',
    required=False
)
comment_parse.add_argument(
    'post',
    location='json',
    required=True
)

from .comment import CommentView

api.add_resource(CommentView, '/')
