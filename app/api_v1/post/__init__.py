from flask import Blueprint
from flask_restful import Api, reqparse

api_post = Blueprint('post', __name__, url_prefix='/post')
api = Api(api_post)


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'title',
    location='json',
    required=True
)
post_parser.add_argument(
    'body',
    location='json',
    required=True
)
post_parser.add_argument(
    'tags',
    location='json',
    required=True
)

from .posts import PostsView
from .post import PostView

api.add_resource(PostView, '/article/')
api.add_resource(PostsView, '/articles/')
