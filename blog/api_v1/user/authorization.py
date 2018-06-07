from sanic.exceptions import Unauthorized
from sanic_restful import Resource, reqparse

from blog.decorators import login_requred
from blog.models import User


parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


class Login(Resource):

    async def post(self, request):
        args = parser.parse_args(request)
        user = await User.query.where(User.email == args.email).first()

        if not user:
            raise Unauthorized('用户不存在')
        elif not user.verify_password(args.password):
            raise Unauthorized('密码错误')
        else:
            return {
                'token':
                user.generate_confirm_token(request.app.config.SECRET_KEY),
                'username': user.username,
                'permission': user.role.permission
            }


class Logout(Resource):

    method_decorators = [login_requred]

    async def delete(self, request):
        pass
