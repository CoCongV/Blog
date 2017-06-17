from flask import g, url_for
from flask_restful import Resource

from app.models import Post, Permission
from app.api_v1 import permission_required, StateCode, token_auth

from . import post_parser


class PostView(Resource, StateCode):

    @permission_required(Permission.ADMINISTER)
    @token_auth.login_required
    def post(self):
        args = post_parser.parse_args()
        title = args['title']
        body = args['body']
        tags = args['tags']
        author = g.current_user
        post = Post.create(title=title, body=body, tags=tags, author_id=author.id)
        return {"data": post.to_json(),
                'location': url_for('api.get_post', id=post.id, _external=True)}, self.CREATED

    def get(self, id):
        post = Post.get_or_404(id)
        if g.current_user != post.author:
            return {"message": "Insufficient Permissions"}, self.PERMISSION_FORBIDDEN
        else:
            return {"data": post.to_json()}, self.SUCCESS

    @permission_required(Permission.ADMINISTER)
    @token_auth.login_required
    def put(self, id):
        args = post_parser.parse_args()
        title = args['title']
        body = args['body']
        tags = args['tags']
        post = Post.get(id)
        if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
            return {"message": "Insufficient permissions"}, self.PERMISSION_FORBIDDEN
        post.body = body
        post.title = title
        post.tags = tags
        post.save()
        return self.SUCCESS

    @permission_required(Permission.ADMINISTER)
    @token_auth.login_required
    def delete(self, id):
        post = Post.get_or_404(id)
        if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
            return {"message": "Insufficient permissions"}, self.PERMISSION_FORBIDDEN
        post.delete()
        return 200
