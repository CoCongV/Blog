from flask import g, request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import Forbidden

from blog.api_v1 import token_auth
from blog.api_v1.decorators import permission_required
from blog.models import Permission, User, Post, Role


class UserPermission(Resource):

    decorators = [token_auth.login_required]

    def get(self):
        uid = request.args.get('uid')
        user = User.get(uid)
        if g.current_user == user and g.current_user.can(
                Permission.ADMINISTER):
            return ''
        raise Forbidden()


class PostPermission(Resource):
    decorators = [token_auth.login_required]

    def get(self):
        print(request.args)
        post = Post.query.get(request.args['post_id'])
        if g.current_user == post.author or g.current_user.can(
                Permission.ADMINISTER):
            return ''
        raise Forbidden()


class CommentPermission(Resource):

    decorators = [token_auth.login_required]

    def get(self):
        if g.current_user.can(Permission.COMMENT) and g.current_user.confirmed:
            return {}
        raise Forbidden()


class UpdatePermission(Resource):
    decorators = [permission_required(Permission.COMMENT), token_auth.login_required]

    def post(self):
        g.current_user.role = Role.query.filter_by(name='Advanced_User').first()
        g.current_user.save()
        return {'permission': g.current_user.role.permissions}
        
    