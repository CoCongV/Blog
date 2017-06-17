from flask import current_app, request, url_for
from flask_restful import Resource

from app.api_v1 import StateCode

from app.models import Post


class PostsView(Resource, StateCode):

    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = Post.query.paginate(
            page, per_page=current_app.config['BLOG_POST_PER_PAGE'],
            error_out=False
        )
        posts = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_posts', page=page - 1, _external=True)
        _next = None
        if pagination.has_next:
            _next = url_for('api.get_posts', page=page + 1, _external=True)
        return {
            'posts': [post.to_json() for post in posts],
            'prev': prev,
            'next': _next,
            'count': pagination.total
        }, self.SUCCESS
