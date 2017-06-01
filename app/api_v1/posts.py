from flask import g, request, current_app, url_for
from flask_restful import Resource, reqparse

from ..models import Post, Permission
from . import api, permission_required, StateCode


class GetPosts(Resource, StateCode):

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


class GetPost(Resource, StateCode):

    def get(self, id):
        post = Post.get_or_404(id)
        return {
            'post': post.to_json()
        }, self.SUCCESS

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


class NewPost(Resource):

    @permission_required(Permission.ADMINISTER)
    def post(self):
        args = post_parser.parse_args()
        title = args['title']
        body = args['body']
        tags = args['tags']
        author = g.current_user
        post = Post.create(title=title, body=body, tags=tags, author_id=author.id)
        post.save()
        return {"data": post.to_json(),
                'location': url_for('api.get_post', id=post.id, _external=True)}, 201


class EditPost(Resource, StateCode):

    @permission_required(Permission.ADMINISTER)
    def get(self, id):
        post = Post.get_or_404(id)
        if g.current_user != post.author:
            return {"message": "Insufficient Permissions"}, 403
        else:
            return {"data": post.to_json()}, 201

    @permission_required(Permission.ADMINISTER)
    def put(self, id):
        args = post_parser.parse_args()
        title = args['title']
        body = args['body']
        tags = args['tags']
        post = Post.get(id)
        if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
            return {"message": "Insufficient permissions"}, self.FORBIDDEN
        post.body = body
        post.title = title
        post.tags = tags
        post.save()
        return self.SUCCESS

    @permission_required(Permission.ADMINISTER)
    def delete(self, id):
        post = Post.get_or_404(id)
        if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
            return {"message": "Insufficient permissions"}, self.FORBIDDEN
        post.delete()
        return 200

api.add_resource(GetPosts, '/posts/')
api.add_resource(GetPost, '/posts/<int:id>')
api.add_resource(NewPost, '/new_post/')
api.add_resource(EditPost, '/edit_post/<int:id>')
