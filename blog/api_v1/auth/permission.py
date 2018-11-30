from flask import g, request
from flask_restful import Resource, reqparse
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
            return ''
        raise Forbidden()


post_reqparse = reqparse.RequestParser()
post_reqparse.add_argument('post_id', type=int, location='args', required=True)


class PostPermission(Resource):
    decorators = [token_auth.login_required]

    def get(self):
        args = post_reqparse.parse_args()
        post = Post.query.get(args.post_id)
        if g.current_user == post.author or g.current_user.can(
                Permission.ADMINISTER):
            return {}
        raise Forbidden()


class CommentPermission(Resource):

    decorators = [token_auth.login_required]

    def get(self):
        if g.current_user.can(Permission.COMMENT) and g.current_user.confirmed:
            return {}
        raise Forbidden()
