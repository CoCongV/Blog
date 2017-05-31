from flask import g, request, current_app, url_for
from flask_restful import Resource, reqparse

from .. import db
from ..models import Post
from . import api


class GetPosts(Resource):

    @staticmethod
    def get():
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
        }, 200


class GetPost(Resource):

    @staticmethod
    def get(id):
        post = Post.get_or_404(id)
        return {
            'post': post.to_json()
        }, 200


class NewPost(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, location='json')
        self.reqparse.add_argument('body', type=str, required=True, location='json')
        self.reqparse.add_argument('tags', type=list, required=True, location='json')

    def post(self):
        args = self.reqparse.parse_args()
        title = args['title']
        body = args['body']
        tags = args['tags']



api.add_resource(GetPosts, '/posts/')
api.add_resource(GetPost, '/posts/<int:id>')
