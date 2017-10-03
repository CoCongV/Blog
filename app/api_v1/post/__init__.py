from flask import Blueprint, current_app
from flask_sqlalchemy import get_debug_queries
from flask_restful import Api

api_post = Blueprint('post', __name__)
api = Api(api_post)


from .post import PostView, PostsView
from .tag import Tag
from .timeline import Timeline
from .post_search import PostSearch
from .media import PhotoStorage

api.add_resource(PostView, '/post/<int: post_id>/')
api.add_resource(PostsView, '/posts/')
api.add_resource(Tag, '/tag/')
api.add_resource(Timeline, '/time/')
api.add_resource(PostSearch, '/search/', endpoint='post_search')
api.add_resource(PhotoStorage, '/photo/', endpoint='upload')


@api_post.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['BLOG_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response
