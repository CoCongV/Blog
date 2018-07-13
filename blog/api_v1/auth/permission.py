from flask import g, request
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from blog.api_v1 import token_auth
from blog.models import Permission, User, Post


class UserPermission(Resource):

    decorators = [token_auth.login_required]

    def get(self):
        uid = request.args.get('uid')
        user = User.query.get(uid)
        if g.current_user == user and g.current_user.can(
                Permission.ADMINISTER):
            return {}
        raise Forbidden()


class PostPermission(Resource):
    decorators = [token_auth.login_required]

    def get(self):
        post_id = request.args.get('post_id')
        post = Post.query.get(post_id)
        if g.current_user == post.author or g.current_user.can(
                Permission.ADMINISTER):
            return {}
        raise Forbidden()


class CommentPermission(Resource):

    decorators = [token_auth.login_required]

    def get(self):
        if g.current_user.confirmed and g.current_user.can(Permission.COMMENT):
            return {}
        raise Forbidden()
