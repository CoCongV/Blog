from sanic.exceptions import Forbidden
from sanic_restful import Resource, reqparse

from blog.decorators import login_requred
from blog.models import Permission, User, Post


user_parser = reqparse.RequestParser()
user_parser.add_argument('uid', type=int, required=True)


class UserPermission(Resource):

    decorators = [login_requred]

    async def get(self, request):
        params = user_parser.parse_args(request)
        user = await User.get(params.id)
        if request['current_user'] == user and request['current_user'].can(
                Permission.ADMINISTER):
            return '', 204
        else:
            raise Forbidden("Permission Exception")


post_parser = reqparse.RequestParser()
post_parser.add_argument('post_id', type=int, required=True)


class PostPermission(Resource):

    decorators = [login_requred]

    async def get(self, request):
        params = user_parser.parse_args(request)
        post = await Post.get(params.post_id)
        if request['current_user'] == post.author or request['current_user'].can(
                Permission.ADMINISTER):
            return '', 204
        else:
            raise Forbidden("Permission Exception")


class CommentPermission(Resource):

    decorators = [login_requred]

    async def get(self, request):
        if request['current_user'].confirmed and request['current_user'].can(Permission.COMMENT):
            return '', 204
        else:
            raise Forbidden("Permission Exception")
