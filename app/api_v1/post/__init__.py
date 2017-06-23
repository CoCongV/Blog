from flask import Blueprint, current_app
from flask_sqlalchemy import get_debug_queries
from flask_restful import Api, reqparse

api_post = Blueprint('post', __name__)
api = Api(api_post)


post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'title',
    location='json',
    required=True
)
post_parser.add_argument(
    'content',
    location='json',
    required=True
)
post_parser.add_argument(
    'tags',
    location='json',
    action='append',
    required=True
)

from .posts import PostsView
from .post import PostView
from .tag import Tag
from .timeline import Timeline

api.add_resource(PostView, '/post/')
api.add_resource(PostsView, '/posts/')
api.add_resource(Tag, '/tag/')
api.add_resource(Timeline, '/time/')


@api_post.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['BLOG_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' % (query.statement, query.parameters, query.duration, query.context)
            )
    return response
