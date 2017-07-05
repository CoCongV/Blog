from flask import current_app, request, url_for
from flask_restful import Resource

from app import db
from app.api_v1 import HTTPStatusCode
from app.models import Post


class PostsView(Resource, HTTPStatusCode):

    def get(self):
        uid = request.args.get('uid')
        page = request.args.get('page', 1, type=int)
        if uid:
            pagination = Post.query.filter_by(author_id=uid).order_by(db.desc('timestamp')).paginate(
                page, per_page=current_app.config['BLOG_POST_PER_PAGE'],
                error_out=False
            )
        else:
            pagination = Post.query.order_by(db.desc('timestamp')).paginate(
                page, per_page=current_app.config['BLOG_POST_PER_PAGE'],
                error_out=False
            )
        posts = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('post.postsview', page=page - 1, _external=True)
        _next = None
        if pagination.has_next:
            _next = url_for('post.postsview', page=page + 1, _external=True)
        return {
            'posts': [post.to_json(500) for post in posts],
            'prev': prev,
            'next': _next,
            'count': pagination.total
        }, self.SUCCESS
