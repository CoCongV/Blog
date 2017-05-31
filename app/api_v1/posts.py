from flask import g, request, current_app, url_for
from flask_restful import Resource, reqparse

from .. import db
from ..models import Post
from . import api


class GetPosts(Resource):

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
        next = None
        if pagination.has_next:
            next = url_for('api.get_posts', page=page + 1, _external=True)
        return {
            'posts': "yes",
            'prev': prev,
            'next': next,
            'count': pagination.total
        }, 200
